'''
    utility
'''
from datetime import datetime
from stock_db.db_stock import \
    StockCash, \
    StockTransaction, \
    StockClosedTransaction
from stock_db.db_connection import get_default_db_connection
from sqlalchemy import asc

def complete_buy_transaction(symbol, price, quantity, cash_offset, conn=None):
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

    stock_cash.amount = stock_cash.amount + cash_offset

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

def complete_sell_transaction(symbol, price, quantity, cash_offset, conn=None):
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

    stock_cash.amount = stock_cash.amount + cash_offset

    # get lowest buy transaction
    stock_transaction = session.query(StockTransaction).\
                        filter(StockTransaction.buy_or_sell ==
                               StockTransaction.BUY_FLAG).\
                               order_by(asc(StockTransaction.price)).\
                               first()
    if stock_transaction is None:
        session.close()
        raise Exception("Cannot find lowest buy price transaction")

    if stock_transaction.quantity < quantity:
        session.close()
        raise Exception("stock_transaction.quantity < quantity")

    if stock_transaction.price < price:
        session.close()
        raise Exception("stock_tranaction price < sell_price")

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
