#coding:UTF-8
import time

dt = "2018-02-08 13:45:54"

#转换成时间数组
#转换成时间戳
timestamp = int(time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S")))

print timestamp
