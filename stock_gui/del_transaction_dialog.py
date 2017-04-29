import logging
from tkinter import *
from tkinter.ttk import *
from stock_db.db_stock import StockTransactionTable, StockTransaction

class DelTransactionFrame(Frame):
    def __init__(self, master=None):
        self.master = master
        Frame.__init__(self, master)
        self.init_widget()

    def init_widget(self):
        self.scrollbar = Scrollbar(self)
        self.lstboxStockTransaction = Listbox(self)
        self.lstboxStockTransaction.grid(row = 0, column = 0, columnspan = 2)
        self.scrollbar.grid(row = 0, column = 3, sticky=NS)
        self.lstboxStockTransaction["yscrollcommand"] = self.scrollbar.set
        self.scrollbar["command"] = self.lstboxStockTransaction.yview
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
        index = self.lstboxStockTransaction.curselection()
        if len(index) == 0:
            return

        list_box_string = self.lstboxStockTransaction.get(index[0])
        list_box_string_list = list_box_string.split(",")
        id_string = list_box_string_list[0]
        trans_id = int(id_string[3:])

        stock_transaction_table = StockTransactionTable()
        stock_transaction = \
            stock_transaction_table.get_stock_transaction_by_trans_id(trans_id)

        stock_transaction_table.delete_stock_transaction(stock_transaction)

        self.refresh_list_box()

        return

    def refresh_list_box(self):
        self.lstboxStockTransaction.delete(0, END)
        stock_transaction_table = StockTransactionTable()
        stock_transaction_list = \
            stock_transaction_table.get_all_stock_transaction()
        for stock_transaction in stock_transaction_list:
            list_box_string = "ID:{0},Symbol:{1},Buy_or_Sell:{2}".format(
                stock_transaction.get_trans_id(),
                stock_transaction.get_symbol(),
                stock_transaction.get_buy_or_sell())
            self.lstboxStockTransaction.insert(END, \
                                               list_box_string)
        return

    def quit_dialog(self):
        self.master.destroy()
        return

class DelTransactionDialog():
    def __init__(self, master=None):
        self.master = master
        self.root = None

    def open(self):
        self.root = Toplevel()
        self.frame = DelTransactionFrame(self.root)
        self.frame.grid(padx = 10, pady = 10)
        self.root.transient(self.master)
        self.root.grab_set()
        self.root.wait_window(self.root)
        result = self.frame.get_result()
        return result
