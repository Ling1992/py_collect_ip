# -*- coding: UTF-8 -*-
import pyssdb
import configparser
import pymysql
import time
from common import request
from common import helper


if __name__ == '__main__':

    if helper.if_exists_pid_file():
        helper.delete_pid_file()
        time.sleep(20)

    helper.create_pid_file()
    time.sleep(30)
    helper.delete_pid_file()
    pass
