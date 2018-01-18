# coding=utf-8
from weloop_common import *
from weloop_function_struct import *
from utc_time import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# dubug打印信息
def print_pace_info(func):
    def wrapper(*args):
        #print("解析--%s--数据" % func)
        return func(*args)
    return wrapper

class sport_struct(object):
    gps_utc = ''
    lat = 0
    lon = 0
    timezone = 0
    altitude = 0
    value_valid = 0
    time_interval = 0
    result = []

    def __init__(self, gps_file, sport_file):
        self.yf = utc_time()
        self.gps_file = gps_file
        self.sport_file = sport_file
        # self.pace_file = pace_file

    # utc时间戳转换
    def get_time(self, utc):
        return get_Localtime_by_zone(self.yf.seconds_to_utc(utc).show(False, True), sport_struct.timezone)

    @print_pace_info
    def RECORD_TAG_EXTEND(self, pstr):
        print("RECORD_TAG_EXTEND")

    @print_pace_info
    def RECORD_TAG_INVALID(self, pstr):
        print("RECORD_TAG_INVALID")

    @print_pace_info
    def record_peroid_t(self, pstr):  # 心率、步频等数据
        bit_list = [4, 3, 1, 4]
        (self.__tag, self.__cadence_type, self.__cadence_tag, self.__value_valid_num) = app_bitmap_read_bit(pstr,
                                                                                                            bit_list)
        self._data = pstr[4:]
        getattr(self, RECORD_SPORT_PEROID[self.__cadence_type])(self._data)

    @print_pace_info
    def record_time_t(self, pstr):  # 记录开始时间戳
        byte_list = [4, 3, 1, 2, 2, 4, 32, 8]
        (self.__tag, self.__cadence_type, self.__cadence_tag, self.__sport_type, self.__none, self.__sport_state,
         self.__utc, self.inteval) = app_bitmap_read_bit(pstr, byte_list)
        info_list = ["运动开始时间:%s" % (self.get_time(self.__utc))]
        self.sport_file.write(str(info_list) + "\n")

    @print_pace_info
    def RECORD_TAG_SPORT_CADENCE(self, pstr):  # 频率数据：心率、步频等

        bit_list = [4, 3, 1, 8]
        (self.__tag, self.__cadence_type, self.__cadence_tag, self.__value_valid_num) = app_bitmap_read_bit(pstr,
                                                                                                            bit_list)
        sport_struct.value_valid = self.__value_valid_num
        getattr(self, RECORD_SPORT_CADENCE_TAG[self.__cadence_tag])(pstr)

    @print_pace_info
    def RECORD_TAG_GPS_HEAD(self, pstr):
        bit_list = [4, 11, 1]
        (self.__tag, self.__speed_value, self.__speed_type) = app_bitmap_read_bit(pstr, bit_list)
        pstr = pstr[4:]
        byte_list = [4, 4, 2, 4]

        (self.__lon, self.__lat, self.__altitude, self.__utc) = app_bitmap_read_byte(pstr, byte_list)
        sport_struct.altitude = self.__altitude
        sport_struct.gps_utc = self.__utc
        sport_struct.lat = self.__lat
        sport_struct.lon = self.__lon
        list=[self.__lon/1000000.0,self.__lat/1000000.0]
        sport_struct.result.append(list)
        info_list = ["time:%s ,lon:%s ,lat:%s ,speed:%s km/h, altitude:%s m" % (
            self.get_time(sport_struct.gps_utc), int(sport_struct.lon), int(sport_struct.lat),
            self.__speed_value / 100, sport_struct.altitude)]
        self.gps_file.write(str(info_list) + "\n")

    @print_pace_info
    def RECORD_TAG_GPS_DIFF(self, pstr):
        bit_list = [4, 11, 1, 16, 16, 8, 8]

        (self.__tag, self.__speed_value, self._speed_type, self._lon, self.__lat, self.__altitude,
         self.__utc_interval) = app_bitmap_read_bit(pstr, bit_list)

        if self._lon>32768:
            self._lon=self._lon-65536

        if self.__lat>32768:
            self.__lat=self.__lat-65536

        sport_struct.lon += self._lon
        sport_struct.lat += self.__lat

        list = [sport_struct.lon/1000000.0, sport_struct.lat/1000000.0]
        sport_struct.result.append(list)


        sport_struct.gps_utc = sport_struct.gps_utc + self.__utc_interval

        if self.__altitude > 128:
            self.__altitude = self.__altitude - 256
        sport_struct.altitude += self.__altitude

        info_list = ["time:%s ,lon:%s ,lat:%s ,speed:%s km/h, altitude:%s m" % (
            self.get_time(sport_struct.gps_utc), int(sport_struct.lon), int(sport_struct.lat), self.__speed_value / 100,
            sport_struct.altitude)]
        self.gps_file.write(str(info_list) + "\n")

    @print_pace_info
    def peroid_step_t(self, pstr):
        # value = ["步频step/min"]
        value = ["步频step/min"]
        app_bitmap_read_bit_t(pstr, 8, value, sport_struct.value_valid)
        self.sport_file.write(str(value) + "\n")

    @print_pace_info
    def peroid_step_len_t(self, pstr):
        value = ["步长cm"]
        app_bitmap_read_bit_t(pstr, 8, value, sport_struct.value_valid)
        self.sport_file.write(str(value) + "\n")

    @print_pace_info
    def peroid_heartrate_t(self, pstr):
        value = ["心率"]
        app_bitmap_read_bit_t(pstr, 8, value, sport_struct.value_valid)
        self.sport_file.write(str(value) + "\n")

    @print_pace_info
    def peroid_trust_level_t(self, pstr):
        value = ["可信度"]
        app_bitmap_read_bit_t(pstr, 2, value, sport_struct.value_valid)
        self.sport_file.write(str(value) + "\n")

    def ouput_result(self):
        for i in range(len(sport_struct.result)):
            sport_struct.result[i].append(0)
        return sport_struct.result

    #清空列表
    def clear_result(self):
        sport_struct.result=[]

class daily_struct(object):
    timezone=0
    time_add=0
    around=1
    result=[]
    def __init__(self, daily_file):
        self.yf = utc_time()
        self.daily_file = daily_file
        self.heart=0
        self.mode_name = ""

        # utc时间戳转换

    def get_time(self, utc):
        return get_Localtime_by_zone(self.yf.seconds_to_utc(utc).show(False, True), daily_struct.timezone)


    def decode_daily(self, pstr):
        i = 0
        while i < len(pstr):
            tag = pstr[i:][0:4]
            status = self.which_status(tag)
            if tag.upper()=="67F8":
                status="swim_around_t"
            if tag.upper()=="78F8":
                status = "swim_summary_t"
            size = DAILY_SIZE[status]
            ppstr = pstr[i:i + size * 2]
            i += size * 2
            getattr(self, status)(ppstr)

    @print_pace_info
    def STATUS_SYNC(self, pstr):
        byte_list = [1, 1]
        (self.sys_id, self.sys_symblo) = app_bitmap_read_byte(pstr, byte_list)


    @print_pace_info
    def STATUS_DATE(self, pstr):
        pstr="00"+pstr
        bit_list=[4,4,5,4,3,4]
        (self.tag,self.num,self.day,self.mon,self.year,self.sys_symblo) = app_bitmap_read_bit(pstr, bit_list)

        #print(self.year+15,self.mon,self.day)

    @print_pace_info
    def STATUS_TIME(self, pstr):
        pstr = "00" + pstr
        bit_list = [4, 4, 6,5,5]
        (self.tag, self.num, self.min, self.hour,self.sys_symblo) = app_bitmap_read_bit(pstr, bit_list)
        #print(self.hour,self.min)

    @print_pace_info
    def STATUS_MODE(self, pstr):
        head = '0x' + rever_two_bytes(pstr)
        assert len(head) == 6
        key0=(eval(head) & 0x3fff)
        if key0 in  DAILY_MODE.keys():
            self.mode_name = DAILY_MODE[(eval(head) & 0x3fff)]



    @print_pace_info
    def STATUS_DATA(self, pstr):
        pstr = "00" + pstr
        bit_list = [4, 4, 8, 8]
        (self.tag, self.num, self.step, self.energe) = app_bitmap_read_bit(pstr, bit_list)
        self.mode_time=self.utc+daily_struct.time_add
        daily_struct.time_add+=1
        info_list = {"start_time":"%s" %self.get_time(self.mode_time),"mode":"%s" %self.mode_name,"energy":"%s" %self.energe, "step":"%s" %self.step, "heart":"%s" %self.heart}
        self.heart=0
        daily_struct.result.append(info_list)
        self.daily_file.write(str(info_list) + "\n")

    @print_pace_info
    def STATUS_HR(self, pstr):
        pstr = "00" + pstr
        bit_list = [4, 4, 12, 4]
        (self.tag, self.num, self.heart, self.sys_symblo) = app_bitmap_read_bit(pstr, bit_list)


    @print_pace_info
    def STATUS_START(self, pstr):
        getattr(self, struct_map[rever_two_bytes(pstr.upper())])(pstr)

    @print_pace_info
    def sport_start_time_t(self,pstr):
        byte_list = [1, 1, 4, 1]
        (self.tag, self.num, self.utc, self.time_zone) = app_bitmap_read_byte(pstr, byte_list)
        if eval('0x' + pstr[12:14]) < 48:
            daily_struct.timezone = int((eval('0x' + pstr[12:14])) / 4)
        else:
            daily_struct.timezone = int((eval('0x' + pstr[12:14]) - 256) / 4)  # 反码加1(解决西时区问题)

        self.start_time=self.get_time(self.utc)

        info_list={"开始时间":"%s" %self.start_time, "时区":"%s" %daily_struct.timezone}
        daily_struct.result.append(info_list)
        self.daily_file.write(str(info_list)+"\n")


    @print_pace_info
    def sport_around_t(self,pstr):
        byte_list = [1, 1, 4, 2, 2]
        (self.tag, self.num, self.utc, self.distance,self.duration) = app_bitmap_read_byte(pstr, byte_list)
        self.start_time = self.get_time(self.utc)
        if self.mode_name == "跑步":
            self.distance = self.distance*0.01
        if self.mode_name == "骑行":
            self.distance = self.distance * 0.1

        info_list={"圈数":"%s" %daily_struct.around, "计圈时间":"%s" %self.start_time, "距离":"%s km" %self.distance, "用时":"%s s" %self.duration}
        daily_struct.around+=1
        daily_struct.result.append(info_list)
        self.daily_file.write(str(info_list) + "\n")

    @print_pace_info
    def swim_around_t(self,pstr):
        byte_list = [1, 1, 4, 2 ,2 ,2 ,2 ,2]
        (self.tag, self.num, self.utc, self.lapspeed,self.duration,self.strokes,self.calorie,self.types) = app_bitmap_read_byte(pstr, byte_list)
        self.start_time = self.get_time(self.utc+self.duration*daily_struct.around)


        info_list={"圈数":"%s" %daily_struct.around,"计圈时间":"%s" %self.start_time, "圈速":"%s s/100m" %self.lapspeed, "用时":"%s s" %self.duration,"划水次数":"%s" %self.strokes, "卡路里":"%s kcal" %(self.calorie/1000), "泳姿":"%s" %SWIM_STROCK_TYPE[self.types]}
        daily_struct.around+=1
        daily_struct.result.append(info_list)
        self.daily_file.write(str(info_list) + "\n")

    @print_pace_info
    def sport_run_summary_t(self,pstr):
        byte_list = [1, 1, 4, 2, 2]
        (self.tag, self.num, self.utc, self.distance, self.duration) = app_bitmap_read_byte(pstr, byte_list)
        self.start_time = self.get_time(self.utc)
        self.distance = self.distance * 0.01
        daily_struct.around = 1
        self.mode_name = "低运动量"
        info_list = {"运动模式":"跑步", "开始时间":"%s" %self.start_time, "总距离":"%s km" %self.distance, "总用时":"%s s" %self.duration}
        daily_struct.result.append(info_list)
        self.daily_file.write(str(info_list) + "\n\n")


    @print_pace_info
    def sport_ride_summary_t(self,pstr):
        byte_list = [1, 1, 4, 2, 2]
        (self.tag, self.num, self.utc, self.distance, self.duration) = app_bitmap_read_byte(pstr, byte_list)
        self.start_time = self.get_time(self.utc)
        self.distance = self.distance *0.1
        daily_struct.around = 1
        self.mode_name = "低运动量"
        info_list = {"运动模式":"骑行", "开始时间":"%s" %self.start_time, "总距离":"%s km" % self.distance, "总用时":"%s s" %self.duration}
        daily_struct.result.append(info_list)
        self.daily_file.write(str(info_list) + "\n\n")

    @print_pace_info
    def swim_summary_t(self,pstr):
        byte_list = [1, 1, 4, 2, 2, 2, 2, 1, 1]
        (self.tag, self.num, self.utc, self.duration, self.calorie, self.speed, self.lap_count, self.pool_len,
         self.types) = app_bitmap_read_byte(pstr, byte_list)
        self.start_time = self.get_time(self.utc)
        self.distance = self.lap_count * self.pool_len
        daily_struct.around = 1
        self.mode_name = "低运动量"

        info_list = {"距离": "%s m" %self.distance,"总用时": "%s s" %self.duration,"卡路里":"%skcal" %(self.calorie/1000),"平均配速":"%s s/100m" %self.speed,"泳池长度":"%s m" %self.pool_len,"泳姿":"%s" %SWIM_STROCK_TYPE[self.types]}

        daily_struct.result.append(info_list)
        self.daily_file.write(str(info_list) + "\n\n")

    @print_pace_info
    def STATUS_REVERSE(self, pstr):
        pass

    def which_status(self, pstr):
        head = '0x' + rever_two_bytes(pstr)
        assert len(head) == 6
        tmp = eval(head)
        if DAILY_STATUS['STATUS_HR'] == tmp & 0xfe00:
            return 'STATUS_HR'

        elif DAILY_STATUS['STATUS_SYNC'] == tmp & 0xf800:
            return 'STATUS_SYNC'

        elif DAILY_STATUS['STATUS_DATA_H'] == tmp & 0xf800:
            return 'STATUS_DATA'

        elif DAILY_STATUS['STATUS_TIME'] == tmp & 0xf800:
            return 'STATUS_TIME'

        elif DAILY_STATUS['STATUS_DATE'] == tmp & 0xe000:
            return 'STATUS_DATE'

        elif DAILY_STATUS['STATUS_MODE'] == tmp & 0xc000:
            return 'STATUS_MODE'

        elif DAILY_STATUS['STATUS_DATA_L'] == tmp & 0x8000:
            return 'STATUS_DATA'

        elif DAILY_STATUS['STATUS_START'] == tmp & 0xf800:
            return 'STATUS_START'

        else:
            return 'STATUS_REVERSE'


    def ouput_result(self):
        return daily_struct.result

    #清空列表
    def clear_result(self):
        daily_struct.result=[]
