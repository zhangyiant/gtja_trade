'''
Created on Jul 8, 2015

@author: yizhang
'''
from selenium import webdriver
import time

class StockInfo:
    def __init__(self):
        self.stock_symbol = ""
        self.stock_name = ""
        self.actual_amount = 0
        self.available_amount = 0
        self.value = 0
        self.price = 0
        self.cost = 0
        self.gain = 0
        return
    
    def __str__(self):
        result = "stock_symbol: " + self.stock_symbol
        result += ",stock_name: " + self.stock_name
        result += ",actual_amount: "  + self.actual_amount
        result += ",available_amount: " + self.available_amount
        result += ",value: " + self.value
        result += ",price: " + self.price
        result += ",cost: " + self.cost
        result += ",gain: " + self.gain
        return result    
    
class AccountInfo:
    def __init__(self):
        self.account_name = ""
        self.currency = ""
        self.cash_balance = 0
        self.available_balance = 0
        self.extractable_balance = 0
        self.current_value = 0
        self.total_value = 0
        self.bank_name = ""
        return
    
    def __str__(self):
        result = "account_name: " + self.account_name
        result += ", currency: " + self.currency
        result += ",cash_balance: " + self.cash_balance
        result += ",available_balance: " + self.available_balance
        result += ",extractable_balance: " + self.extractable_balance
        result += ",current_value: " + self.current_value
        result += ",total_value: " + self.total_value
        result += ",bank_name: " + self.bank_name
        return result

class Trade:
    '''
    classdocs
    '''


    def __init__(self, username, password):
        '''
        Constructor
        '''
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()
        return

        
    def login(self):
        self.driver.get("http://trade.gtja.com")
        print(self.driver.title)
        element = self.driver.find_element_by_partial_link_text("标准")
        element.click()
        
        time.sleep(3)
        
        element = self.driver.find_element_by_name("BranchCode")
        element.send_keys("上海宜山路")
        
        element = self.driver.find_element_by_name("inputid")
        element.send_keys(self.username)
        
        element = self.driver.find_element_by_name("trdpwd")
        element.send_keys(self.password)
        
        validation_code = input("Please input the validation code:\n")
        print("Validation code, ", validation_code)
        
        element = self.driver.find_element_by_name("AppendCode")
        element.send_keys(validation_code)
        
        element = self.driver.find_element_by_id("confirmBtn")
        element.click()
        
        return
    
    def get_stock_info(self):
        
        self.enter_stock_menu()

        time.sleep(3)

        self.driver.switch_to.default_content()
        
        main_frame = self.driver.find_element_by_name("mainFrame")
        self.driver.switch_to.frame(main_frame)
        
        #element = driver.find_element_by_xpath("//body/table[3]")
        row_prefix = "//body/table[3]/tbody/tr/td/table[4]/tbody/tr[2]/td"
        stock_symbol_xpath = row_prefix + "[2]"
        stock_name_xpath = row_prefix + "[3]"
        actual_amount_xpath = row_prefix + "[4]"
        available_amount_xpath = row_prefix + "[5]"
        value_xpath = row_prefix + "[6]"
        price_xpath = row_prefix + "[7]"
        cost_xpath = row_prefix + "[8]"
        gain_xpath = row_prefix + "[9]"
        
        stock_info = StockInfo()
        element = self.driver.find_element_by_xpath(stock_symbol_xpath)
        stock_info.stock_symbol = element.text
        element = self.driver.find_element_by_xpath(stock_name_xpath)
        stock_info.stock_name = element.text
        element = self.driver.find_element_by_xpath(actual_amount_xpath)
        stock_info.actual_amount = element.text
        element = self.driver.find_element_by_xpath(available_amount_xpath)
        stock_info.available_amount = element.text
        element = self.driver.find_element_by_xpath(value_xpath)
        stock_info.value = element.text
        element = self.driver.find_element_by_xpath(price_xpath)
        stock_info.price = element.text
        element = self.driver.find_element_by_xpath(cost_xpath)
        stock_info.cost = element.text
        element = self.driver.find_element_by_xpath(gain_xpath)
        stock_info.gain = element.text
        
        return stock_info
                   
    def get_account_info(self):
        
        # enter stock menu
        self.enter_stock_menu()
        time.sleep(3)
        
        self.driver.switch_to.default_content()
        
        main_frame = self.driver.find_element_by_name("mainFrame")
        self.driver.switch_to.frame(main_frame)
        
        #element = driver.find_element_by_xpath("//body/table[3]")
        row_prefix = "//body/table[3]/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td"
        account_xpath = row_prefix + "[1]"
        currency_xpath = row_prefix + "[2]"
        cash_balance_xpath = row_prefix + "[3]"
        available_balance_xpath = row_prefix + "[4]" 
        extactable_balance_xpath = row_prefix + "[5]"
        current_value_xpath = row_prefix + "[6]"
        total_value_xpath = row_prefix + "[7]"
        bank_name_xpath = row_prefix + "[8]"
        
        account_info = AccountInfo()
        element = self.driver.find_element_by_xpath(account_xpath)
        account_info.account_name = element.text
        element = self.driver.find_element_by_xpath(currency_xpath)
        account_info.currency = element.text
        element = self.driver.find_element_by_xpath(cash_balance_xpath)
        account_info.cash_balance = element.text
        element = self.driver.find_element_by_xpath(available_balance_xpath)
        account_info.available_balance = element.text
        element = self.driver.find_element_by_xpath(extactable_balance_xpath)
        account_info.extractable_balance = element.text
        element = self.driver.find_element_by_xpath(current_value_xpath)
        account_info.current_value = element.text
        element = self.driver.find_element_by_xpath(total_value_xpath)
        account_info.total_value = element.text
        element = self.driver.find_element_by_xpath(bank_name_xpath)
        account_info.bank_name = element.text
        
        return account_info
    
    def enter_stock_menu(self):
        
        self.driver.switch_to.default_content()
        
        top_frame = self.driver.find_element_by_name("topFrame")
        self.driver.switch_to.frame(top_frame)
        
        stock_menu_element = self.driver.find_element_by_xpath('//a[@title="股票"]')
        
        print(stock_menu_element.text)
        
        stock_menu_element.click()
        
        return
    
    def close(self):
        self.driver.close()
