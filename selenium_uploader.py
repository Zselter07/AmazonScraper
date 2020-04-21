from utils.selenium_wrapper.Selenium import Selenium
import time
import os

def upload(video_path, video_title, video_description, video_tags, host=None, port=None):

    user_id = 'youtube'
    yt_url = 'https://www.youtube.com'

    browser = Selenium(user_id, host = host, port = port)

    browser.driver.get(yt_url)
    time.sleep(0.5)
    browser.load_cookies()
    time.sleep(0.5)
    browser.driver.refresh()
    time.sleep(1.5)
    print('refreshed page and logged in')

    camera_icon = browser.driver.find_element_by_class_name('style-scope ytd-topbar-menu-button-renderer')
    camera_icon.click()
    print('clicked camera icon')

    time.sleep(0.8)
    upload_video_button = browser.driver.find_element_by_class_name('style-scope ytd-compact-link-renderer')
    upload_video_button.click()
    print('clicked upload button')

    time.sleep(5)
    upload_file = browser.driver.find_element_by_xpath("//input[@type='file']")
    upload_file.send_keys(video_path)
    print('uploaded video')

    time.sleep(5)
    title = browser.driver.find_element_by_id('textbox')
    title.clear()
    title.click()
    time.sleep(0.5)
    title.send_keys(video_title)
    print('added title')
    time.sleep(0.5)

    description_main = browser.driver.find_element_by_xpath("/html/body/ytcp-uploads-dialog/paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-details/div/ytcp-uploads-basics/ytcp-mention-textbox[2]") 
    description = description_main.find_element_by_id("textbox")
    description.clear()
    description.click()
    time.sleep(1.5)
    description.send_keys(video_description)
    print('added desc')

    time.sleep(0.5)
    more_options = browser.driver.find_element_by_xpath("/html/body/ytcp-uploads-dialog/paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-details/div/div/ytcp-button/div")
    more_options.click()
    print("clicked more options")

    time.sleep(1)
    tags_main = browser.driver.find_element_by_xpath("/html/body/ytcp-uploads-dialog/paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-details/div/ytcp-uploads-advanced/ytcp-form-input-container/div[1]/div[2]/ytcp-free-text-chip-bar/ytcp-chip-bar/div")
    tags = tags_main.find_element_by_id("text-input")
    tags.send_keys(video_tags)
    time.sleep(1.5)
    print("added tags")

    kids_section = browser.driver.find_element_by_name("NOT_MADE_FOR_KIDS")
    no_label = kids_section.find_element_by_id("radioLabel")  
    no_label.click()
    print("selected 'not for kids'")

    time.sleep(1.5)
    first_next = browser.driver.find_element_by_id('next-button')
    first_next.click()
    print('clicked first next')

    time.sleep(1.5)
    second_next = browser.driver.find_element_by_id('next-button')
    second_next.click()
    print('clicked second next')

    time.sleep(1.5)
    public_main_button = browser.driver.find_element_by_name("PUBLIC")
    public_button = public_main_button.find_element_by_id('radioLabel')
    public_button.click()
    print('set to public')

    time.sleep(2)
    publish_button_main = browser.driver.find_element_by_id('done-button')
    publish_button_main.click()
    print('published')

    time.sleep(20)
    browser.driver.quit()
