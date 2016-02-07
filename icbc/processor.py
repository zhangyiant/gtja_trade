'''
Created on 2016年1月24日

@author: Wenwen
'''
from .trade import Trade

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
        print("process {0}".format(nobal_metal_name))
        self.trade.select_noble_metal()
        nobal_metal_price = self.trade.get_nobal_metal_price(nobal_metal_name)
        print("price: {0}".format(nobal_metal_price))
        
        # how many to buy or sell for this nobal metal
        # Todo:
        
        # Buy or sell them
        # Todo:

        return