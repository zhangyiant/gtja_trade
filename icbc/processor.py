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
        self.trade.select_noble_metal()

        noble_metal_price = self.trade.\
                            get_noble_metal_price(noble_metal_name)
        print("price: {0}".format(noble_metal_price))

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
        if (buy_or_sell is not None) and (buy_or_sell == "Buy"):
            amount = algorithm.get_suggested_amount()
            print("buy {0}, price: {1}, amount: {2}".\
                  format(noble_metal_name, buy_price, amount))
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
        if (buy_or_sell is not None) and (buy_or_sell == "Sell"):
            lowest_price = StockTransaction.\
                           get_lowest_buy_price(noble_metal_name)
            if sell_price - lowest_price < 0.04:
                return
            amount = algorithm.get_suggested_amount()
            quantity = StockTransaction.\
                       get_lowest_buy_price_quantity(noble_metal_name)
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
