import pymysql


class Mysql():
    def __init__(self):
        conn = pymysql.connect(host='rds-maria.ciyd9dirrvx6.ap-northeast-2.rds.amazonaws.com',
                               user='root',
                               password='Dhrla153186!',
                               db='grooming')
        self.conn = conn
