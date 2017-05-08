import logging
from datetime import datetime

from stock_db.db_connection import get_default_db_connection
from stock_db.db_stock import TradeKeepAlive

LOGGER = logging.getLogger(__name__)


def update_keep_alive(app_name=None, conn=None):
    if app_name is None:
        return

    if conn is None:
        conn = get_default_db_connection()

    session = conn.create_session()

    trade_keep_alive = session.query(TradeKeepAlive).\
        filter(TradeKeepAlive.app_name == app_name).\
        one_or_none()

    if trade_keep_alive is None:
        LOGGER.debug("No entry in TradeKeepAlive table, create a new one.")
        trade_keep_alive = TradeKeepAlive(
            app_name=app_name,
            refresh_time=datetime.utcnow())
        session.add(trade_keep_alive)
    else:
        LOGGER.debug("Existing entry found, refresh time")
        trade_keep_alive.refresh_time = datetime.utcnow()
    session.commit()
    session.close()

    return
