'''
Created on 2015年8月24日

@author: Yi Zhang
'''
from stock_db.db_stock import StockCashTable
from stock_db.db_stock import StockCash
from stock_db.db_stock import StockPriceRangeTable
from stock_db.db_stock import StockPriceRange
from stock_db.db_stock import StockTransactionTable
from stock_db.db_stock import StockTransaction
import datetime
import time
import logging

from gtja.Trade import Trade
from stock_holding_algorithm.simple_algorithm import SimpleAlgorithm

class StockProcessor(object):
    '''
    classdocs
    '''


    def __init__(self, account_name, password):
        self.logger = logging.getLogger(__name__)
        self.stock_symbol_list = []
        self.stock_process_index = 0
        self.trade = Trade(account_name, password)
        
        return
        
        '''
        Constructor
        '''
    def login(self):
        self.trade.login()
        return
    
    def close(self):
        self.trade.close()
        return

    def set_stock_symbol_list(self, stock_symbol_list):
        self.stock_symbol_list =stock_symbol_list
        return

    def get_stock_symbol_list(self):
        return self.stock_symbol_list
    
    def keep_alive(self):
        self.trade.enter_stock_menu()
        return
    
    def get_one_stock(self):
        result = self.stock_symbol_list[self.stock_process_index]
        self.stock_process_index += 1
        self.stock_process_index = self.stock_process_index % len(self.stock_symbol_list)
        return result
    
    def get_stock_current_value(self, symbol):
        stock_cash_table = StockCashTable()
        stock_cash = stock_cash_table.get_stock_cash_by_symbol(symbol)
        cash_amount = stock_cash.get_amount()
        
        stock_transaction_table = StockTransactionTable()
        stock_transaction_list = \
            stock_transaction_table.get_stock_transaction_list_by_symbol(symbol)
        quantity = 0
        for stock_transaction in stock_transaction_list:
            buy_or_sell = stock_transaction.get_buy_or_sell()
            if (buy_or_sell == "Buy"):
                quantity = quantity + stock_transaction.get_quantity()
            elif (buy_or_sell == "Sell"):
                quantity = quantity - stock_transaction.get_quantity()
            else:
                # Need to raise an error
                return None
        stock_price = 8.09
        
        total = cash_amount + quantity*stock_price
        
        return total
        
    def update_cash_table(self, symbol, amount_offset):
        stock_cash_table = StockCashTable()
        stock_cash = stock_cash_table.get_stock_cash_by_symbol(symbol)
        new_amount = stock_cash.get_amount() + amount_offset
        stock_cash.set_amount(new_amount)
        stock_cash_table.update_stock_cash(stock_cash)
        return
    
    def add_transaction(self, symbol, buy_or_sell, quantity, price):
        stock_transaction = StockTransaction()
        stock_transaction.set_symbol(symbol)
        stock_transaction.set_buy_or_sell(buy_or_sell)
        stock_transaction.set_quantity(quantity)
        stock_transaction.set_price(price)
        stock_transaction.set_date(datetime.datetime.now())
        
        stock_transaction_table = StockTransactionTable()
        stock_transaction_table.add_stock_transaction(stock_transaction)
        return
    
    def process_stock(self, stock_symbol):
        # get remaining cash for the stock
        stock_cash_table = StockCashTable()
        stock_cash = stock_cash_table.get_stock_cash_by_symbol(stock_symbol)
        # get current price of the stock
        stock_price = self.trade.get_stock_price(stock_symbol)
        
        print("process stock: " + stock_symbol)
        print("remaining_cash={0}".format(stock_cash.amount))
        print("stock_price={0}".format(stock_price))
        
        if(abs(stock_price) < 0.005):
            return
        
        stock_price_range_table = StockPriceRangeTable()
        stock_price_range = stock_price_range_table.get_stock_stock_price_range_by_symbol(stock_symbol)
        price_low = stock_price_range.get_price_low()
        price_high = stock_price_range.get_price_high()
                
        simple_algorithm = SimpleAlgorithm(stock_symbol, price_low, price_high,
                                           stock_price)
        simple_algorithm.calculate()

        buy_or_sell = simple_algorithm.get_suggested_buy_or_sell()
        suggested_amount = simple_algorithm.get_suggested_amount()

        result = "Symbol: {0}\nBuy or Sell: {1}\nAmount: {2}".format(stock_symbol, buy_or_sell,
                                                        suggested_amount)
        print(result)
        
        amount = int(suggested_amount/100) * 100
        
        # we suppost we need 10 for transaction service fee, which is a big enough number
        # for normal transaction
        if (buy_or_sell == "Buy"):
            cash_offset = -1 * (amount * stock_price + 10)
        else:
            cash_offset = amount * stock_price - 10
             
        if (amount >= 100):
            debug_msg = "stock_symbol: {0}\nbuy_or_sell: {1}\namount: {2}\nstock_price: {3}".format(stock_symbol,
                                                                                                    buy_or_sell,
                                                                                                    amount,
                                                                                                    stock_price)
            self.logger.debug(debug_msg)
            debug_msg = "cash_offset: {0}".format(cash_offset)
            self.logger.debug(debug_msg)
            
            
            if (buy_or_sell == "Buy"):
                commission_id = self.trade.buy_stock(stock_symbol, stock_price, amount)
                time.sleep(3)
                commission_state = self.trade.get_commission_state(commission_id)
                if (commission_state != "已成"):
                    result = self.trade.cancel_commission(commission_id)
                    if (result != 1):
                        commission_state = self.trade.get_commission_state(commission_id)
                        if (commission_state == "已成"):
                            self.add_transaction(stock_symbol, buy_or_sell, amount, stock_price)
                            self.update_cash_table(stock_symbol, cash_offset)
                        else:
                            print("Unknown error in canceling transaction")
                            self.logger.debug("Unknown error in canceling transaction.")
                else:
                    self.add_transaction(stock_symbol, buy_or_sell, amount, stock_price)
                    self.update_cash_table(stock_symbol, cash_offset)
            elif (buy_or_sell == "Sell"):
                commission_id = self.trade.sell_stock(stock_symbol, stock_price, amount)
                time.sleep(3)
                commission_state = self.trade.get_commission_state(commission_id)
                if (commission_state != "已成"):
                    result = self.trade.cancel_commission(commission_id)
                    if (result != 1):
                        commission_state = self.trade.get_commission_state(commission_id)
                        if (commission_state == "已成"):
                            self.add_transaction(stock_symbol, buy_or_sell, amount, stock_price)
                            self.update_cash_table(stock_symbol, cash_offset)
                        else:
                            print("Unknown error in canceling transaction")
                            self.logger.debug("Unknown error in canceling transaction.")
                else:
                    self.add_transaction(stock_symbol, buy_or_sell, amount, stock_price)
                    self.update_cash_table(stock_symbol, cash_offset)
            else:
                print("Error!")
             

        return
        
    
