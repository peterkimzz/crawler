# 네이버 검색 API예제는 블로그를 비롯 전문자료까지 호출방법이 동일하므로 blog검색만 대표로 예제를 올렸습니다.
# 네이버 검색 Open API 예제 - 블로그 검색
import os
import sys
import urllib.request
import pymysql.cursors
import requests
import math
from time import sleep

DISPLAY_LENGTH = 100
CURRENT_PAGE_NUMBER = 1
START = 1


def setupMysql():

    conn = pymysql.connect(host='rds-peter.ciyd9dirrvx6.ap-northeast-2.rds.amazonaws.com',
                           user='root',
                           password='Dhrla153186!',
                           db='grooming')

    return conn


def init():

    parseData()

    mysql = setupMysql()

    with mysql.cursor() as cursor:
        sql = '''
        SELECT
            *
        FROM
            leads
        '''
        cursor.execute(sql)


def parseData():
    CLIENT_ID = 'qbv04mfrYu64rYqsiI2t'
    CLIENT_SECRET = '32vZm4Wk8R'
    TERM = '강남 미용'.encode('utf-8')
    global CURRENT_PAGE_NUMBER
    global START

    url = "https://openapi.naver.com/v1/search/local?query=%s&display=%s&start=%s" % (
        TERM, DISPLAY_LENGTH, START)
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
        item = json['items']
        print(item)

        if (CURRENT_PAGE_NUMBER < total_page_number):
            CURRENT_PAGE_NUMBER = CURRENT_PAGE_NUMBER + 1
            START = START + DISPLAY_LENGTH
            sleep(1)
            parseData()
        else:
            return print('Done.')

    else:
        print(res)
        return print("Error Code:" + rescode)


# run
init()
