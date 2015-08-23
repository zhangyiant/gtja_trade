'''
Created on Jul 8, 2015

@author: Yi Zhang
'''
from gtja.Trade import Trade
from gtja.stockprocessor import StockProcessor

import csv
import time
import datetime

with open("account_info.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        account_name = row[0]
        password = row[1]
        break


#commission_id = trade.buy_stock("601398", 4.34, 100)

#commission_id = trade.get_last_commission_id("601398", 100)

stock_processor = StockProcessor(account_name, password)
print(account_name, password)
 
stock_processor.login()
 
time.sleep(3)

stock_processor.set_stock_symbol_list(["601398", "601857"])

def is_transaction_time():
    td = datetime.datetime.now()
    t1 = td.time()
    t2 = datetime.time(9,0,0)
    t3 = datetime.time(11,30,0)
    t4 = datetime.time(13,0,0)
    t5= datetime.time(15,0,0)
    if (t1 < t2):
        return False
    if (t1>=t2 and t1<=t3):
        return True
    if (t1>t3 and t1 < t4):
        return False
    if (t1>=t4 and t1 <= t5):
        return True
    if (t1>t5):
        return False
    
def is_market_closed():
    td = datetime.datetime.now()
    t1 = td.time()
    t2 = datetime.time(15,0,0)
    if (t1 > t2):
        return True
    else:
        return False

stock_symbol_list = ["601398", "601857"]

while True:
    # check time
    if (is_market_closed()):
        print("market is close!")
        break
    
#     if (not is_transaction_time()):
#         print("It's not transaction time now!")
#         time.sleep(180)
#         continue
    
    stock_symbol = stock_processor.get_one_stock()
    stock_processor.process_stock(stock_symbol)
    
    break    
#commission_id = trade.sell_stock("601398", 5.12, 200)


stock_processor.close()
