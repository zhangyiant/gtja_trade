import logging
import unittest
import configparser
import stock_db
from stock_db.db_stock import StockInfoTable
from stock_db.db_stock import StockCashTable
from stock_db.db_stock import StockCash
from stock_db.db_stock import StockTransaction
from stock_db.db_stock import StockTransactionTable
from stock_db.db_utility import reset_table
from stock_db.db_connection import get_default_db_connection
from datetime import date


class StockDbConnectionTest(unittest.TestCase):
    def setUp(self):
        config = configparser.ConfigParser()
        config.read("gtja_trade.ini", encoding="utf-8")
        connection_string = config['Database'].get('test_connection')
        stock_db.db_connection.default_connection_string = connection_string
        return

    def test_reset_table(self):
        # test
        logging.info("new StockDbConnection")
        stock_db_connection = get_default_db_connection()
        logging.info("reset table")
        reset_table(stock_db_connection)

        stock_info_table = StockInfoTable(stock_db_connection)
        stock_info_list = stock_info_table.get_all_stock_info()
        self.assertEqual(len(stock_info_list), 7)
        return

    def test_stock_cash_sanity(self):
        stock_db_connection = get_default_db_connection()
        reset_table(stock_db_connection)
        stock_cash_table = StockCashTable(stock_db_connection)
        stock_cash = StockCash("601398", 1000)
        stock_cash_table.add_stock_cash(stock_cash)

        # test the new created line
        stock_cash = stock_cash_table.get_stock_cash_by_symbol("601398")
        self.assertEqual(stock_cash.get_symbol(), "601398")
        self.assertEqual(stock_cash.get_amount(), 1000)

        # test update stock cash
        stock_cash.set_amount(23.456)
        stock_cash_table.update_stock_cash(stock_cash)
        stock_cash = stock_cash_table.get_stock_cash_by_symbol("601398")
        self.assertEqual(stock_cash.get_amount(), 23.456)

        # test an unavailable line
        stock_cash = stock_cash_table.get_stock_cash_by_symbol("XXXXXX")
        self.assertEqual(stock_cash, None)

        # insert a new line, and test get_all function
        stock_cash = StockCash("601857", 5000)
        stock_cash_table.add_stock_cash(stock_cash)
        stock_cash_list = stock_cash_table.get_all_stock_cash()
        self.assertEqual(len(stock_cash_list), 2)
        stock_cash = stock_cash_list[0]
        self.assertEqual(stock_cash.get_symbol(), "601398")
        self.assertEqual(stock_cash.get_amount(), 23.456)
        stock_cash = stock_cash_list[1]
        self.assertEqual(stock_cash.get_symbol(), "601857")
        self.assertEqual(stock_cash.get_amount(), 5000)

        # delete a line
        stock_cash = StockCash("601398", 0)
        stock_cash_table.delete_stock_cash(stock_cash)
        stock_cash = stock_cash_table.get_stock_cash_by_symbol("601398")
        self.assertEqual(stock_cash, None)

    def test_stock_transaction_sanity(self):
        stock_db_connection = get_default_db_connection()
        reset_table(stock_db_connection)
        stock_transaction_table = StockTransactionTable(stock_db_connection)
        stock_transaction = StockTransaction()
        stock_transaction.set_symbol("601398")
        stock_transaction.set_buy_or_sell("buy")
        stock_transaction.set_quantity(100)
        stock_transaction.set_price(4.51)
        stock_transaction.set_date(date(2015, 11, 10))
        stock_transaction_table.add_stock_transaction(stock_transaction)

        stock_transaction = StockTransaction()
        stock_transaction.set_symbol("601857")
        stock_transaction.set_buy_or_sell("buy")
        stock_transaction.set_quantity(100)
        stock_transaction.set_price(4.51)
        stock_transaction.set_date(date(2015, 11, 10))
        stock_transaction_table.add_stock_transaction(stock_transaction)

        stock_transaction = \
            stock_transaction_table.get_stock_transaction_by_trans_id(1)
        stock_transaction.set_quantity("500")
        stock_transaction_table.update_stock_transaction(stock_transaction)

        stock_transaction = \
            stock_transaction_table.get_stock_transaction_by_trans_id(1)
        stock_transaction_table.delete_stock_transaction(stock_transaction)

        return
