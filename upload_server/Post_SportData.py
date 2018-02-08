#coding=utf-8
import pymysql
import json
import uuid
from binascii import b2a_hex, a2b_hex
import SetUUID
import requests
'''写个类，用来上传运动数据。
.获取楚华给的，账号，mode,运动时长，运动距离，start_time，end_time，记录保存。
    5.根据获取的账号，查询数据库中token值，若查询结果为null,则插入token值到指定账号，在获取token值。
    6.替换预先准备的json参数中的，mode，运动时长，运动距离，start_time，end_time,uuid值，
    7.调用上传运动数据接口，上传处理后的仿真数据到指定账号。'''
class Post_sport():

    json = [{"calorie":76796,"deviceId":"COROS PACE A752DF","distance":12601.50,"duration":1021,"endTime":1517823322,"endTimezone":32,"laps":1,"mode":8,"startTime":1517820018,"startTimezone":32,"state":1,"subMode":1,"uuid":"5396504c49724e459afb2ae021b77587"}]
    url ="http://coros-api.weloop.cn/coros/data/sport/save"

    def get_token(self,account):
        '''获取token的方法，若所查账号下没有token值，则update个token值个有效期到t_account表中。'''
        conn = pymysql.connect(host='118.190.173.50', port=3306, user='root', passwd='wx&2014#12#02@@DB', db='coros_user',charset='utf8')
        cur = conn.cursor()
        sql = "select access_token from t_account where email='"+account+"';"
        cur.execute(sql)
        token = cur.fetchone()
        if token ==None:#如果token为null,则插入token和有效期值到指定账号，在返回token值。
            sql = "UPDATE coros_user.t_account SET access_token = '"+self.set_token()+"', validity_date = date_add(now(), interval 10 day)  WHERE email ='"+account+"';"
            cur.execute(sql)
            conn.commit()
            token = self.get_token(account)
        else:
            token = str(token[0])
        cur.close()
        conn.close()
        return token
    @classmethod
    def set_token(self):#获取随机32位token值。
        self.token = str(uuid.uuid4()).replace('-', '')
        return self.token
    def send_form_data_sport(self,url, file_url, data_param):
        '''这个方法用来发送运动数据上传接口请求
        url是请求路径
        file_url是要上传的日常数据文件的路径
        intface_name是接口名称，这里主要是用来在返回值的excel表中展示用的
        data_param是请求参数，字典类型
        param_url是请路径，主要是用来在返回值的Excel表中展示，区别于参数url是应为url带有token值
        '''
        imageData_url = file_url[0]
        sportData_url = file_url[1]
        files = {'imageData': open(imageData_url, 'rb'), 'sportData': open(sportData_url, 'rb')}
        # data_param = eval(data_param)
        r = requests.post(url=url, data={'jsonParameter': json.dumps(data_param)}, files=files, verify=False)


def post_main(data,mode,duration,distance,startTime,endTime,account):
    '''这个方法是用来同一调用的，传参调用该方法，会将仿真数据上传至指定账号下。'''
    setUuid = SetUUID.SetUuid()
    new_uuid = setUuid.uuid
    data = data
    mode = mode
    duration = duration
    distance = distance
    startTime = startTime
    endTime = endTime
    setUuid.insert_uuid(data, new_uuid, mode, "./upload_server/sportData")
    setUuid.replace_uuid(new_uuid, mode,"./upload_server/imageData")

    account = account
    post = Post_sport()
    json_data= post.json
    json_data[0]["mode"]=mode
    json_data[0]["duration"] = duration
    json_data[0]["distance"] = distance
    json_data[0]["startTime"] = startTime
    json_data[0]["endTime"] = endTime
    json_data[0]["uuid"] = new_uuid
    token = post.get_token(account)
    url = post.url+"?accessToken="+token
    file_url =["./upload_server/imageData","./upload_server/sportData"]
    post.send_form_data_sport(url,file_url,json_data)




