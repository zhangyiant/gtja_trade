import logging
from tkinter import *
from tkinter.ttk import *
from stock_db.db_stock import StockInfoTable, StockInfo

class ShowStockInfoFrame(Frame):
    def __init__(self, master=None):
        self.master = master
        Frame.__init__(self, master)
        self.init_widget()

    def init_widget(self):
        self.txtStockInfo = Text(self)
        self.txtStockInfo.grid(row = 0, column = 0)
        stock_info_text = self.get_stock_info_text()
        self.set_text(stock_info_text)
        return

    def set_text(self, text):
        self.txtStockInfo["state"] = NORMAL
        self.txtStockInfo.delete("0.0", END)
        self.txtStockInfo.insert(INSERT, text)
        self.txtStockInfo["state"] = DISABLED
        return

    def get_stock_info_text(self):
        result = ""
        stock_info_table = StockInfoTable()
        stock_info_list = stock_info_table.get_all_stock_info()
        for stock_info in stock_info_list:
            result = result + "{0}".format(stock_info) + "\n"
        return result

    def get_result(self):
        return 100

class ShowStockInfoDialog():
    def __init__(self, master=None):
        self.master = master
        self.root = None

    def open(self):
        self.root = Toplevel()
        self.frame = ShowStockInfoFrame(self.root)
        self.frame.grid(padx = 10, pady = 10)
        self.root.transient(self.master)
        self.root.grab_set()
        self.root.wait_window(self.root)
        result = self.frame.get_result()
        return result
