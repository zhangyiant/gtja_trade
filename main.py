'''
Created on Jul 8, 2015

@author: yizhang
'''
from gtja.Trade import Trade

import csv
import time

with open("account_info.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        account_name = row[0]
        password = row[1]
        break

print(account_name, password)
trade = Trade(account_name, password)

trade.login()

time.sleep(3)

#commission_id = trade.buy_stock("601398", 4.34, 100)

#commission_id = trade.get_last_commission_id("601398", 100)

symbol_list = ["601398", "601857"]

def is_transaction_time():
    return False

def process_stock():
    return

while True:
    # check time
    if (not is_transaction_time()):
        print("It's not transaction time now!")
        break
    
    process_stock("601398")
        
#commission_id = trade.sell_stock("601398", 5.12, 200)


trade.close()
