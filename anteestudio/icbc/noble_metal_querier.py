import logging
import urllib.request
from datetime import datetime
import AdvancedHTMLParser

LOGGER = logging.getLogger(__name__)

class NobleMetalPrice:

    def __init__(self,
                 symbol=None,
                 buy_price=None,
                 sell_price=None,
                 middle_price=None,
                 highest_middle_price=None,
                 lowest_middle_price=None):
        self.symbol = symbol
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.middle_price = middle_price
        self.highest_middle_price = highest_middle_price
        self.lowest_middle_price = lowest_middle_price
        return
        
    def __str__(self):
        result = "symbol: {0}\n".format(self.symbol)
        result += "buy price: {0}\n".format(self.buy_price)
        result += "sell price: {0}\n".format(self.sell_price)
        result += "middle price: {0}\n".format(self.middle_price)
        result += "highest middle price: {0}\n".format(
            self.highest_middle_price)
        result += "lowest middle price: {0}\n".format(
            self.lowest_middle_price)
        return result


class NobleMetalQuerier:

    def __init__(self):
        self.url = "http://www.icbc.com.cn/ICBCDynamicSite/" + \
                   "Charts/GoldTendencyPicture.aspx"
        return

    def get_price_list(self):
        parser = AdvancedHTMLParser.AdvancedHTMLParser()
        LOGGER.debug("Get noble metal price list")
        req = urllib.request.Request(url=self.url)
        price_list = []
        with urllib.request.urlopen(req) as f:
            data = f.read().decode("utf-8")
            parser.parseStr(data)
            e = parser.getElementById("TABLE1")
            tbody = e.getChildren()[0]
            trs = tbody.getChildren()
            for tr in trs[1:]:
                tds = tr.getChildren()
                symbol = tds[0].innerHTML.strip()
                buy_price = float(tds[2].innerHTML)
                sell_price = float(tds[3].innerHTML)
                middle_price = float(tds[4].innerHTML)
                highest_middle_price = float(tds[5].innerHTML)
                lowest_middle_price = float(tds[6].innerHTML)
                price = NobleMetalPrice(
                    symbol=symbol,
                    buy_price=buy_price,
                    sell_price=sell_price,
                    middle_price=middle_price,
                    highest_middle_price=highest_middle_price,
                    lowest_middle_price=lowest_middle_price)
                price_list.append(price)
        return price_list
    
