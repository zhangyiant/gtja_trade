import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from stock_db.db_connection import get_default_db_connection
from stock_db.db_stock import NobleMetalPrice

LOGGER = logging.getLogger(__name__)


class NobleMetalPriceCollector:
    """
        NobleMetalPrice collector
    """
    def __init__(self):
        self.link = \
            "http://www.icbc.com.cn/ICBCDynamicSite/" + \
            "Charts/GoldTendencyPicture.aspx"
        self.driver = webdriver.Firefox()
        self.table_id = "TABLE1"
        self.conn = get_default_db_connection()
        return

    def collect(self):
        try:
            self.driver.get(self.link)
            table_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, self.table_id)))
            if table_element is None:
                return False
        except TimeoutException as timeout_exception:
            LOGGER.warning(
                "Timeout exception when fetching table. {0}".format(
                    timeout_exception))
            return False;
        tbody_element = table_element.find_element_by_xpath("tbody")
        tr_elements = tbody_element.find_elements_by_xpath("*")
        for tr_element in tr_elements[1:]:
            column_elements = tr_element.\
                find_elements_by_tag_name("td")
            symbol = column_elements[0].text
            buy_price = float(column_elements[2].text)
            sell_price = float(column_elements[3].text)
            middle_price = float(column_elements[4].text)
            highest_middle_price = float(column_elements[5].text)
            lowest_middle_price = float(column_elements[6].text)

            session = self.conn.create_session()
            noble_metal_price = NobleMetalPrice()
            noble_metal_price.symbol = symbol
            noble_metal_price.buy_price = buy_price
            noble_metal_price.sell_price = sell_price
            noble_metal_price.middle_price = middle_price
            noble_metal_price.highest_middle_price = highest_middle_price
            noble_metal_price.lowest_middle_price = lowest_middle_price
            noble_metal_price.update_datetime = datetime.utcnow()
            session.add(noble_metal_price)
            session.commit()
            session.close()
        return True

    def close(self):
        self.driver.quit()
        return
