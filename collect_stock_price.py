'''
Created on Jul 21, 2017

@author: Yi Zhang
'''
import time
import datetime
import configparser
import logging
import logging.config

from icbc.settings import LOGGING

import stock_db.db_connection

from anteestudio.stock import StockPriceCollector
from anteestudio.trade.keep_alive import update_keep_alive


APP_NAME = "collect_stock_price"

# read configuration
CONFIG_PARSER = configparser.ConfigParser()
CONFIG_PARSER.read("gtja_trade.ini", encoding="utf-8")
CONNECTION_STRING = CONFIG_PARSER['Database'].get('connection')

logging.config.dictConfig(LOGGING)

# set the DB connection string
stock_db.db_connection.default_connection_string = CONNECTION_STRING

LOGGER = logging.getLogger(__name__)

collector = StockPriceCollector()


def is_transaction_time():
    time_now = datetime.datetime.now()
    weekday = time_now.weekday()
    if weekday > 4:
        return False
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


stock_list = ["000568", "002367", "600019",
              "600115", "600584", "601111",
              "601390", "601398", "601857",
              "601998"]
while True:
    if is_transaction_time():
        LOGGER.debug("Collect")
        for stock in stock_list:
            LOGGER.debug("Collect stock {0}".format(stock))
            try:
                collector.collect(stock)
            except Exception as e:
                LOGGER.error("Error: {0}".format(e))
    else:
        LOGGER.debug("Not in transaction time")
    time.sleep(30)

    update_keep_alive(app_name=APP_NAME)

collector.close()
