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

slack = Slack()


def get_leads():
    mysql = Mysql()
    sql = '''
    SELECT
        l.id AS leadId,
        l.title,
        l.instagram,
        n.thumbnailUrl AS latestThumbnailUrl,
        n.link AS latestLink

    FROM 
        leads l
        
    LEFT JOIN 
	    news n
	ON
		n.id = (
		SELECT MAX(id)
		FROM news
		WHERE leadId = l.id
		)

    WHERE
    	l.isDeleted != 1 AND
        l.instagram > ""
        
    GROUP BY
    	l.id
    '''
    rows = mysql.select(sql)
    return rows


def get_posts(lead):
    print(lead)
    lead_id = lead['leadId']
    title = lead['title']
    url = lead['instagram']
    latest_link = lead['latestLink']
    # latest_thumbnail_url = lead['latestThumbnailUrl']

    driver = Selenium().driver
    driver.get(url)

    try:
        # 첫 번째 포스트 찾아서 디테일 팝업 띄우기
        driver.find_element_by_class_name('v1Nh3').click()

        # 다음 버튼을 누르며 마지막 포스트까지 팝업 모달 창으로부터 데이터 추출 반복
        while(True):
            # 동적 로딩이기 때문에 ajax를 기다리자
            time.sleep(2)

            try:
                # HTML 파싱
                html = driver.page_source
                soup = bs(html, 'html.parser')
                post_detail = soup.find('article', class_='M9sTE')

                # post_detail로부터 데이터 추출
                username = post_detail.find('a', class_='FPmhX').string
                user_img_url = post_detail.find(
                    'img', class_='_6q-tv').get('src')
                meta = post_detail.find('div', class_='C4VMK').find('span')
                total_likes = post_detail.find(
                    'span', class_='zV_Nj').find('span').string
                thumbnail_url = post_detail.find(
                    'div', class_='KL4Bh').contents[0].get('src')
                source = 'Instagram'
                created_date = post_detail.find(
                    'time', class_='_1o9PC').get('datetime')
                link = driver.current_url

                if (latest_link == link):
                    print('새로 등록된 포스트가 없습니다.')
                    return
                else:
                    mysql = Mysql()
                    sql = '''
                    INSERT INTO
                        news(leadId, username, userImgUrl, meta, totalLikes, thumbnailUrl, source, date, link)
                        VALUES(%s, "%s", "%s", '%s', %s, "%s", "%s", "%s", "%s")
                    ''' % (lead_id, username, user_img_url, meta, total_likes, thumbnail_url, source, created_date, link)
                    mysql.update(sql)

            except:
                print('DOM 구조 변경')
                # slack.send_message('인스타그램 HTML DOM 구조 변경이 감지되었습니다.')

            finally:
                try:
                    next_post_button = driver.find_element_by_class_name(
                        'HBoOv')
                    next_post_button.click()
                except:
                    print('마지막 포스트입니다.')
                    return

    except:
        msg = '''
        삭제된 페이지거나 오류가 있습니다.
        lead id: %s
        이름: %s
        링크: %s
        ''' % (lead_id, title, url)
        slack.send_message(msg)
        print(msg)
        # mysql = Mysql()
        # mysql.update('''
        # UPDATE
        #     leads
        # SET
        #     isDeleted = 1
        # WHERE
        #     id = %s
        # ''' % lead_id)


if __name__ == '__main__':

    slack.send_message('인스타그램 스파이더가 최신 포스트들을 크롤링합니다.')

    # multi-processing
    # leads = ['https://www.instagram.com/trala_nail/']
    pool = Pool(processes=4)
    pool.map(get_posts, get_leads())
