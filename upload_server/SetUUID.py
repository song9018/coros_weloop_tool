#coding=utf-8
'''
需求：运动数据仿真上传
    1.bsp给出一段原始数据，十六进制字符串
    2.十六进制转字节类型，服务器加uuid和运动类型，写入文件
    3.上传原始数据文件，
    4.通过账号上传，账号来源也是传参的，json串中的mode,距离，运动时长，start_time,end_time,
    5.需用Python2.7编写代码

步骤：
    1.拿到楚华给的字符串，插入uuid和mode
    2.將插入了uuid和mode的十六進制字符串轉換成字節對象，并寫入到sportData文件中。
    3.并将预先准备的imageData文件的uuid替换一致，（這裡可以先將文件读取后转换成16进制，在走1,2方法，）
    4.获取楚华给的，账号，mode,运动时长，运动距离，start_time，end_time，记录保存。
    5.根据获取的账号，查询数据库中token值，若查询结果为null,则调用登录接口，加密账号后登录（接口要求账号加密），在获取token值。
    6.替换预先准备的json参数中的，mode，运动时长，运动距离，start_time，end_time,uuid值，
    7.调用上传运动数据接口，上传处理后的仿真数据到指定账号。
'''
import binascii as B
import uuid
class SetUuid(object):
    mode_list = {'跑步': '08', '骑行': '09', '10': '0a', '13': '0d'}  # 楚华传过来的mode字符串映射对应的运动类型
    def __init__(self):
        self.uuid = str(uuid.uuid4()).replace('-', '')
    def insert_uuid(self,data,uuid,mode,file_path):
        '''1.在4的位置插入uuid，插完uuid在插mode
           2.將16進制字符串轉換為二進制，
           3.將二進制字節對象寫入到sportData文件中
        '''
        uuid = uuid+SetUuid.mode_list[mode]
        data = data[:4] + uuid + data[4:]#插入uuid和mode
        data_bin = B.a2b_hex(data)#十六进制转字节对象
        f1 = open(file_path, 'wb')#将字节对象写入自定的文件中
        f1.write(data_bin)
        f1.close()
    def replace_uuid(self,uuid,mode,file_path):
        '''将imageData文件读出并转化为16进制字符串'''
        f = open('./upload_server/imageData', 'rb')
        file_binary = f.read()
        file_hex = B.b2a_hex(file_binary)
        new_uuid = uuid + SetUuid.mode_list[mode]
        data = file_hex.replace(file_hex[4:38],new_uuid)
        data_bin = B.a2b_hex(data)  # 十六进制转字节对象
        f1 = open(file_path, 'wb')  # 将字节对象写入自定的文件中
        f1.write(data_bin)
        f.close()





