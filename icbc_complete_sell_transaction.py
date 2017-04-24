import configparser
import logging
import sys
from icbc.utility import complete_sell_transaction

import stock_db


STOCK_SYMBOL = sys.argv[1]
SELL_PRICE = float(sys.argv[2])
QUANTITY = int(sys.argv[3])

# read configuration
CONFIG_PARSER = configparser.ConfigParser()
CONFIG_PARSER.read("gtja_trade.ini", encoding="utf-8")
ACCOUNT_NAME = CONFIG_PARSER['Account'].get('account_name')
PASSWORD = CONFIG_PARSER['Account'].get('password')
CONNECTION_STRING = CONFIG_PARSER['Database'].get('connection')
LOGGING_FILENAME = CONFIG_PARSER['Logging'].get('filename')

# logger setup
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.WARNING)
FH = logging.FileHandler(LOGGING_FILENAME, encoding="utf-8")
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
FH.setFormatter(FORMATTER)
LOGGER.addHandler(FH)

# set the DB connection string
stock_db.db_connection.default_connection_string = CONNECTION_STRING

print(STOCK_SYMBOL)
print(SELL_PRICE)
print(QUANTITY)
complete_sell_transaction(STOCK_SYMBOL, SELL_PRICE, QUANTITY)
