'''
Created on 2016年1月17日

@author: Wenwen
'''
import logging
from selenium import webdriver
import time

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
        input("Please press Enter to continue!")

        # remove the 2 Ads after logging
        self.driver.switch_to_default_content()
        index_frame = self.driver.find_element_by_name("indexFrame")
        self.driver.switch_to.frame(index_frame)
        down_frame = self.driver.find_element_by_name("downFrame")
        self.driver.switch_to.frame(down_frame)
        e = self.driver.find_element_by_id("emall_closebtn")
        e.click()
        time.sleep(3)
        self.driver.switch_to_default_content()
        index_frame = self.driver.find_element_by_name("indexFrame")
        self.driver.switch_to.frame(index_frame)
        down_frame = self.driver.find_element_by_name("downFrame")
        self.driver.switch_to.frame(down_frame)
        e = self.driver.find_element_by_id("div_3")
        e = e.find_element_by_id("emall_closebtn")
        e.click()

        return

    def close(self):
        self.driver.close()
        return

if __name__ == '__main__':
    pass
    