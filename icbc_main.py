'''
Created on 2016年1月18日

@author: Wenwen
'''
from icbc.trade import Trade
from icbc.processor import NobalMetalProcessor
import logging
import configparser
import time

# read configuration
config = configparser.ConfigParser()
config.read("gtja_trade.ini", encoding="utf-8")
account_name = config['Account'].get('account_name')
password = config['Account'].get('password')
connection_string = config['Database'].get('connection')
logging_filename = "icbc.log"

# logger setup
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(logging_filename, encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


if __name__ == '__main__':
    nobal_metal_processor = NobalMetalProcessor()
    nobal_metal_processor.login()

    nobal_metal_processor.close()
    
    
    #trade = Trade()
    #trade.login()
    #trade.select_noble_metal()
    #t = trade.buy_noble_metal("人民币账户白银", 1, 3)
    #print(t)
    #trade.select_noble_metal()
    #t = trade.sell_noble_metal("人民币账户白银", 1, 2)
    #print(t)
    
    #nobal_metal_price = trade.get_nobal_metal_price("人民币账户白银")
    #print(nobal_metal_price)
    #time.sleep(10)
    #trade.close()