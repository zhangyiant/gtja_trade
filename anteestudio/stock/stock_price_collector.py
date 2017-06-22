import logging
from datetime import datetime
from datetime import timezone


from stock_db.db_connection import get_default_db_connection
from stock_db.db_stock import StockPrice

from anteestudio.sina.stock import StockPriceQuerier

LOGGER = logging.getLogger(__name__)


class StockPriceCollector:

    def __init__(self):
        self.conn = get_default_db_connection()
        return

    def collect(self, symbol):
        stock_price_querier = StockPriceQuerier()
        stock_price_querier.get_price(symbol)
        session = self.conn.create_session()
        stock_price = StockPrice()
        stock_price.symbol = stock_price_querier.symbol
        stock_price.opening_price = stock_price_querier.opening_price
        stock_price.closing_price = stock_price_querier.closing_price
        stock_price.price = stock_price_querier.price
        stock_price.highest_price = stock_price_querier.highest_price
        stock_price.lowest_price = stock_price_querier.lowest_price
        stock_price.buy_price = stock_price_querier.buy_price
        stock_price.sell_price = stock_price_querier.sell_price
        stock_price.turnover = stock_price_querier.turnover
        stock_price.amount = stock_price_querier.amount
        stock_price.buy_1_volume = stock_price_querier.buy_1_volume
        stock_price.buy_1_price = stock_price_querier.buy_1_price
        stock_price.buy_2_volume = stock_price_querier.buy_2_volume
        stock_price.buy_2_price = stock_price_querier.buy_2_price
        stock_price.buy_3_volume = stock_price_querier.buy_3_volume
        stock_price.buy_3_price = stock_price_querier.buy_3_price
        stock_price.buy_4_volume = stock_price_querier.buy_4_volume
        stock_price.buy_4_price = stock_price_querier.buy_4_price
        stock_price.buy_5_volume = stock_price_querier.buy_5_volume
        stock_price.buy_5_price = stock_price_querier.buy_5_price
        stock_price.sell_1_volume = stock_price_querier.sell_1_volume
        stock_price.sell_1_price = stock_price_querier.sell_1_price
        stock_price.sell_2_volume = stock_price_querier.sell_2_volume
        stock_price.sell_2_price = stock_price_querier.sell_2_price
        stock_price.sell_3_volume = stock_price_querier.sell_3_volume
        stock_price.sell_3_price = stock_price_querier.sell_3_price
        stock_price.sell_4_volume = stock_price_querier.sell_4_volume
        stock_price.sell_4_price = stock_price_querier.sell_4_price
        stock_price.sell_5_volume = stock_price_querier.sell_5_volume
        stock_price.sell_5_price = stock_price_querier.sell_5_price
        stock_price.update_datetime = stock_price_querier.datetime.astimezone(
            timezone.utc)

        session.add(stock_price)
        session.commit()
        session.close()
        return
