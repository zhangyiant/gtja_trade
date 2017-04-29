import logging
from tkinter import *
from tkinter.ttk import *
from stock_db.db_stock import StockTransactionTable, StockTransaction

class UpdateTransactionFrame(Frame):
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
        self.lstboxStockTransaction.bind("<<ListboxSelect>>", \
                                         self.listbox_select)
        self.refresh_list_box()

        self.lblTransId = Label(self)
        self.lblTransId["text"] = "Transaction ID:"
        self.lblTransId.grid(row = 1, column = 0)
        self.entryTransId = Entry(self)
        self.entryTransId.grid(row = 1, column = 1)

        self.lblSymbol = Label(self)
        self.lblSymbol["text"] = "Symbols:"
        self.lblSymbol.grid(row = 1, column = 0)
        self.entrySymbol = Entry(self)
        self.entrySymbol.grid(row = 1, column = 1)

        self.lblBuyOrSell = Label(self)
        self.lblBuyOrSell["text"] = "Buy/Sell:"
        self.lblBuyOrSell.grid(row = 2, column = 0)
        self.entryBuyOrSell = Entry(self)
        self.entryBuyOrSell.grid(row = 2, column = 1)

        self.lblQuantity = Label(self)
        self.lblQuantity["text"] = "Quantity:"
        self.lblQuantity.grid(row = 3, column = 0)
        self.entryQuantity = Entry(self)
        self.entryQuantity.grid(row = 3, column = 1)

        self.lblPrice = Label(self)
        self.lblPrice["text"] = "Price:"
        self.lblPrice.grid(row = 4, column = 0)
        self.entryPrice = Entry(self)
        self.entryPrice.grid(row = 4, column = 1)

        self.lblDate = Label(self)
        self.lblDate["text"] = "Date:"
        self.lblDate.grid(row = 5, column = 0)
        self.entryDate = Entry(self)
        self.entryDate.grid(row = 5, column = 1)

        self.btnUpdate = Button(self)
        self.btnUpdate["text"] = "Update"
        self.btnUpdate.grid(row = 6, column = 0)
        self.btnUpdate["command"] = self.update_stock_transaction

        self.btnCancel = Button(self)
        self.btnCancel["text"] = "Cancel"
        self.btnCancel.grid(row = 6, column = 1)
        self.btnCancel["command"] = self.quit_dialog

        return

    def get_result(self):
        return 1000

    def update_stock_transaction(self):
        trans_id = int(self.entryTransId.get())

        stock_transaction_table = StockTransactionTable()
        stock_transaction = \
            stock_transaction_table.get_stock_transaction_by_trans_id(trans_id)

        symbol = self.entrySymbol.get()
        buy_or_sell = self.entryBuyOrSell.get()
        quantity = int(self.entryQuantity.get())
        price = float(self.entryPrice.get())
        date = self.entryDate.get()

        stock_transaction.set_symbol(symbol)
        stock_transaction.set_buy_or_sell(buy_or_sell)
        stock_transaction.set_quantity(quantity)
        stock_transaction.set_price(price)

        stock_transaction_table.update_stock_transaction(stock_transaction)

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

    def listbox_select(self, event):
        w = event.widget
        index = w.curselection()
        if len(index) == 0:
            return

        list_box_string = w.get(index[0])
        list_box_string_list = list_box_string.split(",")
        id_string = list_box_string_list[0]
        trans_id = int(id_string[3:])

        stock_transaction_table = StockTransactionTable()
        stock_transaction = \
            stock_transaction_table.get_stock_transaction_by_trans_id(trans_id)

        self.entryTransId.delete(0, END)
        self.entryTransId.insert(END, stock_transaction.get_trans_id())

        self.entrySymbol.delete(0, END)
        self.entrySymbol.insert(END, stock_transaction.get_symbol())

        self.entryBuyOrSell.delete(0, END)
        self.entryBuyOrSell.insert(END, stock_transaction.get_buy_or_sell())

        self.entryQuantity.delete(0, END)
        self.entryQuantity.insert(END, stock_transaction.get_quantity())

        self.entryPrice.delete(0, END)
        self.entryPrice.insert(END, stock_transaction.get_price())

        self.entryDate.delete(0, END)
        self.entryDate.insert(END, stock_transaction.get_date())

        return

    def quit_dialog(self):
        self.master.destroy()
        return

class UpdateTransactionDialog():
    def __init__(self, master=None):
        self.master = master
        self.root = None

    def open(self):
        self.root = Toplevel()
        self.frame = UpdateTransactionFrame(self.root)
        self.frame.grid(padx = 10, pady = 10)
        self.root.transient(self.master)
        self.root.grab_set()
        self.root.wait_window(self.root)
        result = self.frame.get_result()
        return result
