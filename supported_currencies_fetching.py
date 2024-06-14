# for keeping up to date with currency list ( just in case :) )
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time

chrome = uc.Chrome()

chrome.get("https://cash.rbc.ru/cash/converter.html")
# button = chrome.find_element(by=By.XPATH, value="//div[text()='↓']")
# button.click()
currencies = chrome.find_elements(by=By.CLASS_NAME, value="calc__currency__row")
for currency in currencies:
    print(currency.get_attribute("data-cur"))
