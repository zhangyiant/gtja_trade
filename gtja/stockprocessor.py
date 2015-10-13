'''
Created on 2015年8月24日

@author: Yi Zhang
'''
from stock_db.db_stock import StockCashTable
from stock_db.db_stock import StockCash
from stock_db.db_stock import StockPriceRangeTable
from stock_db.db_stock import StockPriceRange

import time

from gtja.Trade import Trade
from stock_holding_algorithm.simple_algorithm import SimpleAlgorithm

class StockProcessor(object):
    '''
    classdocs
    '''


    def __init__(self, account_name, password):
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
    
    def get_one_stock(self):
        result = self.stock_symbol_list[self.stock_process_index]
        self.stock_process_index += 1
        self.stock_process_index = self.stock_process_index % len(self.stock_symbol_list)
        return result
        
    def process_stock(self, stock_symbol):
        # get remaining cash for the stock
        stock_cash_table = StockCashTable()
        stock_cash = stock_cash_table.get_stock_cash_by_symbol(stock_symbol)
        # get current price of the stock
        stock_price = self.trade.get_stock_price(stock_symbol)
        
        print("process stock: " + stock_symbol)
        print("remaining_cash={0}".format(stock_cash.amount))
        print("stock_price={0}".format(stock_price))
        
        stock_price_range_table = StockPriceRangeTable()
        stock_price_range = stock_price_range_table.get_stock_stock_price_range_by_symbol(stock_symbol)
        price_low = stock_price_range.get_price_low()
        price_high = stock_price_range.get_price_high()
        
        
        simple_algorithm = SimpleAlgorithm(stock_symbol, price_low, price_high,
                                           stock_price)
        simple_algorithm.calculate()

        buy_or_sell = simple_algorithm.get_suggested_buy_or_sell()
        suggested_amount = simple_algorithm.get_suggested_amount()

        result = "Buy or Sell: {0}\nAmount: {1}".format(buy_or_sell,
                                                        suggested_amount)
        print(result)
        
        if (buy_or_sell == "Buy"):
            commission_id = self.trade.buy_stock(stock_symbol, stock_price, suggested_amount)
            time.sleep(3)
            commission_state = self.trade.get_commission_state(commission_id)
            if (commission_state != "已成"):
                # TODO: need to cancel the commission
                pass
        elif (buy_or_sell == "Sell"):
            commission_id = self.trade.sell_stock(stock_symbol, stock_price, suggested_amount)
            time.sleep(3)
            commission_state = self.trade.get_commission_state(commission_id)
            if (commission_state != "已成"):
                # TODO: need to cancel the commission
                pass
        else:
            print("Error!")
            

        return
        
    