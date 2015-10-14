'''
Created on Jul 8, 2015

@author: Yi Zhang
'''
from gtja.stockprocessor import StockProcessor

import time
import datetime
import configparser
import stock_db.db_connection
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.ERROR)
fh = logging.FileHandler('stock.log', encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

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
 
stock_processor.login()
 
time.sleep(3)

stock_processor.set_stock_symbol_list(["601398", "601857"])

def is_transaction_time():
    td = datetime.datetime.now()
    t1 = td.time()
    t2 = datetime.time(9,0,0)
    t3 = datetime.time(11,30,0)
    t4 = datetime.time(13,0,0)
    t5= datetime.time(15,0,0)
    if (t1 < t2):
        return False
    if (t1>=t2 and t1<=t3):
        return True
    if (t1>t3 and t1 < t4):
        return False
    if (t1>=t4 and t1 <= t5):
        return True
    if (t1>t5):
        return False
    
def is_market_closed():
    td = datetime.datetime.now()
    t1 = td.time()
    t2 = datetime.time(15,0,0)
    if (t1 > t2):
        return True
    else:
        return False

while True:
    # check time
    if (is_market_closed()):
        print("market is closed!")
        break
    
    if (not is_transaction_time()):
        print("It's not transaction time now!")
        time.sleep(180)
        continue
    
    stock_symbol = stock_processor.get_one_stock()
    stock_processor.process_stock(stock_symbol)

#    commission_id = stock_processor.trade.buy_stock("601398", 4.20, 100)
#    stock_processor.trade.cancel_commission(216527)
#    print(commission_id)

#commission_id = trade.sell_stock("601398", 5.12, 200)


stock_processor.close()
