'''
Created on 2016年1月17日

@author: Wenwen
'''
import logging

class Trade:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        print("constructor")
        self.logger = logging.getLogger(__name__)
        return
    
    
    def login(self):
        print("login")
        self.logger.info("login")
        return

if __name__ == '__main__':
    pass
    