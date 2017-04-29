import logging
from tkinter import *
from tkinter.ttk import *
from stock_db.db_stock import StockCashTable, StockCash

class ShowCashPoolFrame(Frame):
    def __init__(self, master=None):
        self.master = master
        Frame.__init__(self, master)
        self.init_widget()

    def init_widget(self):
        self.txtCashPool = Text(self)
        self.txtCashPool.grid(row = 0, column = 0)
        stock_cash_text = self.get_cash_pool_text()
        self.set_text(stock_cash_text)
        return

    def set_text(self, text):
        self.txtCashPool["state"] = NORMAL
        self.txtCashPool.delete("0.0", END)
        self.txtCashPool.insert(INSERT, text)
        self.txtCashPool["state"] = DISABLED
        return

    def get_cash_pool_text(self):
        result = ""
        stock_cash_table = StockCashTable()
        stock_cash_list = stock_cash_table.get_all_stock_cash()
        for stock_cash in stock_cash_list:
            result = result + "{0}".format(stock_cash) + "\n"
        return result
    
    def get_result(self):
        return 100
        
        
class ShowCashPoolDialog():
    def __init__(self, master=None):
        self.master = master
        self.root = None

    def open(self):
        self.root = Toplevel()
        self.frame = ShowCashPoolFrame(self.root)
        self.frame.grid(padx = 10, pady = 10)
        self.root.transient(self.master)
        self.root.grab_set()
        self.root.wait_window(self.root)
        result = self.frame.get_result()
        return result
