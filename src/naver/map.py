import requests
import pymysql.cursors
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep


def setupMysql():

    conn = pymysql.connect(host='127.0.0.1',
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

    search_term = '강남 미용'
    driver.find_element_by_xpath(
        '//*[@id="search-input"]').send_keys(search_term)
    driver.find_element_by_xpath(
        '//*[@id="header"]/div[1]/fieldset/button').click()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    list = soup.select(
        '#panel > div.panel_content.nano.has-scrollbar > div.scroll_pane.content > div.panel_content_flexible > div.search_result > ul > li')
    for item in list:

        title = item.find('a').get_text()
        roadAddress = item.find('dd', class_="addr").contents[0].strip()
        telephone = item.find('dd', class_="tel").string.strip()
        category = item.find('dd', class_="cate").string.strip()
        img_url = item.find('img').get('src')
        print(title)
        print(roadAddress)
        print(telephone)
        print(category)
        print(img_url)


if __name__ == '__main__':
    init()
