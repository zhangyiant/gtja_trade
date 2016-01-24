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
        return
    
    def login(self):
        self.trade.login()
        return
    
    def close(self):
        self.trade.close()
        return
