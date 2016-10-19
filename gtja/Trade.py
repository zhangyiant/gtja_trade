'''
Created on Jul 8, 2015

@author: yizhang
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
import time
import logging
from datetime import datetime

class CurrentCommissionInfo:
    def __init__(self):
        self.shareholder_code = ""
        self.commission_id = ""
        self.stock_symbol = ""
        self.stock_name = ""
        self.type = ""
        self.price = 0.0
        self.amount = 0
        self.datetime = datetime(1900,1,1)
        self.trade_volumn = 0
        self.trade_state = ""
        return
    
    def __str__(self):
        result = "shareholder_code: " + self.shareholder_code
        result += ", commission_id: {0}".format(self.commission_id)
        result += ", stock_symbol: {0}".format(self.stock_symbol)
        result += ", stock_name: {0}".format(self.stock_name)
        result += ", type: " + self.type
        result += ", price: {0}".format(self.price)
        result += "., amount: {0}".format(self.amount)
        result += ", datetime: {0}".format(self.datetime)
        result += ", trade_volumn: {0}".format(self.trade_volumn)
        result += ", trade_state: {0}".format(self.trade_state)
        return result
    
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
        result += ",actual_amount: {0}".format(self.actual_amount)
        result += ",available_amount: {0}".format(self.available_amount)
        result += ",value: {0}".format(self.value)
        result += ",price: {0}".format(self.price)
        result += ",cost: {0}".format(self.cost)
        result += ",gain: {0}".format(self.gain)
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
        result += ",cash_balance: {0}".format(self.cash_balance)
        result += ",available_balance: {0}".format(self.available_balance)
        result += ",extractable_balance: {0}".format(self.extractable_balance)
        result += ",current_value: {0}".format(self.current_value)
        result += ",total_value: {0}".format(self.total_value)
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
        self.logger = logging.getLogger(__name__)
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        return

    def is_alert_present(self):
        try:
            alert = self.driver.switch_to.alert
            alert.text
            return True
        except NoAlertPresentException:
            return False
    
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
    
    def get_stock_info_list(self):
        
        self.enter_stock_menu()

        time.sleep(3)

        self.select_main_frame()
        
        tbody_xpath = '//body/table[3]/tbody/tr/td/table[4]/tbody'
        
        tbody_element = self.driver.find_element_by_xpath(tbody_xpath)
        
        row_elements = tbody_element.find_elements_by_xpath("*")

        stock_info_list = []
        for row_element in row_elements[1:-1]:
            column_elements = row_element.find_elements_by_tag_name("td")
            stock_info = StockInfo()
            stock_info.stock_symbol = column_elements[1].text
            stock_info.stock_name = column_elements[2].text
            stock_info.actual_amount = column_elements[3].text
            stock_info.available_amount = column_elements[4].text
            stock_info.value = column_elements[5].text
            stock_info.price = column_elements[6].text
            stock_info.cost = column_elements[7].text
            stock_info.gain = column_elements[8].text
            stock_info_list.append(stock_info)
            
        return stock_info_list
    
    def get_account_info(self):
        
        # enter stock menu
        self.enter_stock_menu()
        time.sleep(3)
        
        self.select_main_frame()
        
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
        
        self.select_top_frame()
        
        stock_menu_element = self.driver.find_element_by_xpath('//a[@title="股票"]')
        
        print(stock_menu_element.text)
        
        stock_menu_element.click()
        
        return
    
    def select_main_frame(self):
        
        # wait the main frame is ready
        self.driver.switch_to.default_content()
        element = WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.NAME, "mainFrame"))
            )
        
        # switch to the main frame
        self.driver.switch_to.default_content()
        main_frame = self.driver.find_element_by_name("mainFrame")
        self.driver.switch_to.frame(main_frame)
        return
    
    def select_top_frame(self):
        self.driver.switch_to.default_content()
        top_frame = self.driver.find_element_by_name("topFrame")
        self.driver.switch_to.frame(top_frame)
        return
    
    def select_left_frame(self):
        # wait the main frame is ready
        self.driver.switch_to.default_content()
        element = WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.NAME, "leftFrame"))
            )
        
        # switch to left frame
        self.driver.switch_to.default_content()
        left_frame = self.driver.find_element_by_name("leftFrame")
        self.driver.switch_to.frame(left_frame)
        return
    
    def select_menu_frame(self):
        self.select_left_frame()
        
        element = WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.NAME, "menuiframe"))
            )
#         menu_frame = self.driver.find_element_by_name("menuiframe")
#         self.driver.switch_to.frame(menu_frame)
        return
        
    def get_stock_price(self, symbol):
        symbol_input_xpath = "/html/body/form/table[3]/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr/td/table[1]/tbody/tr[1]/td[2]/input"
        refresh_xpath = "/html/body/form/table[3]/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr/td/table[1]/tbody/tr[1]/td[2]/span/a"
        price_xpath = "/html/body/form/table[3]/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr/td/table[1]/tbody/tr[4]/td[2]"
        
        self.enter_stock_menu()
        time.sleep(3)
        self.select_menu_frame()
        element = self.driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[1]/td/a")
        element.click()
        time.sleep(3)
        
        self.select_main_frame()
        element = self.driver.find_element_by_xpath(symbol_input_xpath)
        element.send_keys(symbol)
        time.sleep(3)
        element = self.driver.find_element_by_xpath(refresh_xpath)
        element.click()
        time.sleep(3)
        
        # wait the price is not 0
        WebDriverWait(self.driver, 10).until_not(
            EC.text_to_be_present_in_element_value((By.XPATH, price_xpath), "0")
            )

        element = self.driver.find_element_by_xpath(price_xpath)
        
        if element.text == "0":
            self.logger.critical("Price is 0")

        price = float(element.text)
        
        return price
    
    def get_commission_state(self, commission_id):
        commission_list = self.get_current_commission_list()
        found = False
        for commission in commission_list:
            if (commission.commission_id == commission_id):
                found = True
                break
        if (found):
            return commission.trade_state
        else:
            return "Error"
    
    def cancel_commission(self, commission_id):
        current_commission_xpath = "/html/body/table[2]/tbody/tr[6]/td/table/tbody/tr[3]/td[3]/a"
        current_commission_table_tbody_xpath = "/html/body/table[3]/tbody/tr/td/table[4]/tbody"
        
        self.enter_stock_menu()
        time.sleep(3)
        self.select_menu_frame()
        
        element = self.driver.find_element_by_xpath(current_commission_xpath)
        element.click()
        
        self.select_main_frame()

        tbody_element = self.driver.find_element_by_xpath(current_commission_table_tbody_xpath)
        
        row_elements = tbody_element.find_elements_by_xpath("*")

        found = False
        for row_element in row_elements[1:-1]:
            column_elements = row_element.find_elements_by_tag_name("td")
            row_commission_id = int(column_elements[2].text)
            row_commission_state = column_elements[10].text
            if (row_commission_id == commission_id):
                # we find the row
                found = True
                break
        
        result = 0
        if found:
            if row_commission_state == "已成" or \
                    row_commission_state == "废单":
                result = 0
            else:
                operation_element = column_elements[0]
                cancel_element = \
                    operation_element.find_element_by_tag_name("a")
                cancel_element.click()
                if (self.is_alert_present()):
                    alert = self.driver.switch_to.alert
                    print(alert.text)
                    alert.accept()
                    if (self.is_alert_present()):
                        alert = self.driver.switch_to.alert
                        print(alert.text)
                        alert.accept()
                result = 1
        else:
            print("Error, cannot find the element to cancel!")

        return result

    def get_current_commission_list(self):
        curr_commission_xpath = "/html/body/table[2]" + \
                                   "/tbody/tr[6]/td/table/tbody/tr[3]/td[3]/a"
        curr_commission_tbody_xpath = "/html/body/table[3]" + \
                                               "/tbody/tr/td/table[4]/tbody"
        test_xpath = curr_commission_tbody_xpath + \
                     "/tr[1]/td[2]/div"
        test_value = "股东代码"

        self.enter_stock_menu()
        time.sleep(3)
        self.select_menu_frame()

        time.sleep(3)

        element = self.driver.find_element_by_xpath(curr_commission_xpath)
        element.click()

        self.select_main_frame()
        WebDriverWait(self.driver, 20).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, test_xpath),
                test_value))

        self.select_main_frame()

        tbody_element = self.driver.find_element_by_xpath(curr_commission_tbody_xpath)
        row_elements = tbody_element.find_elements_by_xpath("*")

        current_commission_list = []
        for row_element in row_elements[1:-1]:
            column_elements = row_element.find_elements_by_tag_name("td")
            current_commission_info = CurrentCommissionInfo()
            current_commission_info.shareholder_code = column_elements[1].text
            current_commission_info.commission_id = int(column_elements[2].text)
            current_commission_info.stock_symbol = column_elements[3].text
            current_commission_info.stock_name = column_elements[4].text
            current_commission_info.type = column_elements[5].text
            current_commission_info.price = float(column_elements[6].text)

            current_commission_info.amount = int(float(column_elements[7].text))
            datetime_string = column_elements[8].text
            year = int(datetime_string[0:4])
            month = int(datetime_string[4:6])
            day = int(datetime_string[6:8])
            hour = int(datetime_string[8:10])
            minute = int(datetime_string[10:12])
            second = int(datetime_string[12:14])
            try:
                current_commission_info.datetime = datetime(year,month,day,hour,minute,second)
            except:
                print("Commission Info DateTime Error: {0}".format(datetime_string))
                current_commission_info.datetime = datetime.now()
            current_commission_info.trade_volumn = int(column_elements[9].text)
            current_commission_info.trade_state = column_elements[10].text
            current_commission_list.append(current_commission_info)

        return current_commission_list
    
    def buy_stock(self, symbol, price, amount):
        symbol_input_xpath = "/html/body/form/table[3]/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr/td/table[1]/tbody/tr[1]/td[2]/input"
        refresh_xpath = "/html/body/form/table[3]/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr/td/table[1]/tbody/tr[1]/td[2]/span/a"
        buy_price_xpath = "/html/body/form/table[3]/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr/td/table[1]/tbody/tr[7]/td[2]/input"
        buy_amount_xpath = "/html/body/form/table[3]/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr/td/table[1]/tbody/tr[10]/td[2]/input"
        buy_button_xpath = "/html/body/form/table[3]/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr/td/table[2]/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td/input"
        normal_delegate_xpath = "/html/body/form/table[3]/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr/td/table[1]/tbody/tr[5]/td[2]/input[1]"
        
        self.enter_stock_menu()
        time.sleep(3)
        self.select_menu_frame()
        element = self.driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[1]/td/a")
        element.click()
        time.sleep(5)
        
        self.select_main_frame()
        element = self.driver.find_element_by_xpath(symbol_input_xpath)
        element.send_keys(symbol)
        
        element = self.driver.find_element_by_xpath(refresh_xpath)
        element.click()
        time.sleep(3)
        
        element = self.driver.find_element_by_xpath(normal_delegate_xpath)
        element.click()
        
        element = self.driver.find_element_by_xpath(buy_price_xpath)
        element.clear()
        element.send_keys("{0}".format(price))
        
        element = self.driver.find_element_by_xpath(buy_amount_xpath)
        element.send_keys("{0}".format(amount))
        
        element = self.driver.find_element_by_xpath(buy_button_xpath)
        element.click()
        
        if (self.is_alert_present()):
            alert = self.driver.switch_to.alert
            print(alert.text)
            alert.accept()
            if (self.is_alert_present()):
                alert = self.driver.switch_to.alert
                print(alert.text)
                alert.accept()

        curr_datetime = datetime.now()
        print(curr_datetime)
        
        commission_id = self.get_last_commission_id(symbol, amount)
        
        print(commission_id)
        
        return commission_id       

    def sell_stock(self, symbol, price, amount):
        symbol_input_xpath = "/html/body/form/table[3]/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr/td/table[1]/tbody/tr[1]/td[2]/input"
        refresh_xpath = "/html/body/form/table[3]/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr/td/table[1]/tbody/tr[1]/td[2]/span/a"
        sell_price_xpath = "/html/body/form/table[3]/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr/td/table[1]/tbody/tr[6]/td[2]/input"
        sell_amount_xpath = "/html/body/form/table[3]/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr/td/table[1]/tbody/tr[8]/td[2]/input"
        sell_button_xpath = "/html/body/form/table[3]/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr/td/table[2]/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td/input"
        normal_delegate_xpath = "/html/body/form/table[3]/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr/td/table[1]/tbody/tr[4]/td[2]/input[1]"

        self.enter_stock_menu()
        time.sleep(3)
        self.select_menu_frame()
        element = self.driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[2]/td/a")
        element.click()
        time.sleep(3)
        
        self.select_main_frame()
        element = self.driver.find_element_by_xpath(symbol_input_xpath)
        element.send_keys(symbol)
        
        element = self.driver.find_element_by_xpath(refresh_xpath)
        element.click()
        time.sleep(3)
        
        element = self.driver.find_element_by_xpath(normal_delegate_xpath)
        element.click()
        
        element = self.driver.find_element_by_xpath(sell_price_xpath)
        element.clear()
        element.send_keys("{0}".format(price))
        
        element = self.driver.find_element_by_xpath(sell_amount_xpath)
        element.send_keys("{0}".format(amount))
        
        element = self.driver.find_element_by_xpath(sell_button_xpath)
        element.click()
         
        if (self.is_alert_present()):
            alert = self.driver.switch_to.alert
            print(alert.text)
            alert.accept()
            if (self.is_alert_present()):
                alert = self.driver.switch_to.alert
                print(alert.text)
                alert.accept()
 
        curr_datetime = datetime.now()
        print(curr_datetime)
         
        commission_id = self.get_last_commission_id(symbol, amount)
         
        print(commission_id)
         
        return commission_id       
    
    def get_last_commission_id(self, symbol, amount):
        commission_list = self.get_current_commission_list()
        
        commission = commission_list[-1]
        print(commission)
        if (commission.stock_symbol == symbol and commission.amount == amount):
            return commission.commission_id
        else:
            return ""
           
    def close(self):
        self.driver.close()
