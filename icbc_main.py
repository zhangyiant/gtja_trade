'''
Created on 2016年1月18日

@author: Wenwen
'''
import logging
import logging.config
import configparser
import datetime
import time
from icbc.trade import Trade
from icbc.processor import NobleMetalProcessor
from icbc.settings import LOGGING
from anteestudio.trade.keep_alive import update_keep_alive

import stock_db

APP_NAME = "icbc_trade"

# Monday 7:00 - Saturday 4:00
# read configuration
config = configparser.ConfigParser()
config.read("gtja_trade.ini", encoding="utf-8")
account_name = config['Account'].get('account_name')
password = config['Account'].get('password')
CONNECTION_STRING = config['Database'].get('connection')
LOGGING_PATH = config["Logging"].get("path")

logging.config.dictConfig(LOGGING)

# logger setup
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

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
        update_keep_alive(app_name=APP_NAME)

    noble_metal_processor.close()
