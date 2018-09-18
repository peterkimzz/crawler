import pymysql


class Mysql():
    def __init__(self):
        conn = pymysql.connect(host='127.0.0.1',
                               user='root',
                               password='Dhrla153186!',
                               db='grooming')
        self.conn = conn
