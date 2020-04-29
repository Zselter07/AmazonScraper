from utils.selenium_wrapper.Selenium import Selenium
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By

import time
import os
# from . import sh

def upload(video_path, video_title, video_description, video_tags, host=None, port=None):
    user_id = 'youtube'
    yt_url = 'https://www.youtube.com'
    yt_upload = 'https://www.youtube.com/upload'

    browser = Selenium(user_id, host = host, port = port)

    browser.driver.get(yt_url)
    time.sleep(1.5)
    browser.load_cookies()
    time.sleep(1.5)
    browser.driver.refresh()
    time.sleep(2)

    buttons_container = browser.find(By.ID, 'buttons')
    browser.find(By.CLASS_NAME, 'style-scope yt-icon-button', element=buttons_container).click()
    print('clicked camera icon')
    browser.save_cookies()
    time.sleep(2)

    browser.driver.get(yt_upload)
    print('refreshed page and logged in')

    browser.find(By.XPATH, "//input[@type='file']").send_keys(video_path)
    print('uploaded video')

    title = browser.find(By.ID, 'textbox')
    title.click()
    title.clear()
    title.send_keys(video_title)
    print('added title')

    i=0

    while True:
        try:
            upload_status = browser.find(By.XPATH, '/html/body/ytcp-uploads-dialog/paper-dialog/div/ytcp-animatable[2]/div/div[1]/ytcp-video-upload-progress/span').text
        except:
            i += 1

            if i >= 4:
                raise
                    
            continue
        
        if 'processed' in upload_status:
            break
        
        time.sleep(0.25)

    description_main = browser.find(By.XPATH, "/html/body/ytcp-uploads-dialog/paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-details/div/ytcp-uploads-basics/ytcp-mention-textbox[2]") 
    description = browser.find(By.ID, "textbox", description_main)
    description.clear()
    description.click()
    description.send_keys(video_description)
    print('added desc')

    browser.find(By.XPATH, "/html/body/ytcp-uploads-dialog/paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-details/div/div/ytcp-button/div").click()
    print("clicked more options")

    tags_main = browser.find(By.XPATH, "/html/body/ytcp-uploads-dialog/paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-details/div/ytcp-uploads-advanced/ytcp-form-input-container/div[1]/div[2]/ytcp-free-text-chip-bar/ytcp-chip-bar/div")
    tags = browser.find(By.ID, "text-input", tags_main)
    tags.send_keys(video_tags)
    print("added tags")

    kids_section = browser.find(By.NAME, "NOT_MADE_FOR_KIDS")
    browser.find(By.ID, "radioLabel", kids_section).click()
    
    browser.find(By.ID, 'next-button').click()
    print('clicked first next')

    browser.find(By.ID, 'next-button').click()
    print('clicked second next')

    public_main_button = browser.find(By.NAME, "PUBLIC")
    browser.find(By.ID, 'radioLabel', public_main_button).click()
    print('set to public')

    browser.find(By.ID, 'done-button').click()
    print('published')

    time.sleep(10)
    browser.driver.quit()

def login(id, url, host, port):
    browser = Selenium(id, host = host, port = port)
    browser.driver.get(url)
    input('log in and enter: ')
    browser.driver.get(url)
    time.sleep(1)
    browser.save_cookies()
    time.sleep(2)



