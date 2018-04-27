# -*- coding: UTF-8 -*-
import pyssdb
import configparser
import pymysql
import time
from common import request
from common import helper


def insert(data):
    cursor = mysql.cursor()
    try:
        cursor.execute(insert_ip_sql.format(**data))
        mysql.commit()
    except Exception as e:
        mysql.rollback()
        print(insert_ip_sql.format(**data))
        print('Exception :{}'.format(e))
        if 'Duplicate entry' in e.__str__():
            print(' 重复的 ！！！！')
        elif 'Out of range value for column' in e.__str__():
            print(' 字段超出范围 ！！！')
            helper.log('mysql insert 出错 ！！Exception: {}'.format(e))
        else:
            helper.log('mysql insert Exception: {}'.format(e))
            raise Exception(e)
    finally:
        cursor.close()


def count_ips():
    cursor = mysql.cursor()
    try:
        cursor.execute(count_ip_sql)
        total = cursor.fetchone()[0]
    except Exception as e:
        print(count_ip_sql)
        print('Exception :{}'.format(e))
        raise Exception(e)
    finally:
        cursor.close()
    return total


def delete_invalid_ips():
    cursor = mysql.cursor()
    try:
        cursor.execute(delete_ips_sql)
        mysql.commit()
    except Exception as e:
        mysql.rollback()
        print(delete_ips_sql)
        print('Exception :{}'.format(e))
        raise Exception(e)
    finally:
        cursor.close()


if __name__ == '__main__':

    # 预处理 pid文件 clear 无效ip
    if helper.if_exists_pid_file():
        helper.delete_pid_file()
        time.sleep(60)
    helper.create_pid_file()

    week = time.strftime('%w', time.localtime())
    if week == '5':  # 周五
        delete_invalid_ips()

    # 初始化 配置文件 ssdb mysql request
    config = configparser.ConfigParser()
    config.read('config/config.ini')

    ssdb = pyssdb.Client(host=config.get('local', 'ssdb_host'),
                         port=config.getint('local', 'ssdb_port'))

    mysql = pymysql.Connect(host=config.get('server', 'mysql_host'),
                            port=config.getint('server', 'mysql_port'),
                            database=config.get('server', 'mysql_db'),
                            user=config.get('server', 'mysql_user'),
                            password=config.get('server', 'mysql_password'))

    request = request.Request(ssdb, config)

    insert_ip_sql = "INSERT INTO collect_ips(host, port, type) VALUES('{host}', {port}, '{type}')"
    count_ip_sql = "SELECT COUNT(*) FROM collect_ips"
    delete_ips_sql = "DELETE FROM collect_ips WHERE status = 0"

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Cache-Control': 'no-cache',
        'Host': 'www.xicidaili.com',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache'
    }

    url = "http://www.xicidaili.com/nn/{}"
    page = 1
    while count_ips() <= 2000 and helper.if_exists_pid_file():
        response = request.get(url.format(page), headers=headers)
        if response.content:
            html = helper.str_decode(response.content)
            helper.translate_collect_ip_html(html, callback=insert)
        page += 1
        if page >= 100:
            helper.log('page >= 100')
            break

    mysql.close()
    helper.delete_pid_file()
    pass
