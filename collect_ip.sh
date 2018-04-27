#!/usr/bin/env bash

echo '任务开始: '`date +'%Y-%m-%d %H:%M:%S'`

# 进入 项目 目录

cd /Users/xxx/PycharmProjects/py_collect_ip  &&

envpath='/Users/xxx/Documents/.env3/bin/'  &&

source ${envpath}'activate'  &&
python collect_ip.py  &&
deactivate

# #   每晚23:30 更新  执行  collect_ip
#30 23 * * * /bin/sh /Users/XXX/PycharmProjects/py_collect_ip/collect_ip.sh >/Users/XXX/PycharmProjects/py_collect_ip/cache/collect_ip.sh.log 2>&1