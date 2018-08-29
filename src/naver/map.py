import requests
import pymysql.cursors
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep


def setupMysql():

    conn = pymysql.connect(host='rds-peter.ciyd9dirrvx6.ap-northeast-2.rds.amazonaws.com',
                           user='root',
                           password='Dhrla153186!',
                           db='grooming')

    return conn


def setupDriver():
    driver = webdriver.Chrome('/Users/Friday/dev/assets/drivers/chromedriver')
    driver.implicitly_wait(3)
    return driver


def init():
    driver = setupDriver()
    driver.get('https://map.naver.com')

    driver.find_element_by_xpath('//*[@id="search-input"]').send_keys('강남 미용')
    driver.find_element_by_xpath(
        '//*[@id="header"]/div[1]/fieldset/button').click()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    list = soup.select(
        '#panel > div.panel_content.nano.has-scrollbar > div.scroll_pane.content > div.panel_content_flexible > div.search_result > ul > li')
    for i, item in enumerate(list):
        print(i)
        print(item.get('src'))


if __name__ == '__main__':
    init()
