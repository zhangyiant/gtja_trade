import logging
from tkinter import *
from tkinter.ttk import *
from stock_db.db_stock import StockCashTable, StockCash

class UpdateCashPoolFrame(Frame):
    def __init__(self, master=None):
        self.master = master
        Frame.__init__(self, master)
        self.init_widget()

    def init_widget(self):
        self.scrollbar = Scrollbar(self)
        self.lstboxStockCash = Listbox(self)
        self.lstboxStockCash.grid(row = 0, column = 0, columnspan = 2)
        self.scrollbar.grid(row = 0, column = 3, sticky=NS)
        self.lstboxStockCash["yscrollcommand"] = self.scrollbar.set
        self.scrollbar["command"] = self.lstboxStockCash.yview
        self.refresh_list_box()

        self.entryAmount = Entry(self)
        self.entryAmount.grid(row = 1, column = 0, columnspan = 2)
        
        self.btnUpdate = Button(self)
        self.btnUpdate["text"] = "Update"
        self.btnUpdate.grid(row = 2, column = 0)
        self.btnUpdate["command"] = self.update_stock_cash
         
        self.btnCancel = Button(self)
        self.btnCancel["text"] = "Cancel"
        self.btnCancel.grid(row = 2, column = 1)
        self.btnCancel["command"] = self.quit_dialog
        
        return
    
    def get_result(self):
        return 1000

    
    def update_stock_cash(self):
        index = self.lstboxStockCash.curselection()
        if len(index) == 0:
            return
        
        symbol = self.lstboxStockCash.get(index[0])
        amount = float(self.entryAmount.get())
        
        stock_cash = StockCash(symbol, amount)
        stock_cash_table = StockCashTable()
        stock_cash_table.update_stock_cash(stock_cash)

        self.refresh_list_box()
        
        return

    def refresh_list_box(self):
        self.lstboxStockCash.delete(0, END)
        stock_cash_table = StockCashTable()
        stock_cash_list = stock_cash_table.get_all_stock_cash()
        for stock_cash in stock_cash_list:
            self.lstboxStockCash.insert(END, stock_cash.get_symbol())
        return
    
    def quit_dialog(self):
        self.master.destroy()
        return
        
        
class UpdateCashPoolDialog():
    def __init__(self, master=None):
        self.master = master
        self.root = None

    def open(self):
        self.root = Toplevel()
        self.frame = UpdateCashPoolFrame(self.root)
        self.frame.grid(padx = 10, pady = 10)
        self.root.transient(self.master)
        self.root.grab_set()
        self.root.wait_window(self.root)
        result = self.frame.get_result()
        return result
        
    
