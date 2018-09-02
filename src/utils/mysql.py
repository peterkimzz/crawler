import pymysql

def setupMysql():

    conn = pymysql.connect(host='127.0.0.1',
                           user='root',
                           password='Dhrla153186!',
                           db='grooming')

    return conn