# 네이버 검색 API예제는 블로그를 비롯 전문자료까지 호출방법이 동일하므로 blog검색만 대표로 예제를 올렸습니다.
# 네이버 검색 Open API 예제 - 블로그 검색
import os
import sys
import urllib.request
import pymysql.cursors
import requests


def setupMysql():

    conn = pymysql.connect(host='rds-peter.ciyd9dirrvx6.ap-northeast-2.rds.amazonaws.com',
                           user='root',
                           password='Dhrla153186!',
                           db='grooming')

    return conn


def init():

    mysql = setupMysql()

    CLIENT_ID = 'qbv04mfrYu64rYqsiI2t'
    CLIENT_SECRET = 'gUO_jURByQ'
    TERM = '강남 미용'

    url = "https://openapi.naver.com/v1/search/local?query=%s" % TERM
    headers = {
        'X-Naver-Client-Id': CLIENT_ID,
        'X-Naver-Client-Secret': CLIENT_SECRET
    }

    res = requests.get(url, headers=headers)
    rescode = res.status_code

    if (rescode == 200):
        json = res.json()

        all_count = json['total']
        print(all_count)
    else:
        print("Error Code:" + rescode)


# run
init()
