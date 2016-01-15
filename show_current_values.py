'''
Created on Jul 8, 2015

@author: Yi Zhang
'''
from gtja.stockprocessor import StockProcessor

import time
import datetime
import configparser
import stock_db


# read configuration
config = configparser.ConfigParser()
config.read("gtja_trade.ini", encoding="utf-8")
account_name = config['Account'].get('account_name')
password = config['Account'].get('password')
connection_string = config['Database'].get('connection')

# set the DB connection string
stock_db.db_connection.default_connection_string = connection_string

#commission_id = trade.get_last_commission_id("601398", 100)

stock_processor = StockProcessor(account_name, password)
print(account_name, password)
 
#stock_processor.login()
 
#time.sleep(3)

symbol_list = ['600115']

stock_processor.set_stock_symbol_list(["600115"])

for symbol in symbol_list:
    total = stock_processor.get_stock_current_value(symbol)
    print("Stock symbol: {0}\t\tTotal Value: {1}".format(symbol, total))

stock_processor.close()

# another testqq
