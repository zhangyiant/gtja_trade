import logging
from tkinter import *
from tkinter.ttk import *
from stock_db.db_stock import StockTransactionTable, StockTransaction

class ShowTransactionFrame(Frame):
    def __init__(self, master=None):
        self.master = master
        Frame.__init__(self, master)
        self.init_widget()

    def init_widget(self):
        self.txtTransaction = Text(self)
        self.txtTransaction.grid(row = 0, column = 0)
        transaction_text = self.get_transaction_text()
        self.set_text(transaction_text)
        return

    def set_text(self, text):
        self.txtTransaction["state"] = NORMAL
        self.txtTransaction.delete("0.0", END)
        self.txtTransaction.insert(INSERT, text)
        self.txtTransaction["state"] = DISABLED
        return

    def get_transaction_text(self):
        result = ""
        transaction_table = StockTransactionTable()
        transaction_list = transaction_table.get_all_stock_transaction()
        for stock_transaction in transaction_list:
            result = result + "{0}".format(stock_transaction) + "\n"
        return result
    
    def get_result(self):
        return 100
        
        
class ShowTransactionDialog():
    def __init__(self, master=None):
        self.master = master
        self.root = None

    def open(self):
        self.root = Toplevel()
        self.frame = ShowTransactionFrame(self.root)
        self.frame.grid(padx = 10, pady = 10)
        self.root.transient(self.master)
        self.root.grab_set()
        self.root.wait_window(self.root)
        result = self.frame.get_result()
        return result
        
    
