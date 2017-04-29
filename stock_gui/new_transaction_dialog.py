import logging
from tkinter import *
from tkinter.ttk import *
from stock_db.db_stock import StockCashTable, StockCash
from stock_db.db_stock import StockTransactionTable, StockTransaction
import datetime

class NewTransactionFrame(Frame):
    def __init__(self, master=None):
        self.master = master
        Frame.__init__(self, master)
        self.init_widget()

    def init_widget(self):
        self.lblSymbol = Label(self)
        self.lblSymbol["text"] = "Symbol:"
        self.lblSymbol.grid(row = 0, column = 0)

        self.cbbSymbol = Combobox(self)
        self.fill_symbol_combobox()
        self.cbbSymbol.grid(row = 0, column = 1)

        self.lblBuyOrSell = Label(self)
        self.lblBuyOrSell["text"] = "Buy/Sell:"
        self.lblBuyOrSell.grid(row = 1, column = 0)
        self.cbbBuyOrSell = Combobox(self)
        self.cbbBuyOrSell["values"] = ["Buy", "Sell"]
        self.cbbBuyOrSell.grid(row = 1, column = 1)

        self.lblQuantity = Label(self)
        self.lblQuantity["text"] = "Quantity:"
        self.lblQuantity.grid(row = 2, column = 0)
        self.entryQuantity = Entry(self)
        self.entryQuantity.grid(row = 2, column = 1)

        self.lblPrice = Label(self)
        self.lblPrice["text"] = "Price:"
        self.lblPrice.grid(row = 3, column = 0)
        self.entryPrice = Entry(self)
        self.entryPrice.grid(row = 3, column = 1)

        self.lblDate = Label(self)
        self.lblDate["text"] = "Date:"
        self.lblDate.grid(row = 4, column = 0)
        self.entryDate = Entry(self)
        self.entryDate.grid(row = 4, column = 1)

        self.btnAdd = Button(self)
        self.btnAdd["text"] = "Add"
        self.btnAdd["command"] = self.add_transaction
        self.btnAdd.grid(row = 5, column = 0)

        self.btnCancel = Button(self)
        self.btnCancel["text"] = "Cancel"
        self.btnCancel.grid(row = 5, column = 1)
        self.btnCancel["command"] = self.quit_dialog

        self.lblStatus = Label(self)
        self.lblStatus.grid(row = 6, column = 0, columnspan = 2, sticky = W)
        self.set_status("")
        
        return

    def set_status(self, status):
        strStatus = "Status: {0}".format(status)
        self.lblStatus["text"] = strStatus
        return
    
    def get_result(self):
        return 1000

    def add_transaction(self):
        symbol = self.cbbSymbol.get()
        if (not symbol):
            self.set_status("Symbol is empty.")
            return
        buy_or_sell = self.cbbBuyOrSell.get()
        if (not buy_or_sell):
            self.set_status("Buy/Sell is empty.")
            return
        quantity = self.entryQuantity.get()
        if (not quantity):
            self.set_status("Quantity is empty.")
            return
        price = self.entryPrice.get()
        if (not price):
            self.set_status("Price is empty.")
            return
#         date = self.entryDate.get()
#         if (not date):
#             self.set_status("Date is empty.")
#             return

        stock_transaction = StockTransaction()
        stock_transaction.set_symbol(symbol)
        stock_transaction.set_buy_or_sell(buy_or_sell)
        stock_transaction.set_quantity(quantity)
        stock_transaction.set_price(price)
#        stock_transaction.set_date(date)
        stock_transaction.set_date(datetime.datetime.now())
        
        stock_transaction_table = StockTransactionTable()
        stock_transaction_table.add_stock_transaction(stock_transaction)
        
        self.set_status("Added")
        return
    
    def fill_symbol_combobox(self):
        stock_cash_table = StockCashTable()
        stock_cash_list = stock_cash_table.get_all_stock_cash()
        symbol_list = []
        for stock_cash in stock_cash_list:
            symbol_list.append(stock_cash.get_symbol())
        self.cbbSymbol["values"] = symbol_list
        return

    def quit_dialog(self):
        self.master.destroy()
        return

class NewTransactionDialog():
    def __init__(self, master=None):
        self.master = master
        self.root = None

    def open(self):
        self.root = Toplevel()
        self.frame = NewTransactionFrame(self.root)
        self.frame.grid(padx = 10, pady = 10)
        self.root.transient(self.master)
        self.root.grab_set()
        self.root.wait_window(self.root)
        result = self.frame.get_result()
        return result
        
    
