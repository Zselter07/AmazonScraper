from utils.selenium_wrapper.Selenium import Selenium
import time
import os

def get_affiliate_links(asin):

    user_id = 'amazon'
    amazon_url = 'https://affiliate-program.amazon.com/'

    browser = Selenium(user_id)

    browser.driver.get(amazon_url)
    time.sleep(1)

    browser.load_cookies()
    time.sleep(1.5)
    browser.driver.refresh()
    time.sleep(1)
    
    asin_box = browser.driver.find_element_by_id("ac-quicklink-search-product-field")
    asin_box.click()
    asin_box.send_keys(asin)
    time.sleep(1)

    go_button = browser.driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div/div/form/div[2]/span/span/span/input")
    go_button.click()
    time.sleep(3.5)

    get_link_button = browser.driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div/div/div[2]/table/tbody/tr/td[3]/div/span[1]/span/a")
    get_link_button.click()
    time.sleep(3)

    text_only_button = browser.driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div[2]/div/div[1]/ul/span[2]/li/a")
    text_only_button.click()
    time.sleep(2)

    affiliate_link_element = browser.driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/div/a")
    affiliate_link = affiliate_link_element.get_attribute('href')

    time.sleep(0.5)
    browser.driver.quit()

    return affiliate_link

