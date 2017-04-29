'''
    stock.py
'''
import configparser
import logging
from stock_gui.stock_app import StockApp
import stock_db.db_connection


def main():
    '''
        main module
    '''
    config = configparser.ConfigParser()
    config.read("stock.ini", encoding="utf-8")
    connection_string = config['Database'].get('connection')
    stock_db.db_connection.default_connection_string = connection_string

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    file_handler = logging.FileHandler('stock.log', encoding="utf-8")
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


    logging.info("App started.")
    stock_app = StockApp()
    stock_app.mainloop()


if __name__ == "__main__":
    main()
