from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from bs4 import BeautifulSoup
import codecs
import time
import os
import random
import sys


GUEST_PASS_LENGTH = 11

def main(url):
    driver = webdriver.Chrome('./chromedriver.exe')
    second_driver = webdriver.Chrome('./chromedriver.exe')
    webpage_file = getwebpage(url, driver, second_driver)
    lookforpass(webpage_file, driver)
    driver.close()

def rand_sleep():
    rand = random.random()
    time.sleep(.75 + rand)

# Loading up the webpage and commments

def getwebpage(url, driver):
    if url == None:
        print("Please enter Link")
        url = input()
    driver.get(url)
    loadcomments = driver.find_element_by_class_name("more_comments_box")
    
    num = 0
    while num < 10:
        loadcomments.click()
        rand_sleep()
        num += 1
    
    return driver.page_source

# Checking guest passes

def lookforpass(page, driver):
    webpage = BeautifulSoup(page, "html.parser")
    comments = webpage.find_all("div", {"class": "guestbook-body"})
    driver.get("https://www.crunchyroll.com/guest_pass")
    
    login = driver.find_element_by_class_name("login")
    login.click()
    rand_sleep()
    
    username = driver.find_element_by_id("login_form_name")
    username.send_keys("Tonthai")
    rand_sleep()
    
    password = driver.find_element_by_id("login_form_password")
    password.send_keys("pikachu")
    rand_sleep()
    
    confirm = driver.find_element_by_id("login_submit_button")
    confirm.click()
    rand_sleep()
    
    for comment in comments:
        for word in comment.get_text().split():
            if (len(word) == GUEST_PASS_LENGTH and word.isalnum() and word.isupper()):
                if validpass(word, driver):
                    return
                rand_sleep()

def validpass(word, driver):
    driver.get("https://www.crunchyroll.com/guest_pass")
    driver.find_element_by_id("guestpass_redeem_code").send_keys(word)
    cont = driver.find_element_by_partial_link_text("Continue")
    cont.click()
    
    try:
        driver.find_element_by_class_name("error-message")
    except NoSuchElementException:
        redeem = driver.find_element_by_partial_link_text("Redeem")
        redeem.click()
        return True
    return False

if __name__  == "__main__":
    main(sys.argv[1])
    

