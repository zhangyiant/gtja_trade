'''
Created on Jul 8, 2015

@author: Yi Zhang
'''
import time
import datetime
import configparser
import logging
import logging.config

from gtja.settings import LOGGING
from gtja.stockprocessor import StockProcessor

import stock_db

# read configuration
CONFIG_PARSER = configparser.ConfigParser()
CONFIG_PARSER.read("gtja_trade.ini", encoding="utf-8")
ACCOUNT_NAME = CONFIG_PARSER['Account'].get('account_name')
PASSWORD = CONFIG_PARSER['Account'].get('password')
CONNECTION_STRING = CONFIG_PARSER['Database'].get('connection')
LOGGING_PATH = CONFIG_PARSER["Logging"].get("path")

logging.config.dictConfig(LOGGING)

# logger setup
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
logging.getLogger(
    'selenium.webdriver.remote.remote_connection').setLevel(
        logging.WARNING)

# set the DB connection string
stock_db.db_connection.default_connection_string = CONNECTION_STRING


STOCK_PROCESSOR = StockProcessor(ACCOUNT_NAME, PASSWORD)
logging.info("account: " + ACCOUNT_NAME)
logging.info("password: " + PASSWORD)

STOCK_PROCESSOR.login()

time.sleep(3)

STOCK_PROCESSOR.set_stock_symbol_list(
    ["600115", "601390", "600584", "000568", "601998",
     "002367", "601111", "601398", "600019", "601857"])

def is_transaction_time():
    '''
        is_transaction_time
    '''
    time_now = datetime.datetime.now()
    time_1 = time_now.time()
    time_2 = datetime.time(9, 30, 0)
    time_3 = datetime.time(11, 30, 0)
    time_4 = datetime.time(13, 0, 0)
    time_5 = datetime.time(15, 0, 0)
    if time_1 < time_2:
        return False
    if time_1 >= time_2 and time_1 <= time_3:
        return True
    if time_1 > time_3 and time_1 < time_4:
        return False
    if time_1 >= time_4 and time_1 <= time_5:
        return True
    if time_1 > time_5:
        return False

def is_market_closed():
    '''
        is_market_close
    '''
    time_now = datetime.datetime.now()
    time_1 = time_now.time()
    time_2 = datetime.time(15, 0, 0)

    return bool(time_1 > time_2)

while True:

    T = datetime.datetime.now()
    logging.debug(T)

    # check time
    if is_market_closed():
        logging.info("market is closed!")
        break

    if not is_transaction_time():
        logging.info("It's not transaction time now!")
        STOCK_PROCESSOR.keep_alive()
        time.sleep(60)
        continue

    STOCK_SYMBOL = STOCK_PROCESSOR.get_one_stock()
    STOCK_PROCESSOR.process_stock(STOCK_SYMBOL)
    time.sleep(59)

STOCK_PROCESSOR.close()
