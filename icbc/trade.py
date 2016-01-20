'''
Created on 2016年1月17日

@author: Wenwen
'''
import logging
from selenium import webdriver
import time

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
        self.switch_to_down_frame()
        e = self.driver.find_element_by_id("div_2")
        e = e.find_element_by_id("emall_closebtn")
        e.click()
        time.sleep(2)
        self.switch_to_down_frame()
        e = self.driver.find_element_by_id("div_3")
        e = e.find_element_by_id("emall_closebtn")
        e.click()

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

    def select_inventment(self):
        self.switch_to_top_frame()
        e = self.driver.find_element_by_id("headspan_LV1_99")
        e.click()
        return

    def select_noble_metal(self):
        self.select_inventment()
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
            print(e.text)
            name = e.text
            e = main_transaction_area_element.find_element_by_xpath(
                                                        buying_price_xpath)
            print(e.text)
            buying_price = float(e.text)
            e = main_transaction_area_element.find_element_by_xpath(
                                                        selling_price_xpath)
            print(e.text)
            selling_price = float(e.text)
            noble_metal_price = NobleMetalPrice(name, 
                                                buying_price, 
                                                selling_price)
            noble_metal_price_list.append(noble_metal_price)
        return noble_metal_price_list

    def close(self):
        self.driver.close()
        return

if __name__ == '__main__':
    pass
    