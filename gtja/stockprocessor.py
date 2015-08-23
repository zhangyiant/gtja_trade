'''
Created on 2015年8月24日

@author: Yi Zhang
'''
from stock_db.db_stock import StockCashTable
from stock_db.db_stock import StockCash
from gtja.Trade import Trade

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
        
        return
        
    