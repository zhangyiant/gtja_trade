"""
    Update total history value
"""
import configparser
import logging
from datetime import datetime
import stock_db
from stock_db.db_connection import get_default_db_connection
from stock_db.db_stock import \
    StockInfo, \
    StockCash, \
    StockTransaction, \
    StockCashTotalHistoryValue, \
    AllInvestmentsHistory

# read configuration
CONFIG_PARSER = configparser.ConfigParser()
CONFIG_PARSER.read("stock.ini", encoding="utf-8")
CONNECTION_STRING = CONFIG_PARSER['Database'].get('connection')
LOGGING_FILENAME = CONFIG_PARSER['Logging'].get('filename')

# logger setup
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
FH = logging.FileHandler(LOGGING_FILENAME, encoding="utf-8")
FORMATTER = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
FH.setFormatter(FORMATTER)
LOGGER.addHandler(FH)

# set the DB connection string
stock_db.db_connection.default_connection_string = CONNECTION_STRING

def get_cash(symbol, session):
    """
        Get cash value from stock cash table.
    """
    stock_cash = session.query(StockCash).\
                 filter(StockCash.symbol == symbol).\
                 one_or_none()
    if stock_cash is None:
        return 0
    else:
        return stock_cash.amount

def get_total_stock_value(symbol, session):
    """
        Get total stock value from stock transaction table
    """
    stock_transactions = session.query(StockTransaction).\
                         filter(StockTransaction.symbol == symbol).\
                         filter(StockTransaction.buy_or_sell ==
                                StockTransaction.BUY_FLAG).\
                                all()
    result = 0
    for stock_transaction in stock_transactions:
        amount = stock_transaction.quantity * \
                 stock_transaction.price
        result += amount

    return result

def update_total_history(symbol, session):
    """
        Record the total value in history table.
    """
    cash_amount = get_cash(symbol, session)
    stock_amount = get_total_stock_value(symbol, session)
    total_amount = cash_amount + stock_amount

    LOGGER.debug("Symbol: {0}".format(symbol))
    LOGGER.debug("Cash: {0}".format(cash_amount))
    LOGGER.debug("Stock: {0}".format(stock_amount))
    LOGGER.debug("Total: {0}".format(total_amount))
    stock_cash_total_history_value = StockCashTotalHistoryValue(
        symbol=symbol,
        date=datetime.utcnow(),
        total_value=total_amount)
    session.add(stock_cash_total_history_value)
    session.commit()

    return total_amount

def main():
    '''
        main module
    '''
    conn = get_default_db_connection()
    session = conn.create_session()

    stock_infos = session.query(StockInfo).all()

    total = 0.0
    for stock_info in stock_infos:
        symbol = stock_info.symbol
        total_amount = update_total_history(symbol, session)
        if "美元" in symbol:
            continue
        else:
            total += total_amount

    all_investments_history = AllInvestmentsHistory(
        date=datetime.utcnow(),
        total_value=total)
    session.add(all_investments_history)
    session.commit()

    session.close()
    return

if __name__ == "__main__":
    main()
