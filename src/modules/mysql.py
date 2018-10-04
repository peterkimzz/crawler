import pymysql


class Mysql():
    def __init__(self):

        host = "rds-maria.ciyd9dirrvx6.ap-northeast-2.rds.amazonaws.com"
        user = "root"
        password = "Dhrla153186!"
        db = "beauty_scandal"

        conn = pymysql.connect(host=host,
                               user=user,
                               password=password,
                               db=db)

        print("MySQL Host %s is connected." % host)

        self.pymysql = pymysql
        self.conn = conn

    def select(self, sql):
        try:
            with self.conn.cursor(self.pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
                return rows
        except:
            print("MySQL select query get error.")

    def update(self, sql):
        try:
            with self.conn.cursor(self.pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                self.conn.commit()

        except:
            print("MySQL insert query get error.")
