import configparser
import logging
import logging.config
from gtja.settings import LOGGING
logging.config.dictConfig(LOGGING)

import sys
from gtja.stockprocessor import StockProcessor
from gtja.utility import complete_sell_transaction;

import stock_db

STOCK_SYMBOL = sys.argv[1]
SELL_PRICE = float(sys.argv[2])
QUANTITY = int(sys.argv[3])

# read configuration
CONFIG_PARSER = configparser.ConfigParser()
CONFIG_PARSER.read("gtja_trade.ini", encoding="utf-8")
CONNECTION_STRING = CONFIG_PARSER['Database'].get('connection')

# set the DB connection string
stock_db.db_connection.default_connection_string = CONNECTION_STRING

print(STOCK_SYMBOL)
print(SELL_PRICE)
print(QUANTITY)
complete_sell_transaction(STOCK_SYMBOL, SELL_PRICE, QUANTITY)
