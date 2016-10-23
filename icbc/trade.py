'''
Created on 2016年1月17日

@author: Wenwen
'''
import logging
import time
import re

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

class NobleMetalPrice:
    """
        NobleMetalPrice object
    """
    def __init__(self,
                 name=None,
                 buying_price=None,
                 selling_price=None):
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
        self.driver = webdriver.Ie(log_level=logging.DEBUG, log_file="ie.log")
        self.driver.implicitly_wait(10)
        return

    def login(self):
        print("login")
        self.logger.info("login")
        self.driver.get("https://mybank.icbc.com.cn/icbc/perbank/index.jsp")

        print("Please input user name and password!")
        input("Please press Enter to continue!\n")

        time.sleep(5)

        return

    def main_page(self):
        self.driver.get("https://mybank.icbc.com.cn/icbc/perbank/index.jsp")
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
        self.switch_to_market_frame()
        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.NAME, "_left")))
        return

    def switch_to_main_right_frame(self):
        self.switch_to_market_frame()
        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.NAME, "_right")))
        return

    # confirm transaction frame
    def switch_to_main_manage_p31_frame(self):
        self.switch_to_main_frame()
        manage_p31_frame = self.driver.find_element_by_name("_right")
        self.driver.switch_to.frame(manage_p31_frame)
        return

    # transaction complete frame
    def switch_to_main_manage_p32_frame(self):
        self.switch_to_main_frame()
        manage_p32_frame = self.driver.find_element_by_name("_right")
        self.driver.switch_to.frame(manage_p32_frame)
        return

    def switch_to_market_frame(self):
        self.switch_to_content_frame()
        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.NAME, "_market")))
        return

    def switch_to_content_frame(self):
        self.driver.switch_to_default_content()
        per_bank_content_frame = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "perbank-content-frame")))
        #content_frame = self.driver.find_element_by_id("content-frame")
        self.driver.switch_to.frame(per_bank_content_frame)
        content_frame = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "content-frame")))
        self.driver.switch_to.frame(content_frame)
        return

    def select_investment(self):
        self.switch_to_top_frame()
        e = self.driver.find_element_by_id("headspan_LV1_99")
        e.click()
        print("investment should be clicked")
        return

    def select_noble_metal(self):
        self.driver.switch_to_default_content()

        quanbu_element = self.driver.find_element_by_id("quanbu")
        quanbu_element.click()
        quanbu_element.click()
        #script = 'perbankAtomLocationTW' + \
        #         '("PBL200204","",dse_sessionId)'
        #self.driver.execute_script(script)

        self.switch_to_content_frame()

        noble_metal_xpath = "html/body/div/div/div[6]" + \
                            "/div/div/div/ul/li[1]/a"
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, noble_metal_xpath)))

        script = 'AtomSerivceSubmit("PBL201311","","","")'
        self.driver.execute_script(script)

        counter = 0
        while counter < 3:
            found_exception = False
            try:
                self.switch_to_content_frame()

                WebDriverWait(self.driver, 10).until(
                    EC.frame_to_be_available_and_switch_to_it(
                        (By.NAME, "_market")))

                WebDriverWait(self.driver, 10).until(
                    EC.frame_to_be_available_and_switch_to_it(
                        (By.NAME, "_left")))

            except StaleElementReferenceException as stale_exception:
                error_msg = "select noble metal: StaleException {0}"
                error_msg = error_msg.format(stale_exception)
                self.logger.error(error_msg)
                print(error_msg)
                found_exception = True
            if not found_exception:
                break
            time.sleep(10)
            counter = counter + 1
        if counter == 3:
            raise StaleElementReferenceException(
                "select noble metal: tried 3 times")
        return

    def _unsafe_get_noble_metal_price_list(self):
        self.switch_to_main_left_frame()
        main_transaction_area_element = self.driver.\
                                        find_element_by_id(
                                            "主交易区")
        # tbody/tr/td/div/table[2]/tbody/tr[1]/td[0]
        noble_metal_price_list = []
        base_table_xpath = "tbody/tr/td/div/table[2]/tbody"
        for i in range(8):
            name_xpath = base_table_xpath + \
                         "/tr[{0}]/td[1]".format(i+2)
            buying_price_xpath = base_table_xpath + \
                                 "/tr[{0}]/td[4]/a/span".\
                                 format(i+2)
            selling_price_xpath = base_table_xpath + \
                                  "/tr[{0}]/td[5]/a/span".\
                                  format(i+2)
            element = main_transaction_area_element.\
                      find_element_by_xpath(
                          name_xpath)
            name = element.text
            element = main_transaction_area_element.\
                      find_element_by_xpath(
                          buying_price_xpath)
            buying_price = float(element.text)
            element = main_transaction_area_element.\
                      find_element_by_xpath(
                          selling_price_xpath)
            selling_price = float(element.text)
            noble_metal_price = NobleMetalPrice(name,
                                                buying_price,
                                                selling_price)
            noble_metal_price_list.append(noble_metal_price)
        return noble_metal_price_list

    def get_noble_metal_price_list(self):
        noble_metal_price_list = None
        counter = 0
        while counter < 3:
            found_exception = False
            try:
                noble_metal_price_list = self.\
                                         _unsafe_get_noble_metal_price_list()
            except StaleElementReferenceException as stale_exception:
                error_msg = "get_noble_metal_price_list: Stale Exception"
                error_msg += "\n{0}".format(stale_exception)
                self.logger.error(error_msg)
                print(error_msg)
                found_exception = True
            if not found_exception:
                break
            counter = counter + 1
            time.sleep(10)
        if counter == 3:
            raise StaleElementReferenceException(
                "get_noble_metal_price_list: Tried 3 times.")
        return noble_metal_price_list

    def get_noble_metal_price(self,name):
        noble_metal_price_list = self.get_noble_metal_price_list()
        for noble_metal_price in noble_metal_price_list:
            if noble_metal_price.name == name:
                return noble_metal_price
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

        script = "form_submit()"
        self.driver.execute_script(script)

        submit_again_xpath = \
            "/html/body/table/tbody/tr/td/form[2]/table[2]/tbody/tr[8]/td/div/a[1]"
        goback_xpath = \
            "/html/body/table/tbody/tr/td/form[2]/table[2]/tbody/tr[8]/td/div/a[2]"
        total_price_xpath = \
            "/html/body/table/tbody/tr/td/form[2]/table[2]/tbody/tr[6]/td[2]/span"
        self.switch_to_main_right_frame()
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

        if (total_price > amount * price):
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

        self.switch_to_main_right_frame()
        complete_xpath = \
            "/html/body/table[2]/tbody/tr/td/div/div[2]/h4/b"
        complete_element = self.driver.find_element_by_xpath(complete_xpath)
        result = complete_element.text
        print(result)
        script = "changedeal_imme('0')"
        self.driver.execute_script(script)
        if (result.find("交易成功") != -1):
            return True
        else:
            raise Exception("Error {0}".format(result))


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

        script = "form_submit()"
        self.driver.execute_script(script)

        submit_again_xpath = \
            "/html/body/table/tbody/tr/td/form[2]/table[2]/tbody/tr[8]/td/div/a[1]"
        goback_xpath = \
            "/html/body/table/tbody/tr/td/form[2]/table[2]/tbody/tr[8]/td/div/a[2]"
        total_price_xpath = \
            "/html/body/table/tbody/tr/td/form[2]/table[2]/tbody/tr[6]/td[2]/span"

        self.switch_to_main_right_frame()
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

        self.switch_to_main_right_frame()
        complete_xpath = \
             "/html/body/table[2]/tbody/tr/td/div/div[2]/h4/b"
        complete_element = self.driver.find_element_by_xpath(complete_xpath)
        result = complete_element.text
        print(result)
        script = "changedeal_imme('0')"
        self.driver.execute_script(script)
        if (result.find("交易成功") != -1):
            return True
        else:
            raise Exception("Error {0}".format(result))

    def close(self):
        self.driver.close()
        return

if __name__ == '__main__':
    pass
