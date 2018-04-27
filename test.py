# -*- coding: UTF-8 -*-
import pyssdb
import configparser
import pymysql
import time
from common import request
from common import helper


def delete_invalid_ips():
    cursor = mysql.cursor()
    try:
        cursor.execute(delete_ips_sql)
        print('111111')
        mysql.commit()
    except Exception as e:
        mysql.rollback()
        print(delete_ips_sql)
        print('Exception :{}'.format(e))
        raise Exception(e)
    finally:
        cursor.close()


if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('config/test.ini')

    mysql = pymysql.Connect(host=config.get('server', 'mysql_host'),
                            port=config.getint('server', 'mysql_port'),
                            database=config.get('server', 'mysql_db'),
                            user=config.get('server', 'mysql_user'),
                            password=config.get('server', 'mysql_password'))

    delete_ips_sql = "DELETE FROM collect_ips WHERE status = 0"

    delete_invalid_ips()

    a = time.strftime('%w', time.localtime())
    if a == '5':
        print('今天要clear!!!')

    print(config.get('local', 'url'))
    mysql.close()
    pass
