'''
Created on 2016年1月24日

@author: Wenwen
'''
import time
import logging
from selenium.common.exceptions import \
    StaleElementReferenceException, \
    WebDriverException
from .trade import Trade
from stock_db.db_stock import \
    StockTransaction, \
    StockPriceRangeTable, \
    StockLowestUnitTable
from stock_db.db_utility import \
    get_lowest_gain
from stock_holding_algorithm.simple_algorithm2 import SimpleAlgorithm
from .utility import \
    complete_buy_transaction, \
    complete_sell_transaction

class NobleMetalProcessorException(Exception):
    pass

class NobleMetalProcessor:
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.trade = Trade()
        self.process_index = 0
        self.error_counter = 0
        self.logger = logging.getLogger(__name__)
        return

    def login(self):
        self.trade.login()
        return

    def close(self):
        self.trade.close()
        return

    def set_noble_metal_name_list(self, noble_metal_name_list):
        self.noble_metal_name_list = noble_metal_name_list
        return

    def get_noble_metal_name_list(self):
        return self.noble_metal_name_list

    def get_one_noble_metal(self):
        noble_metal_name = self.noble_metal_name_list[self.process_index]
        self.process_index = (self.process_index + 1) % \
                                 (len(self.noble_metal_name_list))
        return noble_metal_name

    def process_noble_metal(self, noble_metal_name):
        '''
            process the noble metal
        '''

        print("process {0}".format(noble_metal_name))

        try:
            self.trade.main_page()
            self.trade.select_noble_metal()
        except StaleElementReferenceException as stale_exception:
            error_msg = "select noble metal error. " + \
                        "StaleElementReferenceException{0}"
            self.logger.error(error_msg)
            print(error_msg.format(stale_exception))
            self.error_counter += 1
            if self.error_counter > 10:
                raise NobleMetalProcessorException("Stale Element Exception")
            time.sleep(10)
            return
        except WebDriverException as web_driver_exception:
            error_msg = "select noble metal error." + \
                        "WebDriverException{0}"
            error_msg = error_msg.format(web_driver_exception)
            self.logger.error(error_msg)
            print(error_msg)
            self.error_counter += 1
            if self.error_counter > 10:
                raise NobleMetalProcessorException("WebDriver Exception")
            time.sleep(10)
            return
        except Exception as exc:
            error_msg = "Exception {0}"
            error_msg = error_msg.format(exc)
            self.logger.error(error_msg)
            print(error_msg)
            self.error_counter += 1
            if self.error_counter > 10:
                raise NobleMetalProcessorException("Unknown Exception")
            time.sleep(10)
            return

        # reset counter
        self.error_counter = 0

        try:
            noble_metal_price = self.trade.\
                                get_noble_metal_price(noble_metal_name)
            print("price: {0}".format(noble_metal_price))
        except Exception as exception:
            self.logger.debug("get price exception")
            print("get price exception: {0}".format(exception))
            return

        stock_price_range_table = StockPriceRangeTable()
        stock_price_range = \
                            stock_price_range_table.\
                            get_stock_stock_price_range_by_symbol(
                                noble_metal_name)
        price_low = stock_price_range.get_price_low()
        price_high = stock_price_range.get_price_high()

        # buy
        buy_price = noble_metal_price.selling_price
        algorithm = SimpleAlgorithm(symbol=noble_metal_name,
                                    start_price=price_low,
                                    stop_price=price_high,
                                    current_price=buy_price)

        algorithm.calculate()

        buy_or_sell = algorithm.get_suggested_buy_or_sell()
        print("Buy_or_sell: {0}".format(buy_or_sell))
        if (buy_or_sell is not None) and (buy_or_sell == "Buy"):
            suggested_amount = algorithm.get_suggested_amount()
            print("buy {0}, price: {1}, suggested_amount: {2}".\
                  format(noble_metal_name, buy_price, suggested_amount))

            stock_lowest_unit_table = StockLowestUnitTable()
            stock_lowest_unit = stock_lowest_unit_table.\
                                get_lowest_unit(noble_metal_name)
            if stock_lowest_unit is not None:
                lowest_unit = stock_lowest_unit.lowest_unit
                is_integer = stock_lowest_unit.is_integer
            else:
                lowest_unit = 1
                is_integer = True

            if is_integer:
                amount = int(suggested_amount / lowest_unit) * int(lowest_unit)
            else:
                amount = int(suggested_amount / lowest_unit) * lowest_unit

            print(amount)
            if amount < lowest_unit:
                return

            result = self.trade.buy_noble_metal(noble_metal_name,
                                                amount,
                                                buy_price)
            print(result)
            if result:
                print("update db")
                complete_buy_transaction(noble_metal_name,
                                         buy_price,
                                         amount)
            return

        # sell
        sell_price = noble_metal_price.buying_price
        algorithm = SimpleAlgorithm(symbol=noble_metal_name,
                                    start_price=price_low  ,
                                    stop_price=price_high,
                                    current_price=sell_price)

        algorithm.calculate()

        buy_or_sell = algorithm.get_suggested_buy_or_sell()
        print("Buy_or_sell: {0}".format(buy_or_sell))
        if (buy_or_sell is not None) and (buy_or_sell == "Sell"):
            lowest_price = StockTransaction.\
                           get_lowest_buy_price(noble_metal_name)
            lowest_gain = get_lowest_gain(noble_metal_name)
            if lowest_gain is None:
                lowest_gain = 0.04
            print(lowest_gain)
            if sell_price - lowest_price < lowest_gain:
                return
            suggested_amount = algorithm.get_suggested_amount()

            stock_lowest_unit_table = StockLowestUnitTable()
            stock_lowest_unit = stock_lowest_unit_table.\
                                get_lowest_unit(noble_metal_name)
            if stock_lowest_unit is not None:
                lowest_unit = stock_lowest_unit.lowest_unit
                is_integer = stock_lowest_unit.is_integer
            else:
                lowest_unit = 1
                is_integer = True
            if is_integer:
                amount = int(suggested_amount / lowest_unit) * int(lowest_unit)
            else:
                amount = int(suggested_amount / lowest_unit) * lowest_unit

            print(suggested_amount)
            print(amount)
            quantity = StockTransaction.\
                       get_lowest_buy_price_quantity(noble_metal_name)
            if amount < lowest_unit:
                return
            if amount >= quantity:
                amount = quantity

            print("sell {0}, price: {1}, amount: {2}".\
                  format(noble_metal_name, sell_price, amount))
            result = self.trade.sell_noble_metal(noble_metal_name,
                                                 amount,
                                                 sell_price)
            print(result)
            if result:
                complete_sell_transaction(noble_metal_name,
                                          sell_price,
                                          amount)
            return

        return
