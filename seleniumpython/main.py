'''
Created on 年

@author: Wenwen
'''
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException

driver = webdriver.Firefox()
driver.get("http://trade.gtja.com")


def is_alert_present(driver):
    
    try:
        alert = driver.switch_to.alert
        alert.text
        return alert
    except NoAlertPresentException:
        return False

print(is_alert_present(driver))
    
driver.close()
