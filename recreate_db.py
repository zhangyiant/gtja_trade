'''
Created on 2016年2月29日

@author: Wenwen
'''
from stock_db.db_utility import recreate_db
import stock_db
import configparser

if __name__ == '__main__':
    # read configuration
    config = configparser.ConfigParser()
    config.read("stock.ini", encoding="utf-8")
    connection_string = config['Database'].get('connection')
    
    # set the DB connection string
    stock_db.db_connection.default_connection_string = connection_string

    recreate_db()
