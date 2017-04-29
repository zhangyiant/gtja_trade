import logging
from tkinter import *
from tkinter.ttk import *
from stock_db.db_stock import StockCashTable, StockCash

class NewCashPoolFrame(Frame):
    def __init__(self, master=None):
        self.master = master
        Frame.__init__(self, master)
        self.init_widget()

    def init_widget(self):
        self.lblSymbol = Label(self)
        self.lblSymbol["text"] = "Symbol:"
        self.lblSymbol.grid(row = 0, column = 0)

        self.lblAmount = Label(self)
        self.lblAmount["text"] = "Amount:"
        self.lblAmount.grid(row = 1, column = 0)

        self.entrySymbol = Entry(self)
        self.entrySymbol.grid(row = 0, column = 1)

        self.entryAmount = Entry(self)
        self.entryAmount.grid(row = 1, column = 1)

        self.btnAdd = Button(self)
        self.btnAdd["text"] = "Add"
        self.btnAdd["command"] = self.add_stock_cash
        self.btnAdd.grid(row = 2, column = 0)

        self.btnCancel = Button(self)
        self.btnCancel["text"] = "Cancel"
        self.btnCancel.grid(row = 2, column = 1)
        self.btnCancel["command"] = self.quit_dialog

        self.lblStatus = Label(self)
        self.lblStatus.grid(row = 3, column = 0, columnspan = 2, sticky = W)
        self.set_status("")
        
        return

    def set_status(self, status):
        strStatus = "Status: {0}".format(status)
        self.lblStatus["text"] = strStatus
        return
    
    def get_result(self):
        return 1000

    def add_stock_cash(self):
        stock_cash = StockCash()
        stock_cash.set_symbol(self.entrySymbol.get())
        stock_cash.set_amount(self.entryAmount.get())
        stock_cash_table = StockCashTable()
        stock_cash_table.add_stock_cash(stock_cash)
        self.set_status("Added")
        
    
    def quit_dialog(self):
        self.master.destroy()
        
        
class NewCashPoolDialog():
    def __init__(self, master=None):
        self.master = master
        self.root = None

    def open(self):
        self.root = Toplevel()
        self.frame = NewCashPoolFrame(self.root)
        self.frame.grid(padx = 10, pady = 10)
        self.root.transient(self.master)
        self.root.grab_set()
        self.root.wait_window(self.root)
        result = self.frame.get_result()
        return result
        
    
