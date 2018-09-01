# 네이버 검색 API예제는 블로그를 비롯 전문자료까지 호출방법이 동일하므로 blog검색만 대표로 예제를 올렸습니다.
# 네이버 검색 Open API 예제 - 블로그 검색
import pymysql
import requests
import math
from time import sleep
from bs4 import BeautifulSoup

DISPLAY_LENGTH = 100


def setupMysql():

    conn = pymysql.connect(host='127.0.0.1',
                           user='root',
                           password='Dhrla153186!',
                           db='grooming')

    return conn


def getLocations():
    mysql = setupMysql()
    location = '강남구'

    try:
        with mysql.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''
                SELECT
                    name
                FROM
                    locations
                WHERE
                    location_id IN (
                        SELECT
                            id
                        FROM
                            locations
                        WHERE
                            name = "%s"
                    ) 
                ''' % location
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
    finally:
        mysql.close()


def parseData():
    # get locations
    locations = getLocations()

    lists = ['네일', '피부', '타투', '문신', '왁싱', '미용']

    # for location in locations:
    #     loc = location['name']
    #     keyword = loc + ' 피부'
    #     searchNaverLocalAPI(keyword)

    keyword = '강남구 압구정동 왁싱'
    searchNaverLocalAPI(keyword)


def searchNaverLocalAPI(search_keyword):
    CLIENT_ID = 'qbv04mfrYu64rYqsiI2t'
    CLIENT_SECRET = '32vZm4Wk8R'
    DEFAULT_START = 1
    DEFAULT_CURRENT_PAGE_NUMBER = 1

    def useAPI(current_page_number, start):

        print('%s %s %s is started.' %
              (search_keyword, current_page_number, start))

        if (current_page_number > 10):
            return print('Search for %s is finished.' % search_keyword)

        url = "https://openapi.naver.com/v1/search/local?query=%s&display=%s&start=%s" % (
            search_keyword, DISPLAY_LENGTH, start)
        headers = {
            'X-Naver-Client-Id': CLIENT_ID,
            'X-Naver-Client-Secret': CLIENT_SECRET
        }

        res = requests.get(url, headers=headers)
        rescode = res.status_code
        if (rescode == 200):
            json = res.json()

            all_count = json['total']
            total_page_number = math.ceil(all_count / DISPLAY_LENGTH)
            items = json['items']
            updateDataToDB(items)

            if (current_page_number < total_page_number):
                current_page_number = current_page_number + 1
                start = start + DISPLAY_LENGTH
                sleep(0.5)
                print('전체: ', all_count)
                useAPI(current_page_number, start)
            else:
                return print('Search for %s is finished.' % search_keyword)

        else:
            print(res)
            return print("Error Code:" + rescode)

    useAPI(DEFAULT_CURRENT_PAGE_NUMBER, DEFAULT_START)


def updateDataToDB(items):
    mysql = setupMysql()

    try:
        with mysql.cursor(pymysql.cursors.DictCursor) as cursor:
            for item in items:

                title = BeautifulSoup(item['title'], 'html.parser').get_text()
                link = item['link']
                description = BeautifulSoup(
                    item['description'], 'html.parser').get_text()
                category = item['category']
                telephone = item['telephone']
                address = item['address']
                roadAddress = item['roadAddress']
                mapx = item['mapx']
                mapy = item['mapy']

                sql = '''
                    INSERT INTO
                        leads_naver (title, link, description, category, telephone, address, roadAddress, mapx, mapy)
                        VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")
                    ''' % (title, link, description, category, telephone, address, roadAddress, mapx, mapy)
                cursor.execute(sql)
                mysql.commit()
                # print('%s is updated.' % title)
    finally:
        mysql.close()


if __name__ == '__main__':
    parseData()
