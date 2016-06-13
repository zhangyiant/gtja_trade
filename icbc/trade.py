'''
Created on 2016年1月17日

@author: Wenwen
'''
import logging
from selenium import webdriver
import time
import re

class NobleMetalPrice:
    def __init__(self, 
                 name = None, 
                 buying_price = None, 
                 selling_price = None):
        self.name = name
        self.buying_price = buying_price
        self.selling_price = selling_price
        return

    def __str__(self):
        result = "Name: {0}, buying price: {1}, selling_price: {2}".format(
                                                        self.name,
                                                        self.buying_price,
                                                        self.selling_price)
        return result

class Trade:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.logger = logging.getLogger(__name__)
        self.driver = webdriver.Ie()
        return

    def login(self):
        print("login")
        self.logger.info("login")
        self.driver.get("https://mybank.icbc.com.cn/icbc/perbank/index.jsp")

        print("Please input user name and password!")
        print("Please choose 简约版.")
        input("Please press Enter to continue!\n")

        # remove the 2 Ads after logging
        '''
        self.switch_to_down_frame()
        e = self.driver.find_element_by_id("div_2")
        e = e.find_element_by_id("emall_closebtn")
        e.click()
        time.sleep(2)
        self.switch_to_down_frame()
        e = self.driver.find_element_by_id("div_3")
        e = e.find_element_by_id("emall_closebtn")
        e.click()
        '''
        return

    def switch_to_top_frame(self):
        self.driver.switch_to_default_content()
        index_frame = self.driver.find_element_by_name("indexFrame")
        self.driver.switch_to.frame(index_frame)
        top_frame = self.driver.find_element_by_name("topFrame")
        self.driver.switch_to.frame(top_frame)
        return
    
    def switch_to_down_frame(self):
        self.driver.switch_to_default_content()
        index_frame = self.driver.find_element_by_name("indexFrame")
        self.driver.switch_to.frame(index_frame)
        down_frame = self.driver.find_element_by_name("downFrame")
        self.driver.switch_to.frame(down_frame)
        return
    
    def switch_to_left_frame(self):
        self.switch_to_down_frame()
        left_frame = self.driver.find_element_by_name("leftFrame")
        self.driver.switch_to.frame(left_frame)
        return 
    
    def switch_to_main_frame(self):
        self.switch_to_down_frame()
        main_frame = self.driver.find_element_by_name("mainFrame")
        self.driver.switch_to.frame(main_frame)
        return

    def switch_to_main_left_frame(self):
        self.switch_to_main_frame()
        left_frame = self.driver.find_element_by_name("_left")
        self.driver.switch_to.frame(left_frame)
        return

    def switch_to_main_right_frame(self):
        self.switch_to_main_frame()
        right_frame = self.driver.find_element_by_name("_right")
        self.driver.switch_to.frame(right_frame)
        return
    
    # confirm transaction frame
    def switch_to_main_manage_p31_frame(self):
        self.switch_to_main_frame()
        manage_p31_frame = self.driver.find_element_by_name("manage_p31")
        self.driver.switch_to.frame(manage_p31_frame)
        return
    
    # transaction complete frame
    def switch_to_main_manage_p32_frame(self):
        self.switch_to_main_frame()
        manage_p32_frame = self.driver.find_element_by_name("manage_p32")
        self.driver.switch_to.frame(manage_p32_frame)
        return

    def select_investment(self):
        self.switch_to_top_frame()
        e = self.driver.find_element_by_id("headspan_LV1_99")
        e.click()
        print("investment should be clicked")
        return

    def select_noble_metal(self):
        self.select_investment()
        time.sleep(2)
        self.switch_to_top_frame()
        e = self.driver.find_element_by_id("headspan_LV2_16")
        e.click()
        return

    def get_noble_metal_price_list(self):
        self.switch_to_main_left_frame()
        main_transaction_area_element = self.driver.find_element_by_id("主交易区")
        # tbody/tr/td/table[1]/tbody/tr[1]/td[0]
        noble_metal_price_list = []
        for i in range(8):
            name_xpath = "tbody/tr/td/table[2]/tbody/tr[{0}]/td[1]".format(i+2)
            buying_price_xpath = \
                "tbody/tr/td/table[2]/tbody/tr[{0}]/td[3]/a/span".format(i+2)
            selling_price_xpath = \
                "tbody/tr/td/table[2]/tbody/tr[{0}]/td[4]/a/span".format(i+2)
            e = main_transaction_area_element.find_element_by_xpath(
                                                                name_xpath)
            name = e.text
            e = main_transaction_area_element.find_element_by_xpath(
                                                        buying_price_xpath)
            buying_price = float(e.text)
            e = main_transaction_area_element.find_element_by_xpath(
                                                        selling_price_xpath)
            selling_price = float(e.text)
            noble_metal_price = NobleMetalPrice(name,
                                                buying_price,
                                                selling_price)
            noble_metal_price_list.append(noble_metal_price)
        return noble_metal_price_list

    def get_nobal_metal_price(self,name):
        nobal_metal_price_list = self.get_noble_metal_price_list()
        for nobal_metal_price in nobal_metal_price_list:
            if nobal_metal_price.name == name:
                return nobal_metal_price
        return None

    def buy_noble_metal(self, name, amount, price):
        name_xpath = "tbody/tr/td[2]/select"
        buy_radio_xpath = "tbody/tr[5]/td[2]/div[1]/input"
        amount_xpath = "tbody/tr[9]/td[2]/input"
        submit_xpath = "tbody/tr[16]/td[1]/a"
        self.switch_to_main_right_frame()
        main_table_element = self.driver.find_element_by_id("maintable")
        name_element = \
            main_table_element.find_element_by_xpath(name_xpath)
        name_element.send_keys(name)
        buy_radio_element = \
            main_table_element.find_element_by_xpath(buy_radio_xpath)
        buy_radio_element.click()
        amount_element = \
            main_table_element.find_element_by_xpath(amount_xpath)
        amount_element.send_keys(str(amount))
        submit_element = \
            main_table_element.find_element_by_xpath(submit_xpath)
        submit_element.click()

        submit_again_xpath = \
            "/html/body/form[2]/table[2]/tbody/tr[9]/td/div/a[1]"
        goback_xpath = \
            "/html/body/form[2]/table[2]/tbody/tr[9]/td/div/a[2]"
        total_price_xpath = \
            "/html/body/form[2]/table[2]/tbody/tr[7]/td[2]"
        self.switch_to_main_manage_p31_frame()
        total_price_element = self.driver.find_element_by_xpath(
                                                    total_price_xpath)
        print(total_price_element.text)
        t = re.compile("(\d+,)*\d+\.\d+")
        m = t.match(total_price_element.text)
        total_price_string = m.group()
        total_price_string = total_price_string.replace(",", "")
        total_price = float(total_price_string)
        print(total_price)
        print(amount * price)
        if(total_price > amount * price):
            goback_element = self.driver.find_element_by_xpath(goback_xpath)
            goback_element.click()
            return False
        #else:
        #    goback_element = self.driver.find_element_by_xpath(goback_xpath)
        #    goback_element.click()
        #    return True

        submit_again_element = self.driver.find_element_by_xpath(
                                                        submit_again_xpath)
        submit_again_element.click()

        self.switch_to_main_manage_p32_frame()
        complete_xpath = \
            "/html/body/table[3]/tbody/tr/td/table/tbody/tr[2]/td"
        complete_element = self.driver.find_element_by_xpath(complete_xpath)
        result = complete_element.text
        print(result)
        if(result.find("已成交") != -1):
            return True
        else:
            return False

    def sell_noble_metal(self, name, amount, price):
        name_xpath = "tbody/tr/td[2]/select"
        sell_radio_xpath = "tbody/tr[5]/td[2]/div[2]/input"
        amount_xpath = "tbody/tr[9]/td[2]/input"
        submit_xpath = "tbody/tr[16]/td[1]/a"
        self.switch_to_main_right_frame()
        main_table_element = self.driver.find_element_by_id("maintable")
        name_element = \
            main_table_element.find_element_by_xpath(name_xpath)
        name_element.send_keys(name)
        buy_radio_element = \
            main_table_element.find_element_by_xpath(sell_radio_xpath)
        buy_radio_element.click()
        amount_element = \
            main_table_element.find_element_by_xpath(amount_xpath)
        amount_element.send_keys(str(amount))
        submit_element = \
            main_table_element.find_element_by_xpath(submit_xpath)
        submit_element.click()

        submit_again_xpath = \
            "/html/body/form[2]/table[2]/tbody/tr[9]/td/div/a[1]"
        goback_xpath = \
            "/html/body/form[2]/table[2]/tbody/tr[9]/td/div/a[2]"
        total_price_xpath = \
            "/html/body/form[2]/table[2]/tbody/tr[7]/td[2]"
        self.switch_to_main_manage_p31_frame()
        total_price_element = self.driver.find_element_by_xpath(
                                                    total_price_xpath)
        print(total_price_element.text)
        t = re.compile("(\d+,)*\d+\.\d+")
        m = t.match(total_price_element.text)
        total_price_string = m.group()
        total_price_string = total_price_string.replace(",", "")
        total_price = float(total_price_string)
        if(total_price < amount * price):
            goback_element = self.driver.find_element_by_xpath(goback_xpath)
            goback_element.click()
            return False
        #else:
        #    goback_element = self.driver.find_element_by_xpath(goback_xpath)
        #    goback_element.click()
        #    return True

        submit_again_element = self.driver.find_element_by_xpath(
                                                        submit_again_xpath)
        submit_again_element.click()

        self.switch_to_main_manage_p32_frame()
        complete_xpath = \
            "/html/body/table[3]/tbody/tr/td/table/tbody/tr[2]/td"
        complete_element = self.driver.find_element_by_xpath(complete_xpath)
        result = complete_element.text
        print(result)
        if(result.find("已成交") != -1):
            return True
        else:
            return False

    def close(self):
        self.driver.close()
        return

if __name__ == '__main__':
    pass
