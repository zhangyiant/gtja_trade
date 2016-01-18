'''
Created on 2016年1月18日

@author: Wenwen
'''
from icbc.trade import Trade
import logging
import configparser

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
    trade = Trade()
    trade.login()