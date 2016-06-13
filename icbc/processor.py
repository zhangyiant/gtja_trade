'''
Created on 2016年1月24日

@author: Wenwen
'''
from .trade import Trade
from stock_db.db_stock import \
    StockCashTable, \
    StockTransaction, \
    StockTransactionTable, \
    StockPriceRangeTable
from stock_holding_algorithm.simple_algorithm2 import SimpleAlgorithm
from .utility import \
    complete_buy_transaction, \
    complete_sell_transaction

class NobalMetalProcessor:
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.trade = Trade()
        self.process_index = 0
        return

    def login(self):
        self.trade.login()
        return

    def close(self):
        self.trade.close()
        return

    def set_nobal_metal_name_list(self, nobal_metal_name_list):
        self.nobal_metal_name_list = nobal_metal_name_list
        return

    def get_nobal_metal_name_list(self):
        return self.nobal_metal_name_list

    def get_one_nobal_metal(self):
        nobal_metal_name = self.nobal_metal_name_list[self.process_index]
        self.process_index = (self.process_index + 1) % \
                                 (len(self.nobal_metal_name_list))
        return nobal_metal_name

    def process_nobal_metal(self, nobal_metal_name):
        '''
            process the nobal metal
        '''
        print("process {0}".format(nobal_metal_name))
        self.trade.select_noble_metal()
        nobal_metal_price = self.trade.get_nobal_metal_price(nobal_metal_name)
        print("price: {0}".format(nobal_metal_price))

        stock_price_range_table = StockPriceRangeTable()
        stock_price_range = \
            stock_price_range_table.\
            get_stock_stock_price_range_by_symbol(nobal_metal_name)
        price_low = stock_price_range.get_price_low()
        price_high = stock_price_range.get_price_high()

        stock_cash_table = StockCashTable()
        nobal_metal_cash = stock_cash_table.\
                           get_stock_cash_by_symbol(nobal_metal_name)
        owned_quantity = StockTransaction.\
                         get_owned_quantity(nobal_metal_name)

        # buy
        buy_price = nobal_metal_price.selling_price
        algorithm = SimpleAlgorithm(symbol=nobal_metal_name,
                                    start_price=price_low  ,
                                    stop_price=price_high,
                                    current_price=buy_price)

        algorithm.calculate()

        buy_or_sell = algorithm.get_suggested_buy_or_sell()
        if (buy_or_sell is not None) and (buy_or_sell == "Buy"):
            amount = algorithm.get_suggested_amount()
            print("buy {0}, price: {1}, amount: {2}".\
                  format(nobal_metal_name, buy_price, amount))
            result = self.trade.buy_noble_metal(nobal_metal_name,
                                                amount,
                                                buy_price)
            print(result)
            if result:
                print("update db")
                complete_buy_transaction(nobal_metal_name,
                                         buy_price,
                                         amount)
            return

        # sell
        sell_price = nobal_metal_price.buying_price
        alogrithm = SimpleAlgorithm(symbol=nobal_metal_name,
                                    start_price=price_low  ,
                                    stop_price=price_high,
                                    current_price=sell_price)

        alogrithm.calculate()

        buy_or_sell = algorithm.get_suggested_buy_or_sell()
        if (buy_or_sell is not None) and (buy_or_sell == "Sell"):
            lowest_price = StockTransaction.\
                           get_lowest_buy_price(nobal_metal_name)
            if sell_price - lowest_price < 0.1:
                return
            amount = algorithm.get_suggested_amount()
            quantity = StockTransaction.\
                       get_lowest_buy_price_quantity(nobal_metal_name)
            if amount >= quantity:
                amount = quantity

            print("sell {0}, price: {1}, amount: {2}".\
                  format(nobal_metal_name, sell_price, amount))
            result = self.trade.sell_noble_metal(nobal_metal_name,
                                                 amount,
                                                 sell_price)
            if result:
                complete_sell_transaction(nobal_metal_name,
                                          sell_price,
                                          amount)
            return

        return
