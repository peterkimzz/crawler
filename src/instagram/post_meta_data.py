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
        id,
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


def get_contents(post_links):

    for link in post_links:
        print(link)


def get_posts(lead):
    url = lead['instagram']

    try:
        driver = Selenium().driver
        driver.get(url)
        html = driver.page_source
        soup = bs(html, 'html.parser')

        title = soup.title.string.strip()
        is_deleted = 'Page Not Found' in title

        if (is_deleted == False):
            article = soup.find_all('article', class_='FyNDV')
            print(len(article))
        else:
            # update is_deleted = 1 on db
            pass

    except:
        print("Connection refused by the server. ")
        print('Continue after 5 seconds.')
        time.sleep(5)


if __name__ == '__main__':

    slack = Slack()
    slack.send_message("Instagram Post Crawler Started")

    # multi-processing
    pool = Pool(processes=1)
    pool.map(get_posts, get_leads())
