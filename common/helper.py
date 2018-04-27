# -*- coding: UTF-8 -*-
import random
import time
import os
from pyquery import PyQuery as pq


agent = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
    ]


def get_random_agent():
    return random.choice(agent)


def log(logs):
    with open('cache/py_collect_ip.log', 'a') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        f.write(' :')
        f.write(logs)
        f.write('\n')
    f.close()
    pass


def str_decode(content, priority='utf-8'):

    decode_types = ['utf-8', 'gb2312', 'gbk', 'gb18030']

    if priority not in decode_types:
        priority = 'utf-8'

    try:
        return content.decode(priority)
    except Exception as e:
        print('str_decode {} exception {}'.format(priority, e))

    for decode_type in decode_types:
        if decode_type == priority:
            continue
        try:
            return content.decode(decode_type)
        except Exception as e:
            print('str_decode {} exception {}'.format(priority, e))


def translate_collect_ip_html(html, callback=None):
    dom = pq(html)
    trs = dom('table')('tr')
    i = 0
    for tr in trs.items():
        i += 1
        if i == 1:
            continue
        else:
            tds = tr('td')
            data = {}
            j = 0
            for td in tds.items():
                j += 1
                if j == 2:  # Ip地址
                    data['host'] = td.html()

                if j == 3:  # 端口
                    data['port'] = td.html()

                if j == 6:  # 类型
                    data['type'] = td.html().lower()

                if j == 7:  # 速度
                    race = str_to_second(td('div').attr('title'))

                    if race > 10:
                        data = {}
                        continue

                if j == 8:  # 连接时间
                    connect_time = str_to_second(td('div').attr('title'))

                    if connect_time > 10:
                        data = {}
                        continue

            if data and callback:
                callback(data)
    pass


def str_to_second(time_str):
    if time_str:
        if '秒' in time_str:
            time_str = time_str.replace('秒', '')
            return eval(time_str)
        elif '分' in time_str or '分钟' in time_str:
            time_str = time_str.replace('分钟', '')
            time_str = time_str.replace('分', '')
            return eval(time_str) * 60
        elif '小时' in time_str:
            time_str = time_str.replace('小时', '')
            return eval(time_str) * 60 * 60
        else:
            return 10000
    else:
        return 0


def create_pid_file():
    with open('collect_ip.pid', 'w') as f:
        f.write('{}'.format(os.getpid()))
    f.close()


def delete_pid_file():
    os.remove('collect_ip.pid')


def if_exists_pid_file():
    return os.path.exists('collect_ip.pid')
