import logging
import urllib.request
from datetime import datetime
import AdvancedHTMLParser

LOGGER = logging.getLogger(__name__)


class NobleMetalQuerier:

    def __init__(self):
        self.url = "http://www.icbc.com.cn/ICBCDynamicSite/" + \
                   "Charts/GoldTendencyPicture.aspx"
        return

    def get_price_list(self):
        parser = AdvancedHTMLParser.AdvancedHTMLParser()
        LOGGER.debug("Get noble metal price list")
        req = urllib.request.Request(url=self.url)
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
                print("{0}:{1}:{2}:{3}:{4}:{5}".format(
                    symbol,
                    buy_price,
                    sell_price,
                    middle_price,
                    highest_middle_price,
                    lowest_middle_price))
        return
    
