from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymysql

__author__ = "Peter Kim"
__version__ = "0.1"

BASE_URL = "https://www.instagram.com/explore/tags"
LOGIN_URL = "https://www.instagram.com/accounts/login/"

# inputXPath = "//*[@id="f18c577ef00d4f"]"
# passwordXPath = "//*[@id="f564182af1c174"]"
# buttonXPath = "//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/span/button"


def init():
    accounts = getAccounts()

    for account in accounts:
        driver = setDriver()
        insta_link = account['instagram']
        print('%s is started' % insta_link)
        driver.get(insta_link)
        first_post = driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/div[2]/article/div[1]/div/div[1]/div[1]/a').click()
        sleep(3)

        for i in range(0, 9):
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            post_detail = soup.find('article', class_='M9sTE')

            # Check image or video
            isVideoType = len(post_detail.find_all('video')) > 0

            global content_type, src, activity_amount
            thumbnaiL_img = post_detail.find('img', class_='_6q-tv').get('src')
            # hashtag = post_detail.find('img', class_='FFVAD').get('alt')
            description = post_detail.find(
                'div', class_='C4VMK').get_text().strip()
            # createdDate = post_detail.find('time').get('datetime')
            createdDate = post_detail.find('time').get('title')

            if (isVideoType):
                content_type = 'video'
                activity_amount = post_detail.find(
                    'span', class_='vcOH2').find('span').string
                src = post_detail.find('video', class_="tWeCl").get('src')
            else:
                content_type = 'image'
                activity_amount = post_detail.find(
                    'span', class_='zV_Nj').find('span').string
                src = post_detail.find('img', class_='FFVAD').get('src')

            post = {
                'parent_id': account['id'],
                'content_type': content_type,
                'src': src,
                'source': 'instagram',
                'activity_amount': activity_amount,
                'thumbnail_img': thumbnaiL_img,
                'description': description,
                # 'hashtag': hashtag,
                'createdDate': createdDate
            }
            insertRow(post)

            next_button = driver.find_element_by_css_selector('.HBoOv').click()
            sleep(2)


def init_test():

    driver = setDriver()
    insta_link = 'https://www.instagram.com/so.so_beauty/'
    driver.get(insta_link)
    first_post = driver.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/div[2]/article/div[1]/div/div[1]/div[1]/a').click()
    sleep(3)

    for i in range(0, 9):
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        post_detail = soup.find('article', class_='M9sTE')

        print('시작')
        # print(post_detail.prettify())
        tags1 = post_detail.find_all(lambda tag: 'src' in tag.attrs)
        tags2 = post_detail.find_all(lambda tag: tag.has_attr('src'))
        tag = post_detail.find(lambda tag: tag.name ==
                               'script' and 'src' in tag.attrs)

        for i, tag in enumerate(tags1):
            print('\n', i)
            print(tag)

        # Check image or video
        isVideoType = len(post_detail.find_all('video')) > 0

        global content_type, source, activity_amount
        thumbnaiL_img = post_detail.find('img', class_='_6q-tv').get('src')
        hashtag = post_detail.find('img', class_='FFVAD')
        description = post_detail.find('div', class_='C4VMK')
        createdDate = post_detail.find('time').get('datetime')

        if (isVideoType):
            content_type = 'video'
            activity_amount = post_detail.find(
                'span', class_='vcOH2').find('span').string
            source = post_detail.find('video', class_="tWeCl").get('src')
        else:
            content_type = 'image'
            activity_amount = post_detail.find(
                'span', class_='zV_Nj').find('span').string
            source = post_detail.find('img', class_='FFVAD').get('src')

        # print('')
        # print('content_type', content_type)
        # print('source:', source)
        # print('activity_amount', activity_amount)
        # print('thumbnail_img:', thumbnaiL_img)
        # print('description', description)
        # print('hashtag', hashtag)
        # print('createdDate', createdDate)

        next_button = driver.find_element_by_css_selector('.HBoOv').click()
        sleep(1.5)


def setupMySQL():
    conn = pymysql.connect(host='127.0.0.1',
                           user='root',
                           password='Dhrla153186!',
                           db='grooming')

    return conn


def getAccounts():

    mysql = setupMySQL()
    try:
        with mysql.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''
                SELECT
                    id,
                    title,
                    instagram,
                    imgSrc
                FROM
                    leads_naver_gangnam
                WHERE
                    instagram > ""
                '''
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
    finally:
        mysql.close()


def insertRow(post):

    parentId = post['parent_id']
    title = ''
    description = post['description']
    # hashtag = post['hashtag']
    content_type = post['content_type']
    activity_amount = post['activity_amount']
    src = post['src']
    thumbnail = post['thumbnail_img']
    source = post['source']
    createdDate = post['createdDate']

    mysql = setupMySQL()
    try:
        with mysql.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''
                INSERT INTO
                    news (parentId, title, description, likeCount, thumbnail, contentType, src, source, date)
                    VALUES (%s, "%s", "%s", "%s", %s, "%s", "%s", "%s", "%s", "%s")
                ''' % (parentId, title, description, activity_amount, thumbnail, content_type, src, source, createdDate)
            # print(sql)
            cursor.execute(sql)
            mysql.commit()
            print('updated.', parentId)

    finally:
        mysql.close()


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


if __name__ == '__main__':
    # init()
    init_test()
