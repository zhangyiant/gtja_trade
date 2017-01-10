'''
Created on 2016年1月18日

@author: Wenwen
'''
import logging
import configparser
import time
from icbc.trade import Trade
from icbc.processor import NobleMetalProcessor
import stock_db

# Monday 7:00 - Saturday 4:00
# read configuration
config = configparser.ConfigParser()
config.read("gtja_trade.ini", encoding="utf-8")
account_name = config['Account'].get('account_name')
password = config['Account'].get('password')
CONNECTION_STRING = config['Database'].get('connection')
logging_filename = config['Logging'].get('filename')

# logger setup
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(logging_filename, encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

stock_db.db_connection.default_connection_string = CONNECTION_STRING

if __name__ == '__main__':
    noble_metal_processor = NobleMetalProcessor()
    noble_metal_processor.set_noble_metal_name_list(
        ["人民币账户白银",
         "人民币账户黄金",
         "人民币账户钯金",
         "人民币账户铂金",
         "美元账户白银"])
    noble_metal_processor.login()
    t = 10
    while True:
        noble_metal_name = noble_metal_processor.get_one_noble_metal()
        noble_metal_processor.process_noble_metal(noble_metal_name)

    noble_metal_processor.close()
    
    
    #trade = Trade()
    #trade.login()
    #trade.select_noble_metal()
    #t = trade.buy_noble_metal("人民币账户白银", 1, 3)
    #print(t)
    #trade.select_noble_metal()
    #t = trade.sell_noble_metal("人民币账户白银", 1, 2)
    #print(t)
    
    #noble_metal_price = trade.get_noble_metal_price("人民币账户白银")
    #print(noble_metal_price)
    #time.sleep(10)
    #trade.close()
