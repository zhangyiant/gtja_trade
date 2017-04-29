import logging
from tkinter import *
from tkinter.ttk import *
from stock_db.db_connection import get_default_db_connection
from stock_gui.new_cash_pool_dialog import NewCashPoolDialog
from stock_gui.show_cash_pool_dialog import ShowCashPoolDialog
from stock_gui.del_cash_pool_dialog import DelCashPoolDialog
from stock_gui.update_cash_pool_dialog import UpdateCashPoolDialog
from stock_gui.show_transaction_dialog import ShowTransactionDialog
from stock_gui.new_transaction_dialog import NewTransactionDialog
from stock_gui.update_transaction_dialog import UpdateTransactionDialog
from stock_gui.del_transaction_dialog import DelTransactionDialog
from stock_gui.show_stock_info_dialog import ShowStockInfoDialog
from stock_gui.suggestion_dialog import SuggestionDialog

import stock_db.db_utility

def donothing():
    return

class StockApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Stock buy/sell suggestion")
        self.root.minsize(400, 400)
        self.init_stock_cash_menu()
        self.init_widget()

    def init_stock_cash_menu(self):
        self.menu_bar = Menu(self.root)
        self.cash_menu = Menu(self.menu_bar)
        self.transaction_menu = Menu(self.menu_bar)
        self.other_menu = Menu(self.menu_bar)

        # cash menu
        self.cash_menu.add_command(label="New cash pool",
                                   command=self.new_cash_pool)
        self.cash_menu.add_command(label="Delete cash pool",
                                   command=self.delete_cash_pool)
        self.cash_menu.add_command(label="Update cash pool",
                                   command=self.update_cash_pool)
        self.cash_menu.add_command(label="Show cash pool",
                                   command=self.show_cash_pool)
        self.menu_bar.add_cascade(label="Cash", menu=self.cash_menu)

        # transaction menu
        self.transaction_menu.add_command(label="Add transaction",
                                          command=self.new_transaction)
        self.transaction_menu.add_command(label="Delete transaction",
                                          command=self.delete_transaction)
        self.transaction_menu.add_command(label="Update transaction",
                                          command=self.update_transaction)
        self.transaction_menu.add_command(label="Show transaction",
                                          command=self.show_transaction)
        self.menu_bar.add_cascade(label="Transaction",
                                  menu=self.transaction_menu)

        # other menu
        self.other_menu.add_command(label="new quit!", command=self.root.quit)
        self.other_menu.add_command(label="Get suggestion",
                                    command=self.suggestion)
        self.other_menu.add_command(label="Reset database",
                                    command=self.reset_db)
        self.other_menu.add_command(label = "Import stock information",
                                    command = self.import_stock_info)
        self.other_menu.add_command(label="Show stock information",
                                    command=self.show_stock_info)
        self.menu_bar.add_cascade(label="other", menu=self.other_menu)

        self.root["menu"] = self.menu_bar

    def init_widget(self):
        self.button = Button(self.root)
        self.button["text"] = "hello world"
        self.button.pack()
        return

    def new_cash_pool(self):
        dialog = NewCashPoolDialog()
        result = dialog.open()
        return

    def delete_cash_pool(self):
        dialog = DelCashPoolDialog()
        result = dialog.open()
        return

    def update_cash_pool(self):
        dialog = UpdateCashPoolDialog()
        result = dialog.open()
        return

    def show_cash_pool(self):
        dialog = ShowCashPoolDialog()
        result = dialog.open()
        return

    def new_transaction(self):
        dialog = NewTransactionDialog()
        result = dialog.open()
        return

    def delete_transaction(self):
        dialog = DelTransactionDialog()
        result = dialog.open()
        return

    def update_transaction(self):
        dialog = UpdateTransactionDialog()
        result = dialog.open()
        return

    def show_transaction(self):
        dialog = ShowTransactionDialog()
        result = dialog.open()
        return

    def show_stock_info(self):
        dialog = ShowStockInfoDialog()
        result = dialog.open()
        return

    def suggestion(self):
        dialog = SuggestionDialog()
        result = dialog.open()
        return

    def import_stock_info(self):
        stock_db.db_utility.import_stock_info()
        return

    def reset_db(self):
        stock_db.db_utility.reset_table()
        return

    def mainloop(self):
        self.root.mainloop()
        return
