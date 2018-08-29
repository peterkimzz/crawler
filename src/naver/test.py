# -*- coding: utf-8 -*-

import sys
import os
import requests
import locale
from bs4 import BeautifulSoup


req = requests.get('https://beomi.github.io/beomi.github.io_old/')
html = req.text
soup = BeautifulSoup(html, 'html.parser')
my_titles = soup.select(
    'h3 > a'
)
# my_titles는 list 객체
for title in my_titles:
    # Tag안의 텍스트
    print(title.text)
    # Tag의 속성을 가져오기(ex: href속성)
    print(title.get('href'))
