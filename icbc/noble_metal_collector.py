import logging
from datetime import datetime

from stock_db.db_connection import get_default_db_connection
from stock_db.db_stock import NobleMetalPrice

from anteestudio.icbc import NobleMetalQuerier

LOGGER = logging.getLogger(__name__)


class NobleMetalPriceCollector:
    """
        NobleMetalPrice collector
    """
    def __init__(self):
        self.conn = get_default_db_connection()
        return

    def collect(self):
        querier = NobleMetalQuerier()
        price_list = querier.get_price_list()
        for price in price_list:
            session = self.conn.create_session()
            noble_metal_price = NobleMetalPrice()
            noble_metal_price.symbol = price.symbol
            noble_metal_price.buy_price = price.buy_price
            noble_metal_price.sell_price = price.sell_price
            noble_metal_price.middle_price = price.middle_price
            noble_metal_price.highest_middle_price = price.highest_middle_price
            noble_metal_price.lowest_middle_price = price.lowest_middle_price
            noble_metal_price.update_datetime = datetime.utcnow()
            session.add(noble_metal_price)
            session.commit()
            session.close()
        return True

    def close(self):
        return
