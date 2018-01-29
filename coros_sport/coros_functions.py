# coding:utf-8
from weloop_daily.weloop_common import *
from weloop_daily.yf_time import utc_time
from coros_struct_head import *
from operator import add
import logging

logging.basicConfig(level=logging.INFO) #DEBUG，INFO，WARNING，ERROR

class coros_function(object):
    def __init__(self):
        self.yf_time = utc_time()
        self.str = ""

    # 4k头设置格式
    def string_4k(self, *args):
        str = self.app_bit_tmp(args, self.get_value(record_4k_t))
        str_4k_head = (hex(int(str, 2)).split("0x")[1].split("L")[0])  # 二进制转十进制
        str_4k_head = rever_bytes("0" * (8 - len(str_4k_head)) + str_4k_head)  # 4字节不足补0
        assert len(str_4k_head) == 8, "str_4k_head length error"
        logging.info(str_4k_head)
        return str_4k_head

    def tag_sport_type(self,*args):
        str = self.app_bit_tmp(args, self.get_value(record_sport_info_t))
        tap_sport = (hex(int(str, 2)).split("0x")[1])
        tap_sport = rever_bytes("0" * (4 - len(tap_sport)) + tap_sport)  # 2字节不足补0
        assert len(tap_sport) == 4, "tag_sport_type length error"
        return tap_sport

    def gps_head(self, *args):  # gps头：16byte
        str = self.app_bit_tmp(args, self.get_value(record_gps_head_t))
        gps_str = hex(int(str, 2)).split("0x")[1].split("L")[0]
        gps_str = rever_bytes("0" * (32 - len(gps_str)) + gps_str)
        assert len(gps_str) == 32, "gps_head length error"
        return gps_str

    def gps_diff(self, tag, num, lon, lat, gps_lon_sign=0, gps_lat_sign=0):
        if lon < 0:
            lon = abs(lon)
            gps_lon_sign = 1
        if lat < 0:
            lat = abs(lat)
            gps_lat_sign = 1
        str = self.app_bit_tmp([tag, num, lon, lat, gps_lon_sign, gps_lat_sign], [4, 4, 11, 11])
        gps_str = (hex(int(str, 2)).split("0x")[1])
        gps_str = rever_bytes("0" * (8 - len(gps_str)) + gps_str)
        assert len(gps_str) == 8, "gps_diff length error"
        return gps_str

    def peroid_t(self, *args):
        str = self.app_bit_tmp(args, self.get_value(record_peroid_t))
        tap_peroid = (hex(int(str, 2)).split("0x")[1].split("L")[0])
        tap_peroid = rever_bytes("0" * (6 - len(tap_peroid)) + tap_peroid)
        assert len(tap_peroid)==6,"peroid_t length error"
        return tap_peroid

    def peroid_time_t(self, *args):
        return rever_bytes(self.app_byte_tmp(args, self.get_value(peroid_time_t)))

    def heart(self, seconds, index, peroid_type):  # 心率:29个,8bit:1个,29byte
        return self.peroid_data("./init_data/heart_data.txt", 29, 8, 29, seconds, index, peroid_type)

    def trust_level(self, seconds, index, peroid_type):  # 可信度:116个,2bit:1个,29byte
        return self.peroid_data("./init_data/trust_level_data.txt", 116, 2, 29, seconds, index, peroid_type)

    def step_cadence(self, seconds, index, peroid_type):  # 步频:11个,9bit:1个,13byte
        return self.peroid_data("./init_data/cadence_data.txt", 11, 9, 13, seconds, index, peroid_type)

    def step_len(self, seconds, index, peroid_type):  # 步长:11个,9bit:1个,13byte
        return self.peroid_data("./init_data/step_len_data.txt", 11, 9, 13, seconds, index, peroid_type)

    def calories(self, seconds, index, peroid_type): #卡路里:6个,16bit:1个,13byte
        return self.peroid_data("./init_data/calories_data.txt", 6, 16, 13, seconds, index, peroid_type)

    def altitude(self, seconds, index, peroid_type): #海拔:14个,16bit:1个,29byte
        return self.peroid_data("./init_data/altitude_data.txt", 14, 16, 29, seconds, index, peroid_type)

    def pace(self, seconds, index, peroid_type):  #配速:14个,16bit:1个,29byte
        return self.peroid_data("./init_data/sport_speed.txt", 14, 16, 29, seconds, index, peroid_type)

    def peroid_data(self, file_name, number, bit, data_count, num, index, peroid_type):  # 心率1byte
        with open(file_name, "r") as fp:
            peroid_list = fp.readline().strip("\n").split()
            peroid_str = ""
        zero = "0" * (data_count * 8 - (number * bit))

        peroid_0 = []
        peroid_1 = []
        for i in range(num):
            peroid_0.append(peroid_list[index])
            index += 1
            if index == number:  # number个值存一组
                peroid_1.append(peroid_0)
                cadence_0 = []
                break

            if index > len(peroid_list):  # 循环获取
                index = 0
        if peroid_0 != []:

            while len(cadence_0) < number:  # 不够--存0
                cadence_0.append(0)
                peroid_1.append(cadence_0)
        peroid_str = peroid_str + self.period_bit_to_hex(bit, peroid_1[0], peroid_type)
        peroid_str = (hex(int(peroid_str + zero, 2)).split("0x")[1].split("L")[0])
        peroid_str = ("0" * (data_count * 2 - len(peroid_str)) + peroid_str)
        assert len(peroid_str) == data_count * 2, "peroid_str length error"
        return peroid_str

    def start_time(self, date_time, time_zone, lap_distance_setting, iron_group,
                   sec_utc):  # "日期：2017/10/12 09:21:00  时区：32"
        year = int(date_time.split("/")[0])
        mon = int(date_time.split("/")[1])
        day = int(date_time.split("/")[2].split()[0])
        hour = int(date_time.split()[1].split(":")[0])
        min = int(date_time.split(":")[1])
        sec = int(date_time.split(":")[2])
        metric_inch = 0
        reverse = 0

        if time_zone < 0:
            time_zone = 256 - abs(int(time_zone)) * 4  # 解决负时区问题
        else:
            time_zone = abs(int(time_zone)) * 4
        if iron_group == 0:
            r_sec = self.yf_time.utc_to_seconds(year - 2000, mon, day, hour, min, sec)  # 十六进制时间戳
            second_0 = self.yf_time.utc_to_seconds(year - 2000, mon, day, hour, min, sec)
        else:
            r_sec = sec_utc
            second_0 = sec_utc

        str_start = rever_bytes(
            self.app_byte_tmp([r_sec, metric_inch, time_zone, lap_distance_setting, iron_group, reverse],
                              [4, 1, 1, 4, 1, 3]))
        assert len(str_start) == 28, "str_start length error"
        return str_start, second_0

    def stop_time(self, stop_sec):
        return rever_bytes(self.app_byte_tmp([stop_sec, 1, 1], self.get_value(sport_stop_info_t)))

    def lap_run_info(self, *args):
        return rever_bytes(self.app_byte_tmp(args, self.get_value(lap_run_info_t)))

    def lap_bicycle_info(self,*args):
        return rever_bytes(self.app_byte_tmp(args, self.get_value(lap_bicycle_info_t)))

    def lap_swim_info(self, *args):
        return rever_bytes(self.app_byte_tmp(args, self.get_value(lap_swim_info_t)))

    def sport_run_summary(self,*args):
        return rever_bytes(self.app_byte_tmp(args,self.get_value(sport_run_summary_info_t)))

    def sport_bicycle_summary(self, *args):
        return rever_bytes(self.app_byte_tmp(args,self.get_value(sport_bicycle_summary_info_t)))

    def sport_swim_summary(self, *args):
        return rever_bytes(self.app_byte_tmp(args,self.get_value(sport_swim_summary_info_t)))

    def period_bit_to_hex(self, bit_num, data, peroid_type):
        str_data = ""
        for i in range(len(data)):
            if peroid_type == "altitude" and int(data[i]) < 0:
                new_data = (65535 + int(data[i]))
            elif peroid_type == "speed":
                new_data = int(float(data[i]) * 100)
            elif peroid_type == "open_swim_pace":
                new_data = int(float(data[i]) * 100)
            else:
                new_data = int(data[i])
            str_data = str_data + ('{0:0%sb}' % bit_num).format(new_data)
        assert len(str_data) == bit_num*len(data), "period_bit_to_hex length error"
        return str_data

    def get_value(self,dict):
        dic_list = []
        for key in sorted(dict.keys()):
            dic_list.append(dict[key])
        return dic_list

    def app_bit_tmp(self, value_list, bit_list):
        len_bit_list = len(bit_list) - 1
        str = ""
        while len_bit_list >= 0:
            str += ('{0:0%sb}' % bit_list[len_bit_list]).format(int(value_list[len_bit_list]))
            len_bit_list -= 1
        assert len(str) == reduce(add,bit_list), "app_bit_tmp length error" #reduce(add,bit_list)/8*2
        return str

    def app_byte_tmp(self, value_list, byte_list):
        len_bit_list = len(byte_list) - 1
        str = ""
        while len_bit_list >= 0:
            byte = '%%0%sx' % (byte_list[len_bit_list] * 2)
            str += byte % int(value_list[len_bit_list])
            len_bit_list -= 1
        assert len(str) == reduce(add, byte_list)*2, "app_byte_tmp length error"
        return str


if __name__ == '__main__':
    func11 = coros_function()
    head = func11.gps_head(1, 4, 124039800, 113020140, 23012010, 1)
    print func11.string_4k(2,2,2,2,2)

