import os
import sys
import time
import requests
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool

# ../ 에 있는 애들부터 참조 가능
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# from modules.SeleniumDriver import selenium
# from modules.Slack.slack import Slack
from modules.slack import Slack
from modules.selenium import Selenium
from modules.mysql import Mysql


def get_leads():
    mysql = Mysql()
    sql = '''
    SELECT
        id AS leadId,
        title,
        instagram,
        imgSrc
    FROM
        leads
    WHERE
        instagram > ""
    '''
    rows = mysql.select(sql)
    return rows


def get_content(driver):
    html = driver.page_source
    soup = bs(html, 'html.parser')
    post_detail = soup.find('article')
    img = post_detail.find('img')
    print(img)


def get_posts():
    # lead_id = lead['leadId']
    # url = lead['instagram']
    url = 'https://www.instagram.com/yn0202/'

    driver = Selenium().driver
    driver.get(url)

    try:
        # 첫 번째 포스트 찾아서 디테일 팝업 띄우기
        driver.find_element_by_class_name('v1Nh3').click()

        # 팝업 소스로부터 데이터 추출
        while(True):
            # 동적 로딩이기 때문에 ajax를 기다리자
            time.sleep(5)

            html = driver.page_source
            soup = bs(html, 'html.parser')
            post_detail = soup.find('article', class_='M9sTE')
            img = post_detail.find('div', class_='KL4Bh')
            a_tag = post_detail.select(
                'body > div:nth-child(15) > div > div.EfHg9 > div > div > a').click()

    except:
        print('error ocurred.')
        pass


if __name__ == '__main__':

    slack = Slack()
    # slack.send_message("Instagram Post Crawler Started")

    get_posts()

    # multi-processing
    # pool = Pool(processes=1)
    # pool.map(get_posts, get_leads())
