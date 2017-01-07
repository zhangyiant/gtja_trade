'''
Created on 2015年8月24日

@author: Yi Zhang
'''
import time
import logging

from stock_db.db_stock import StockCashTable
from stock_db.db_stock import StockCash
from stock_db.db_stock import StockPriceRangeTable
from stock_db.db_stock import StockPriceRange
from stock_db.db_stock import StockTransactionTable
from stock_db.db_stock import StockTransaction
from stock_db.db_stock import StockLowestUnitTable
from stock_db.db_utility import get_lowest_gain
from .utility import \
    complete_buy_transaction, \
    complete_sell_transaction

from gtja.Trade import Trade
from stock_holding_algorithm.simple_algorithm3 import SimpleAlgorithm

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

    def login(self):
        """
            Login GTJA web system
        """
        self.trade.login()
        return

    def close(self):
        """
            Close GTJA web system
        """
        self.trade.close()
        return

    def set_stock_symbol_list(self, stock_symbol_list):
        """
            set symbol list
        """
        self.stock_symbol_list = stock_symbol_list
        return

    def get_stock_symbol_list(self):
        """
            get symbol list
        """
        return self.stock_symbol_list

    def keep_alive(self):
        """
            keep alive method
        """
        #self.trade.enter_stock_menu()
        self.trade.get_current_commission_list()
        return

    def get_one_stock(self):
        """
            select one stock
        """
        result = self.stock_symbol_list[self.stock_process_index]
        self.stock_process_index += 1
        self.stock_process_index = \
            self.stock_process_index % len(self.stock_symbol_list)
        return result

    def process_stock(self, stock_symbol):
        """
            process the stock
        """
        # get remaining cash for the stock
        stock_cash_table = StockCashTable()
        stock_cash = stock_cash_table.get_stock_cash_by_symbol(stock_symbol)
        # get current price of the stock
        stock_price = self.trade.get_stock_price(stock_symbol)

        print("process stock: " + stock_symbol)
        print("remaining_cash={0}".format(stock_cash.amount))
        print("stock_price={0}".format(stock_price))

        if abs(stock_price) < 0.005:
            return

        stock_price_range_table = StockPriceRangeTable()
        stock_price_range = \
            stock_price_range_table.get_stock_stock_price_range_by_symbol(
                stock_symbol)
        price_low = stock_price_range.get_price_low()
        price_high = stock_price_range.get_price_high()

        simple_algorithm = SimpleAlgorithm(stock_symbol, price_low, price_high,
                                           stock_price)
        simple_algorithm.calculate()

        buy_or_sell = simple_algorithm.get_suggested_buy_or_sell()
        suggested_amount = simple_algorithm.get_suggested_amount()

        result = "Symbol: {0}\nBuy or Sell: {1}\nAmount: {2}".format(
            stock_symbol,
            buy_or_sell,
            suggested_amount)
        print(result)

        stock_lowest_unit_table = StockLowestUnitTable()
        stock_lowest_unit = stock_lowest_unit_table.\
                            get_lowest_unit(stock_symbol)
        if stock_lowest_unit is not None:
            lowest_unit = stock_lowest_unit.lowest_unit
            is_integer = stock_lowest_unit.is_integer
        else:
            lowest_unit = 100
            is_integer = True

        if is_integer:
            amount = int(suggested_amount / lowest_unit) * int(lowest_unit)
        else:
            amount = int(suggested_amount / lowest_unit) * lowest_unit

        print(amount)
        if amount >= lowest_unit:
            debug_msg = "stock_symbol: {0}\nbuy_or_sell: {1}\n" + \
                        "amount: {2}\nstock_price: {3}"
            debug_msg = debug_msg.format(
                stock_symbol,
                buy_or_sell,
                amount,
                stock_price)
            self.logger.debug(debug_msg)

            if buy_or_sell == "Buy":
                commission_id = self.trade.buy_stock(
                    stock_symbol,
                    stock_price,
                    amount)
                time.sleep(3)
                commission_state = self.trade.get_commission_state(
                    commission_id)
                if commission_state != "已成":
                    result = self.trade.cancel_commission(commission_id)
                    if result != 1:
                        commission_state = self.trade.get_commission_state(
                            commission_id)
                        if commission_state == "已成":
                            complete_buy_transaction(stock_symbol,
                                                     stock_price,
                                                     amount)
                        else:
                            print("Unknown error in canceling transaction")
                            self.logger.debug(
                                "Unknown error in canceling transaction.")
                else:
                    complete_buy_transaction(stock_symbol,
                                             stock_price,
                                             amount)
            elif buy_or_sell == "Sell":
                lowest_buy_price = StockTransaction.\
                                   get_lowest_buy_price(stock_symbol)
                lowest_buy_price_quantity = StockTransaction.\
                                            get_lowest_buy_price_quantity(
                                                stock_symbol)
                lowest_gain = get_lowest_gain(stock_symbol)
                if lowest_gain is None:
                    lowest_gain = 0.3
                if stock_price - lowest_buy_price < lowest_gain:
                    debug_msg = "stock_price is not high enough. {0} vs {1}"
                    debug_msg = debug_msg.format(
                        stock_price,
                        lowest_buy_price)
                    self.logger.debug(debug_msg)
                    return
                if amount > lowest_buy_price_quantity:
                    amount = lowest_buy_price_quantity
                commission_id = self.trade.sell_stock(
                    stock_symbol,
                    stock_price,
                    amount)
                time.sleep(3)
                commission_state = self.trade.get_commission_state(
                    commission_id)
                if commission_state != "已成":
                    result = self.trade.cancel_commission(commission_id)
                    if result != 1:
                        commission_state = self.trade.get_commission_state(
                            commission_id)
                        if commission_state == "已成":
                            complete_sell_transaction(stock_symbol,
                                                      stock_price,
                                                      amount)
                        else:
                            print("Unknown error in canceling transaction")
                            self.logger.debug(
                                "Unknown error in canceling transaction.")
                else:
                    complete_sell_transaction(stock_symbol,
                                              stock_price,
                                              amount)
            else:
                print("Error!")

        return
