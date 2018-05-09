# -*- coding: UTF-8 -*-
import requests
from common import helper
import http.cookiejar
import time


class Request(object):

    def __init__(self, ssdb=None, config=None):
        print('Request init__')
        if not ssdb or not config:
            self.use_proxy = False
            print('request 无法使用 proxy ssdb 为None 或 config 为None')
        else:
            self.ssdb = ssdb
            self.config = config
            self.use_proxy = True
            self.proxy_addr = None
            self.change_proxy = True
            self.agent = helper.get_random_agent()

    def get_proxy(self):
        # get ip
        if self.use_proxy and self.change_proxy:
            proxy_info = self.ssdb.qpop(self.config.get('local', 'ssdb_queue_ip_pool'))
            self.agent = helper.get_random_agent()
            if not proxy_info:
                print('proxy_info 不存在 ！！！')
                self.proxy_addr = None
                pass
            else:
                self.proxy_addr = '{}://{}:{}'.format(proxy_info['type'], proxy_info['host'], proxy_info['port'])
                self.ssdb.set(self.config.get('local', 'ssdb_kv_black_list') + proxy_info['id'], self.proxy_addr)

    def get(self, url, retries=3, interval=5, **kwargs):
        if retries < 0:
            return None

        self.get_proxy()
        self.change_proxy = False

        headers = kwargs.get("headers")
        if headers is None:
            headers = {}
        headers['User-Agent'] = self.agent
        kwargs["headers"] = headers

        if self.proxy_addr:
            kwargs["proxies"] = self.proxy_addr

        print(kwargs)
        session = requests.session()
        # session.keep_alive = False

        session.cookies = http.cookiejar.LWPCookieJar(filename='cookies')

        try:
            session.cookies.load(filename='cookies', ignore_discard=True)
        except Exception as e:
            print('not find cookies . exception:', e)

        helper.log('url:{} ; proxy:{}'.format(url, self.proxy_addr))

        time.sleep(interval)  # 请求 间隔
        try:
            response = session.get(url, timeout=20, **kwargs)
            session.cookies.save()
            session.close()
            if response:
                helper.log('response.status_code:{}'.format(response.status_code))
                if response.status_code == 200:  # 请求成功
                    helper.log('请求成功 ！！！！')
                    return response

                else:
                    # 407 请求失败 需要代理认证
                    # 403 代理 被网站限制
                    # 503 代理 被网站限制
                    if response.status_code == 407 \
                            or response.status_code == 403\
                            or response.status_code == 503:
                        pass

                    elif response.status_code == 404:
                        if retries == 1:
                            raise Exception('404 错误！！！！')
                        retries -= 1

                    elif response.status_code == 502:  # 设置了host  url是个重定向链接会出现这样的问题
                        retries -= 1

                    else:
                        helper.log('未知错误！！！')
                        retries -= 1

                    self.change_proxy = True
                    return self.get(url, retries, interval + 1, **kwargs)
            else:
                helper.log('请求错误！！！ response为:{}'.format(response))
        except Exception as e:  # 连接超时 拒绝 中止 没网络 等
            helper.log('请求出错 Exception:{}'.format(e))
            if "ConnectTimeoutError" in e \
                    or "[Errno 60] Operation timed out" in e\
                    or "[Errno 61] Connection refused":
                pass

            elif "Connection aborted" in e:
                retries -= 1

            else:
                if retries == 1:
                    raise Exception('请求出错 !! Exception: {}'.format(e))
                retries -= 1
            self.change_proxy = True
            return self.get(url, retries, interval + 1, **kwargs)

        return None

