'''
    Stock Table DB operation testing
'''
import unittest
import configparser
from datetime import date, datetime
import stock_db
from stock_db.db_stock import StockClosedTransaction, \
                              StockClosedTransactionTable, \
                              StockTransaction, \
                              StockTransactionTable
from stock_db.db_utility import reset_table
from stock_db.db_connection import get_default_db_connection

class StockClosedTransactionTableTest(unittest.TestCase):
    '''
        StockClosedTransactionTableTest class
    '''
    def setUp(self):
        config = configparser.ConfigParser()
        config.read("gtja_trade.ini", encoding="utf-8")
        connection_string = config['Database'].get('test_connection')
        stock_db.db_connection.default_connection_string = connection_string
        return

    def test_stock_closed_transaction_sanity(self):
        '''
            test_stock_closed_transaction_sanity()
        '''
        stock_db_connection = get_default_db_connection()
        reset_table(stock_db_connection)
        transaction_table = StockClosedTransactionTable(stock_db_connection)
        # new a stock closed transaction
        stock_closed_transaction = StockClosedTransaction()
        stock_closed_transaction.symbol = "601398"
        stock_closed_transaction.buy_price = 4.51
        stock_closed_transaction.sell_price = 4.61
        stock_closed_transaction.buy_date = datetime(2015, 11, 10, 0, 0, 0)
        stock_closed_transaction.sell_date = datetime(2015, 12, 30, 0, 0, 0)
        stock_closed_transaction.quantity = 200
        transaction_table.add_stock_closed_transaction(
                                                  stock_closed_transaction)

        # query and compare
        stock_closed_transaction_list = \
                transaction_table.get_all_stock_closed_transaction()
        self.assertEqual(len(stock_closed_transaction_list),
                         1,
                         "There should be only 1 item")
        stock_closed_transaction = stock_closed_transaction_list[0]
        self.assertEqual(stock_closed_transaction.symbol,
                         "601398")
        self.assertEqual(stock_closed_transaction.buy_price,
                         4.51)
        self.assertEqual(stock_closed_transaction.sell_price,
                         4.61)
        self.assertEqual(stock_closed_transaction.buy_date,
                         datetime(2015, 11, 10, 0, 0, 0))
        self.assertEqual(stock_closed_transaction.sell_date,
                         datetime(2015, 12, 30, 0, 0, 0))
        self.assertEqual(stock_closed_transaction.quantity,
                         200)

        # delete the newly created item
        transaction_table.delete_stock_closed_transaction(
            stock_closed_transaction)
        stock_closed_transaction_list = \
                transaction_table.get_all_stock_closed_transaction()
        self.assertEqual(len(stock_closed_transaction_list),
                         0,
                         "The list should be an empty list")

        return

    def test_close_stock_transaction(self):
        '''
            test_close_stock_transaction
        '''
        stock_db_connection = get_default_db_connection()
        reset_table(stock_db_connection)
        stock_transaction_table = StockTransactionTable(stock_db_connection)


        # init transaction 1
        stock_transaction_1 = StockTransaction()
        stock_transaction_1.symbol = "601398"
        stock_transaction_1.buy_or_sell = StockTransaction.BUY_FLAG
        stock_transaction_1.date = datetime(2016, 5, 15, 0, 0, 0)
        stock_transaction_1.quantity = 200
        stock_transaction_1.price = 4.51
        stock_transaction_table.add_stock_transaction(stock_transaction_1)
        trans_id_1 = stock_transaction_1.trans_id

        # init transaction 2
        stock_transaction_2 = StockTransaction()
        stock_transaction_2.symbol = "601398"
        stock_transaction_2.buy_or_sell = StockTransaction.SELL_FLAG
        stock_transaction_2.date = datetime(2016, 5, 16, 0, 0, 0)
        stock_transaction_2.quantity = 200
        stock_transaction_2.price = 4.81
        stock_transaction_table.add_stock_transaction(stock_transaction_2)
        trans_id_2 = stock_transaction_2.trans_id

        stock_closed_transaction = \
            StockClosedTransactionTable.close_transaction(stock_transaction_1,
                                                          stock_transaction_2)

        self.assertEqual(stock_closed_transaction.symbol,
                         "601398")
        self.assertEqual(stock_closed_transaction.buy_price,
                         4.51)
        self.assertEqual(stock_closed_transaction.sell_price,
                         4.81)
        self.assertEqual(stock_closed_transaction.buy_date,
                         datetime(2016, 5, 15, 0, 0, 0))
        self.assertEqual(stock_closed_transaction.sell_date,
                         datetime(2016, 5, 16, 0, 0, 0))
        self.assertEqual(stock_closed_transaction.quantity,
                         200)

        stock_transaction = \
            stock_transaction_table.get_stock_transaction_by_trans_id(
                trans_id_1)
        self.assertIsNone(stock_transaction,
                          "stock_transaction_1 is not deleted")
        stock_transaction = \
            stock_transaction_table.get_stock_transaction_by_trans_id(
                trans_id_2)
        self.assertIsNone(stock_transaction,
                          "stock_transaction_2 is not deleted")

        return

    def test_owned_transaction(self):
        '''
            test_owned_transaction
        '''
        stock_db_connection = get_default_db_connection()
        reset_table(stock_db_connection)
        stock_transaction_table = StockTransactionTable(stock_db_connection)

        # init transaction 1
        stock_transaction_1 = StockTransaction()
        stock_transaction_1.symbol = "601398"
        stock_transaction_1.buy_or_sell = StockTransaction.BUY_FLAG
        stock_transaction_1.date = date(2016, 5, 15)
        stock_transaction_1.quantity = 200
        stock_transaction_1.price = 4.51
        stock_transaction_table.add_stock_transaction(stock_transaction_1)
        trans_id_1 = stock_transaction_1.trans_id

        # init transaction 2
        stock_transaction_2 = StockTransaction()
        stock_transaction_2.symbol = "601398"
        stock_transaction_2.buy_or_sell = StockTransaction.SELL_FLAG
        stock_transaction_2.date = date(2016, 5, 16)
        stock_transaction_2.quantity = 100
        stock_transaction_2.price = 4.81
        stock_transaction_table.add_stock_transaction(stock_transaction_2)
        trans_id_2 = stock_transaction_2.trans_id

        owned_quantity = StockTransaction.get_owned_quantity("601398")
        self.assertEqual(owned_quantity,
                         100)

        return

    def test_lowest_buy_price(self):
        '''
            test lowest buy price
        '''
        stock_db_connection = get_default_db_connection()
        reset_table(stock_db_connection)
        stock_transaction_table = StockTransactionTable(stock_db_connection)

        # init transaction 1
        stock_transaction_1 = StockTransaction()
        stock_transaction_1.symbol = "601398"
        stock_transaction_1.buy_or_sell = StockTransaction.BUY_FLAG
        stock_transaction_1.date = date(2016, 5, 15)
        stock_transaction_1.quantity = 200
        stock_transaction_1.price = 4.9
        stock_transaction_table.add_stock_transaction(stock_transaction_1)
        trans_id_1 = stock_transaction_1.trans_id

        # init transaction 2
        stock_transaction_2 = StockTransaction()
        stock_transaction_2.symbol = "601398"
        stock_transaction_2.buy_or_sell = StockTransaction.BUY_FLAG
        stock_transaction_2.date = date(2016, 5, 16)
        stock_transaction_2.quantity = 100
        stock_transaction_2.price = 4.81
        stock_transaction_table.add_stock_transaction(stock_transaction_2)
        trans_id_2 = stock_transaction_2.trans_id

        lowest_price = StockTransaction.get_lowest_buy_price("601398")
        self.assertEqual(lowest_price, 4.81)

        return

    def test_lowest_buy_price2(self):
        '''
            test lowest buy price
        '''
        stock_db_connection = get_default_db_connection()
        reset_table(stock_db_connection)
        stock_transaction_table = StockTransactionTable(stock_db_connection)

        lowest_price = StockTransaction.get_lowest_buy_price("601398")
        self.assertEqual(lowest_price, 9999.00)

        return

    def test_lowest_buy_price3(self):
        '''
            test lowest buy price with sell transaction
        '''
        stock_db_connection = get_default_db_connection()
        reset_table(stock_db_connection)
        stock_transaction_table = StockTransactionTable(stock_db_connection)

        # init transaction 1
        stock_transaction_1 = StockTransaction()
        stock_transaction_1.symbol = "601398"
        stock_transaction_1.buy_or_sell = StockTransaction.BUY_FLAG
        stock_transaction_1.date = date(2016, 5, 15)
        stock_transaction_1.quantity = 200
        stock_transaction_1.price = 4.51
        stock_transaction_table.add_stock_transaction(stock_transaction_1)
        trans_id_1 = stock_transaction_1.trans_id

        # init transaction 2
        stock_transaction_2 = StockTransaction()
        stock_transaction_2.symbol = "601398"
        stock_transaction_2.buy_or_sell = StockTransaction.SELL_FLAG
        stock_transaction_2.date = date(2016, 5, 16)
        stock_transaction_2.quantity = 100
        stock_transaction_2.price = 4.81
        stock_transaction_table.add_stock_transaction(stock_transaction_2)
        trans_id_2 = stock_transaction_2.trans_id

        with self.assertRaises(Exception):
            lowest_price = StockTransaction.get_lowest_buy_price("601398")

        return

    def test_lowest_buy_price_quantity(self):
        '''
            test lowest buy price quantity
        '''
        stock_db_connection = get_default_db_connection()
        reset_table(stock_db_connection)
        stock_transaction_table = StockTransactionTable(stock_db_connection)

        # init transaction 1
        stock_transaction_1 = StockTransaction()
        stock_transaction_1.symbol = "601398"
        stock_transaction_1.buy_or_sell = StockTransaction.BUY_FLAG
        stock_transaction_1.date = date(2016, 5, 15)
        stock_transaction_1.quantity = 200
        stock_transaction_1.price = 4.9
        stock_transaction_table.add_stock_transaction(stock_transaction_1)
        trans_id_1 = stock_transaction_1.trans_id

        # init transaction 2
        stock_transaction_2 = StockTransaction()
        stock_transaction_2.symbol = "601398"
        stock_transaction_2.buy_or_sell = StockTransaction.BUY_FLAG
        stock_transaction_2.date = date(2016, 5, 16)
        stock_transaction_2.quantity = 100
        stock_transaction_2.price = 4.81
        stock_transaction_table.add_stock_transaction(stock_transaction_2)
        trans_id_2 = stock_transaction_2.trans_id

        quantity = StockTransaction.get_lowest_buy_price_quantity("601398")
        self.assertEqual(quantity, 100)

        return

    def test_lowest_buy_price_quantity2(self):
        '''
            test lowest buy price quantity
        '''
        stock_db_connection = get_default_db_connection()
        reset_table(stock_db_connection)
        stock_transaction_table = StockTransactionTable(stock_db_connection)

        quantity = StockTransaction.get_lowest_buy_price_quantity("601398")
        self.assertEqual(quantity, 0)

        return

    def test_lowest_buy_price_quantity3(self):
        '''
            test lowest buy price quantity with sell transaction
        '''
        stock_db_connection = get_default_db_connection()
        reset_table(stock_db_connection)
        stock_transaction_table = StockTransactionTable(stock_db_connection)

        # init transaction 1
        stock_transaction_1 = StockTransaction()
        stock_transaction_1.symbol = "601398"
        stock_transaction_1.buy_or_sell = StockTransaction.BUY_FLAG
        stock_transaction_1.date = date(2016, 5, 15)
        stock_transaction_1.quantity = 200
        stock_transaction_1.price = 4.51
        stock_transaction_table.add_stock_transaction(stock_transaction_1)
        trans_id_1 = stock_transaction_1.trans_id

        # init transaction 2
        stock_transaction_2 = StockTransaction()
        stock_transaction_2.symbol = "601398"
        stock_transaction_2.buy_or_sell = StockTransaction.SELL_FLAG
        stock_transaction_2.date = date(2016, 5, 16)
        stock_transaction_2.quantity = 100
        stock_transaction_2.price = 4.81
        stock_transaction_table.add_stock_transaction(stock_transaction_2)
        trans_id_2 = stock_transaction_2.trans_id

        with self.assertRaises(Exception):
            quantity = StockTransaction.get_lowest_buy_price_quantity("601398")

        return
