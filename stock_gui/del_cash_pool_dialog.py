'''
    del_cash_pool_dialog
'''
from tkinter import *
from tkinter.ttk import *
from stock_db.db_stock import StockCashTable, StockCash

class DelCashPoolFrame(Frame):
    '''
        class DelCashPoolFrame
    '''
    def __init__(self, master=None):
        self.master = master
        Frame.__init__(self, master)
        self.init_widget()

    def init_widget(self):
        '''
            init_widget
        '''
        self.scrollbar = Scrollbar(self)
        self.lstboxStockCash = Listbox(self)
        self.lstboxStockCash.grid(row = 0, column = 0, columnspan = 2)
        self.scrollbar.grid(row = 0, column = 3, sticky=NS)
        self.lstboxStockCash["yscrollcommand"] = self.scrollbar.set
        self.scrollbar["command"] = self.lstboxStockCash.yview
        self.refresh_list_box()

        self.btnDelete = Button(self)
        self.btnDelete["text"] = "Delete"
        self.btnDelete.grid(row = 1, column = 0)
        self.btnDelete["command"] = self.delete_stock_cash

        self.btnCancel = Button(self)
        self.btnCancel["text"] = "Cancel"
        self.btnCancel.grid(row = 1, column = 1)
        self.btnCancel["command"] = self.quit_dialog
        
        return
    
    def get_result(self):
        return 1000

    
    def delete_stock_cash(self):
        index = self.lstboxStockCash.curselection()
        if len(index) == 0:
            return
        
        symbol = self.lstboxStockCash.get(index[0])

        stock_cash = StockCash(symbol)
        stock_cash_table = StockCashTable()
        stock_cash_table.delete_stock_cash(stock_cash)

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
        
        
class DelCashPoolDialog():
    def __init__(self, master=None):
        self.master = master
        self.root = None

    def open(self):
        self.root = Toplevel()
        self.frame = DelCashPoolFrame(self.root)
        self.frame.grid(padx = 10, pady = 10)
        self.root.transient(self.master)
        self.root.grab_set()
        self.root.wait_window(self.root)
        result = self.frame.get_result()
        return result
        
    
