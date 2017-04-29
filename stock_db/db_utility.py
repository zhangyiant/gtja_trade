'''
    db_utility module
'''
import logging
import csv

from sqlalchemy import desc
from sqlalchemy.orm.session import make_transient

from stock_db.db_connection import get_default_db_connection
from stock_db.db_stock import StockInfoTable,\
                              StockInfo,\
                              StockTransaction,\
                              StockClosedTransactionTable, \
                              StockLowestGain
import stock_db.db_stock

LOGGER = logging.getLogger(__name__)

def import_stock_info(conn=None):
    '''
        import_stock_info
    '''
    if conn is None:
        stock_info_table = StockInfoTable()
    else:
        stock_info_table = StockInfoTable(conn)

    with open("stock_info.csv", newline="", encoding="utf-8") as file_handler:
        reader = csv.reader(file_handler)
        for row in reader:
            stock_symbol = row[0]
            stock_name = row[1]
            stock_info = \
                stock_info_table.get_stock_info_by_symbol(stock_symbol)
            if stock_info != None:
                stock_info = \
                    StockInfo(stock_symbol, stock_name)
                stock_info_table.update_stock_info(stock_info)
            else:
                stock_info = \
                    StockInfo(stock_symbol, stock_name)
                stock_info_table.add_stock_info(stock_info)
    return

def reset_table(conn=None):
    '''
        reset_table
    '''
    if conn is None:
        db_connection = get_default_db_connection()
    else:
        db_connection = conn

    base = stock_db.db_stock.Base

    engine = db_connection.get_engine()

    base.metadata.drop_all(engine)
    base.metadata.create_all(engine)

    # import stock info from csv file
    import_stock_info()

    return

def recreate_db(conn=None):
    '''
        recreate_db
    '''
    if conn is None:
        db_connection = get_default_db_connection()
    else:
        db_connection = conn

    base = stock_db.db_stock.Base

    engine = db_connection.get_engine()

    base.metadata.create_all(engine)

    return

def split_transaction(conn = None):
    '''
        split_transaction
    '''
    if conn is None:
        db_connection = get_default_db_connection()
    else:
        db_connection = conn
    session = db_connection.create_session()

    query = session.query(StockTransaction).\
            filter(StockTransaction.quantity > 100)
    transactions = query.all()
    for transaction in transactions:
        quantity = transaction.quantity
        i = 100
        while i <= quantity:
            trans = StockTransaction()
            trans.buy_or_sell = transaction.buy_or_sell
            trans.date = transaction.date
            trans.price = transaction.price
            trans.symbol = transaction.symbol
            trans.quantity = 100
            session.add(trans)
            print("ADD")
            i = i + 100
        session.delete(transaction)
        session.commit()
        break
    session.close()
    return

def get_lowest_gain(symbol, conn=None):
    """
        Get lowest gain by symbol
    """
    if conn is None:
        db_connection = get_default_db_connection()
    else:
        db_connection = conn
    session = db_connection.create_session()

    stock_lowest_gain = session.query(StockLowestGain).\
            filter(StockLowestGain.symbol == symbol).\
            one_or_none()

    if stock_lowest_gain is None:
        lowest_gain = None
    else:
        lowest_gain = stock_lowest_gain.lowest_gain

    session.close()

    return lowest_gain

def clean_transaction_by_symbol(symbol, conn=None):
    '''
        clean_transaction_table_by_symbol
    '''
    if conn is None:
        db_connection = get_default_db_connection()
    else:
        db_connection = conn
    session = db_connection.create_session()

    query = session.query(StockTransaction).\
            filter(StockTransaction.symbol == symbol).\
            filter(StockTransaction.buy_or_sell ==
                   StockTransaction.SELL_FLAG).\
            order_by(desc(StockTransaction.date))
    sell_transaction = query.first()

    if (sell_transaction is None):
        session.close()
        raise Exception("no need to clean up transaction table")

    query = session.query(StockTransaction).\
            filter(StockTransaction.symbol == symbol).\
            filter(StockTransaction.buy_or_sell ==
                   StockTransaction.BUY_FLAG).\
            order_by(desc(StockTransaction.price))
    found = False
    buy_transaction = None
    for trans in query:
        if (trans.quantity == sell_transaction.quantity) and \
           (trans.price < sell_transaction.price):
            buy_transaction = trans
            found = True
            break

    if not found:
        session.close()
        raise Exception("no matched buy transaction found")

    print(buy_transaction)
    print(sell_transaction)
    make_transient(buy_transaction)
    make_transient(sell_transaction)

    session.close()

    StockClosedTransactionTable.close_transaction(buy_transaction,
                                                  sell_transaction)

    return

if __name__ == "__main__":
    recreate_db()
