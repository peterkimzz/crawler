import argparse
import datetime
import os
import time
import bs4
from selenium import webdriver
from sys import platform

__author__ = "Peter Kim"
__version__ = "0.1"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://www.instagram.com/explore/tags"
LOGIN_URL = "https://www.instagram.com/accounts/login/"

# inputXPath = "//*[@id="f18c577ef00d4f"]"
# passwordXPath = "//*[@id="f564182af1c174"]"
# buttonXPath = "//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/span/button"


def init():
    print('Started.')

    driver = setDriver()
    driver.get(LOGIN_URL)


def setDriver():

     # configure selenium options
    options = webdriver.ChromeOptions()
    # hedless
    options.add_argument('headless')
    # for responsive web
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    # force change user-agent of selenium
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    # korean language
    options.add_argument("lang=ko_KR")

    driver = webdriver.Chrome(
        r"C:\Users\peter\Desktop\dev\assets\drivers/chromedriver.exe", options=options)

    driver.implicitly_wait(3)

    return driver


init()
