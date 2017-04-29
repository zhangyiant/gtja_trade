import logging
from tkinter import *
from tkinter.ttk import *
from stock_db.db_stock import StockCashTable, StockCash
from stock_db.db_stock import StockTransactionTable, StockTransaction
from stock_holding_algorithm.simple_algorithm import SimpleAlgorithm

class SuggestionFrame(Frame):
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

        self.lblCurrentPrice = Label(self)
        self.lblCurrentPrice["text"] = "Current price:"
        self.lblCurrentPrice.grid(row = 1, column = 0)
        self.entryCurrentPrice = Entry(self)
        self.entryCurrentPrice.grid(row = 1, column = 1)

        self.lblStartPrice = Label(self)
        self.lblStartPrice["text"] = "Start price:"
        self.lblStartPrice.grid(row = 2, column = 0)
        self.entryStartPrice = Entry(self)
        self.entryStartPrice.grid(row = 2, column = 1)

        self.lblStopPrice = Label(self)
        self.lblStopPrice["text"] = "Stop price:"
        self.lblStopPrice.grid(row = 3, column = 0)
        self.entryStopPrice = Entry(self)
        self.entryStopPrice.grid(row = 3, column = 1)

        self.btnSuggest = Button(self)
        self.btnSuggest["text"] = "Suggest"
        self.btnSuggest.grid(row = 4, column = 0)
        self.btnSuggest["command"] = self.suggest_stock

        self.btnCancel = Button(self)
        self.btnCancel["text"] = "Cancel"
        self.btnCancel.grid(row = 4, column = 1)
        self.btnCancel["command"] = self.quit_dialog

        self.txtSuggestion = Text(self)
        self.txtSuggestion.grid(row = 5, column = 0, columnspan = 2)
        self.set_text("")

        return

    def set_text(self, text):
        self.txtSuggestion["state"] = NORMAL
        self.txtSuggestion.delete("0.0", END)
        self.txtSuggestion.insert(INSERT, text)
        self.txtSuggestion["state"] = DISABLED
        return

    def get_result(self):
        return 1000

    def fill_symbol_combobox(self):
        stock_cash_table = StockCashTable()
        stock_cash_list = stock_cash_table.get_all_stock_cash()
        symbol_list = []
        for stock_cash in stock_cash_list:
            symbol_list.append(stock_cash.get_symbol())
        self.cbbSymbol["values"] = symbol_list
        return

    def suggest_stock(self):
        symbol = self.cbbSymbol.get()
        if (not symbol):
            self.set_text("Symbol is empty.")
            return
        start_price = float(self.entryStartPrice.get())
        stop_price = float(self.entryStopPrice.get())
        current_price = float(self.entryCurrentPrice.get())

        simple_algorithm = SimpleAlgorithm(symbol, start_price, stop_price,
                                           current_price)
        simple_algorithm.calculate()

        buy_or_sell = simple_algorithm.get_suggested_buy_or_sell()
        suggested_amount = simple_algorithm.get_suggested_amount()

        result = "Buy or Sell: {0}\nAmount: {1}".format(buy_or_sell,
                                                        suggested_amount)
        self.set_text(result)

        return

    def quit_dialog(self):
        self.master.destroy()
        return

class SuggestionDialog():
    def __init__(self, master=None):
        self.master = master
        self.root = None

    def open(self):
        self.root = Toplevel()
        self.frame = SuggestionFrame(self.root)
        self.frame.grid(padx = 10, pady = 10)
        self.root.transient(self.master)
        self.root.grab_set()
        self.root.wait_window(self.root)
        result = self.frame.get_result()
        return result
