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

from icbc import NobleMetalPriceCollector

# read configuration
CONFIG_PARSER = configparser.ConfigParser()
CONFIG_PARSER.read("gtja_trade.ini", encoding="utf-8")
CONNECTION_STRING = CONFIG_PARSER['Database'].get('connection')

logging.config.dictConfig(LOGGING)

# set the DB connection string
stock_db.db_connection.default_connection_string = CONNECTION_STRING

LOGGER = logging.getLogger(__name__)

collector = NobleMetalPriceCollector()


def is_transaction_time():
    time_now = datetime.datetime.now()
    weekday = time_now.weekday()
    hour = time_now.hour
    if weekday > 0 and weekday < 5:
        return True
    elif weekday == 0:
        if hour >= 7:
            return True
        else:
            return False
    elif weekday == 5:
        if hour < 4:
            return True
        else:
            return False
    else:
        return False
    return False


while True:
    if is_transaction_time():
        LOGGER.debug("Collect")
        collector.collect()
        pass
    else:
        LOGGER.debug("Not in transaction time")
    time.sleep(30)

collector.close()
