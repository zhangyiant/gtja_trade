'''
    utility
'''
from datetime import datetime
import logging
from stock_db.db_stock import \
    StockCash, \
    StockTransaction, \
    StockClosedTransaction
from stock_db.db_connection import get_default_db_connection
from sqlalchemy import asc

LOGGER = logging.getLogger(__name__)

def is_shanghai_stock(symbol):
    if symbol[0] == "6":
        return True
    else:
        return False

def get_commission_fee(price, quantity):
    total = price * quantity * 0.0006
    result = round(total, 2)
    if result >= 5:
        return result
    else:
        return 5.0

def get_transfer_fee(price, quantity):
    total = price * quantity * 0.00002
    result = round(total, 2)
    return result

def get_tax_fee(price, quantity):
    total = price * quantity * 0.001
    result = round(total, 2)
    return result

def buy_fee(symbol, price, quantity):
    if is_shanghai_stock(symbol):
        result = get_commission_fee(price, quantity) + \
                 get_transfer_fee(price, quantity)
    else:
        result = get_commission_fee(price, quantity)
    return result

def sell_fee(symbol, price, quantity):
    if is_shanghai_stock(symbol):
        result = get_commission_fee(price, quantity) + \
                 get_tax_fee(price, quantity) + \
                 get_transfer_fee(price, quantity)
    else:
        result = get_commission_fee(price, quantity) + \
                 get_tax_fee(price, quantity)
    return result

def complete_buy_transaction(symbol, price, quantity, conn=None):
    '''
        update DB after buy transaction
    '''
    if conn is None:
        conn = get_default_db_connection()
    session = conn.get_sessionmake()()

    stock_cash = session.query(StockCash).\
                 filter(StockCash.symbol == symbol).\
                 one_or_none()
    if stock_cash is None:
        session.close()
        raise Exception("Save buy transaction failed")

    LOGGER.debug("Amount before: {0}".format(stock_cash.amount))
    stock_cash.amount = stock_cash.amount - \
                        price * quantity - \
                        buy_fee(symbol, price, quantity)
    LOGGER.debug("Amount after: {0}".format(stock_cash.amount))

    stock_transaction = StockTransaction()
    stock_transaction.symbol = symbol
    stock_transaction.buy_or_sell = "Buy"
    stock_transaction.quantity = quantity
    stock_transaction.price = price
    stock_transaction.date = datetime.now()

    session.add(stock_transaction)
    session.commit()

    session.close()
    return

def complete_sell_transaction(symbol, price, quantity, conn=None):
    '''
        update DB after sell transaction
    '''
    if conn is None:
        conn = get_default_db_connection()
    session = conn.get_sessionmake()()

    stock_cash = session.query(StockCash).\
                 filter(StockCash.symbol == symbol).\
                 one_or_none()
    if stock_cash is None:
        session.close()
        raise Exception("Save sell transaction failed")

    LOGGER.debug("Amount before: {0}".format(stock_cash.amount))
    stock_cash.amount = stock_cash.amount + \
                        price * quantity - \
                        sell_fee(symbol, price, quantity)
    LOGGER.debug("Amount after: {0}".format(stock_cash.amount))

    # get lowest buy transaction
    stock_transaction = session.query(StockTransaction).\
                        filter(StockTransaction.buy_or_sell ==
                               StockTransaction.BUY_FLAG).\
                        filter(StockTransaction.symbol == symbol).\
                               order_by(asc(StockTransaction.price)).\
                               first()
    if stock_transaction is None:
        session.close()
        raise Exception("Cannot find lowest buy price transaction")

    if stock_transaction.quantity < quantity:
        session.close()
        raise Exception("stock_transaction.quantity < quantity")

    if stock_transaction.price > price:
        session.close()
        raise Exception("stock_tranaction price > sell_price")

    stock_closed_transaction = StockClosedTransaction(
        symbol=symbol,
        quantity=quantity,
        buy_price=stock_transaction.price,
        buy_date=stock_transaction.date,
        sell_price=price,
        sell_date=datetime.now())
    session.add(stock_closed_transaction)

    if stock_transaction.quantity == quantity:
        session.delete(stock_transaction)
    else:
        stock_transaction.quantity = stock_transaction.quantity - quantity

    session.commit()

    session.close()
    return
