import urllib.request


class StockPrice:

    def __init__(self):
        self.url_prefix = "http://hq.sinajs.cn/"
        self.symbol = None
        self.opening_price = None
        self.closing_price = None
        self.price = None
        self.highest_price = None
        self.lowest_price = None
        self.buy_price = None
        self.sell_price = None
        self.turnover = None
        self.amount = None
        self.buy_1_volume = None
        self.buy_1_price = None
        self.buy_2_volume = None
        self.buy_2_price = None
        self.buy_3_volume = None
        self.buy_3_price = None
        self.buy_4_volume = None
        self.buy_4_price = None
        self.buy_5_volume = None
        self.buy_5_price = None
        self.sell_1_volume = None
        self.sell_1_price = None
        self.sell_2_volume = None
        self.sell_2_price = None
        self.sell_3_volume = None
        self.sell_3_price = None
        self.sell_4_volume = None
        self.sell_4_price = None
        self.sell_5_volume = None
        self.sell_5_price = None
        self.date = None
        self.time = None
        return

    def strip_script(self, data):
        r = data
        q = r.find("\"")
        r = r[q + 1:]
        q = r.find("\"")
        r = r[0:q]
        return r

    def parse(self, data):
        stripped_data = self.strip_script(data)
        items = stripped_data.split(",")
        print(items)
        self.symbol = items[0]
        self.opening_price = float(items[1])
        self.closing_price = float(items[2])
        self.price = float(items[3])
        self.highest_price = float(items[4])
        self.lowest_price = float(items[5])
        self.buy_price = float(items[6])
        self.sell_price = float(items[7])
        self.turnover = int(items[8])
        self.amount = float(items[9])
        self.buy_1_volume = int(items[10])
        self.buy_1_price = float(items[11])
        self.buy_2_volume = int(items[12])
        self.buy_2_price = float(items[13])
        self.buy_3_volume = int(items[14])
        self.buy_3_price = float(items[15])
        self.buy_4_volume = int(items[16])
        self.buy_4_price = float(items[17])
        self.buy_5_volume = int(items[18])
        self.buy_5_price = float(items[19])
        self.sell_1_volume = int(items[20])
        self.sell_1_price = float(items[21])
        self.sell_2_volume = int(items[22])
        self.sell_2_price = float(items[23])
        self.sell_3_volume = int(items[24])
        self.sell_3_price = float(items[25])
        self.sell_4_volume = int(items[26])
        self.sell_4_price = float(items[27])
        self.sell_5_volume = int(items[28])
        self.sell_5_price = float(items[29])
        self.date = items[30]
        self.time = items[31]
        return

    def get_full_symbol(self, symbol):
        first_char = symbol[0]
        if first_char == "6":
            full_symbol = "sh" + symbol
        elif first_char == "0":
            full_symbol = "sz" + symbol
        else:
            full_symbol = symbol
        return full_symbol

    def get_price(self, symbol):
        full_symbol = self.get_full_symbol(symbol)
        url = self.url_prefix + "list=" + full_symbol
        req = urllib.request.Request(url=url)
        with urllib.request.urlopen(req) as f:
            data = f.read().decode("GBK")
        self.parse(data)
        return

    def __str__(self):
        result = "股票代码: {0}\n".format(self.symbol)
        result += "今日开盘价: {0}\n".format(self.opening_price)
        result += "昨日收盘价: {0}\n".format(self.closing_price)
        result += "当前价格: {0}\n".format(self.price)
        result += "今日最高价: {0}\n".format(self.highest_price)
        result += "今日最低价: {0}\n".format(self.lowest_price)
        result += "竞买价: {0}\n".format(self.buy_price)
        result += "竞卖价: {0}\n".format(self.sell_price)
        result += "成交量: {0}\n".format(self.turnover)
        result += "成交金额: {0}\n".format(self.amount)
        result += "买一量: {0}\n".format(self.buy_1_volume)
        result += "买一价格: {0}\n".format(self.buy_1_price)
        result += "买二量: {0}\n".format(self.buy_2_volume)
        result += "买二价格: {0}\n".format(self.buy_2_price)
        result += "买三量: {0}\n".format(self.buy_3_volume)
        result += "买三价格: {0}\n".format(self.buy_3_price)
        result += "买四量: {0}\n".format(self.buy_4_volume)
        result += "买四价格: {0}\n".format(self.buy_4_price)
        result += "买五量: {0}\n".format(self.buy_5_volume)
        result += "买五价格: {0}\n".format(self.buy_5_price)
        result += "卖一量: {0}\n".format(self.sell_1_volume)
        result += "卖一价格: {0}\n".format(self.sell_1_price)
        result += "卖二量: {0}\n".format(self.sell_2_volume)
        result += "卖二价格: {0}\n".format(self.sell_2_price)
        result += "卖三量: {0}\n".format(self.sell_3_volume)
        result += "卖三价格: {0}\n".format(self.sell_3_price)
        result += "卖四量: {0}\n".format(self.sell_4_volume)
        result += "卖四价格: {0}\n".format(self.sell_4_price)
        result += "卖五量: {0}\n".format(self.sell_5_volume)
        result += "卖五价格: {0}\n".format(self.sell_5_price)
        result += "日期: {0}\n".format(self.date)
        result += "时间: {0}\n".format(self.time)
        return result
