'''
Created on 年

@author: Wenwen
'''
from selenium import webdriver
import time
import csv

with open("account_info.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        account_name = row[0]
        password = row[1]
        break


driver = webdriver.Firefox()
driver.get("http://trade.gtja.com")
print(driver.title)

element = driver.find_element_by_partial_link_text("标准")
element.click()

element = driver.find_element_by_name("BranchCode")
element.send_keys("上海宜山路")

element = driver.find_element_by_name("inputid")
element.send_keys(account_name)

element = driver.find_element_by_name("trdpwd")
element.send_keys(password)

validation_code = input("Please input the validation code:\n")
print("Validation code, ", validation_code)

element = driver.find_element_by_name("AppendCode")
element.send_keys(validation_code)

element = driver.find_element_by_id("confirmBtn")
element.click()

time.sleep(5)

main_frame = driver.find_element_by_name("mainFrame")
driver.switch_to.frame(main_frame)

#element = driver.find_element_by_xpath("//body/table[3]")
row_prefix = "//body/table[3]/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td"
account_xpath = row_prefix + "[1]"
currency_type = row_prefix + "[2]"
element = driver.find_element_by_xpath(account_xpath)
print(element.text)
element = driver.find_element_by_xpath(currency_type)
print(element.text)
driver.close()
