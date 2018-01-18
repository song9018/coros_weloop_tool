#coding:utf-8
import yf_time
from weloop_common import *

class function(object):

    def __init__(self):
        self.yf_time = yf_time.utc_time()
        self.str=""

    def start_time(self,date_time,time_zone): #"日期：2017/10/12 09:21:00  时区：32"
        year = int(date_time.split("/")[0])
        mon = int(date_time.split("/")[1])
        day = int(date_time.split("/")[2].split()[0])
        hour = int(date_time.split()[1].split(":")[0])
        min = int(date_time.split(":")[1])
        sec = int(date_time.split(":")[2])
        
        if time_zone<0:
            time_zone=256-abs(int(time_zone))*4  #解决负时区问题
        else:
            time_zone = abs(int(time_zone)) * 4

        r_sec = rever_bytes('%08x' % self.yf_time.utc_to_seconds(year-2000, mon, day, hour, min, sec)) #十六进制时间戳
        second_0=self.yf_time.utc_to_seconds(year-2000, mon, day, hour, min, sec)  #十进制时间戳：1240001010
        date = ("1100" + '{0:03b}'.format(int(year)-2015) + '{0:04b}'.format(int(mon)) + '{0:05b}'.format(int(day)))
        date=rever_bytes(hex(int(date, 2)).split("0x")[1])
        time = ("11011" + '{0:05b}'.format(hour) + '{0:06b}'.format(min))
        time = rever_bytes(hex(int(time, 2)).split("0x")[1])
        head="01e8"+date+time+"34f8"+r_sec+rever_bytes('%04x' %time_zone)+"0000"  #日常数据头
        return head,second_0

    def tip_mode(self,mode_str,seconds,energe,step):  #mode+能量值+步数：6bytes
        for i in range(int(seconds)):
            mode_str=mode_str+rever_bytes('%02x'%(int(step)))+rever_bytes('%02x'%(int(energe)))
            self.str=mode_str
        return self.str
    
    #运动标签：跑步、骑行
    def sport_mode(self,min,energe,step):
        mode_str=""
        for i in range(int(min)):
            mode_str=mode_str+rever_bytes('%02x'%(int(step)))+rever_bytes('%02x'%(int(energe)))
            self.str=mode_str
        return self.str
    
    #运动单圈设置：跑步、骑行
    def sport_around(self,utc_second,distance,duration):
        self.sport_around_str="24f8" #mode
        self.sport_around_str=self.sport_around_str+rever_bytes('%08x'%(int(utc_second)))+rever_bytes('%04x'%(int(distance*100)))+rever_bytes('%04x'%(int(duration)))
        return self.sport_around_str
    
    #游泳单圈设置
    def swim_around(self,utc_second, lapspeed,duration,strokes,calorie,types):
        self.swim_around_str = "67f8" #mode
        self.swim_around_str = self.swim_around_str + rever_bytes('%08x' % (int(utc_second))) + rever_bytes(
            '%04x' % (int(lapspeed))) + rever_bytes('%04x' % (int(duration)))+ rever_bytes('%04x' % (int(strokes)))+ rever_bytes('%04x' % (int(calorie)))+ rever_bytes('%04x' % (int(types)))
        return self.swim_around_str
    
    #运动数据概要设置:跑步、骑行
    def sport_summary(self,mode,utc_second, distance,duration):
        if mode=="14f8": #mode
            distance=distance*100
        if mode=="04f8":  #mode
            distance = distance * 10
        self.sport_summary_str =mode
        self.sport_summary_str = self.sport_summary_str + rever_bytes('%08x' % (int(utc_second))) + rever_bytes(
            '%04x' % (int(distance))) + rever_bytes('%04x' % (int(duration)))
        return self.sport_summary_str
    
    #游泳数据概要
    def swim_summary(self,utc_second, duration, calorie, speed, lap_count,pool_len,types):
        self.swim_summary_str = "78f8"  #mode
        self.swim_summary_str = self.swim_summary_str + rever_bytes('%08x' % (int(utc_second))) + rever_bytes(
            '%04x' % (int(duration))) + rever_bytes('%04x' % (int(calorie))) + rever_bytes(
            '%04x' % (int(speed))) + rever_bytes('%04x' % (int(lap_count))) + rever_bytes('%02x' % (int(pool_len)))+ rever_bytes('%02x' % (int(types)))
        return self.swim_summary_str

    #跑步、骑行标签设置调用接口
    def sport_tip_data(self,start_time,duration_time,mode,summary_mode,around_num,around_distance,energy=10,step=10):
        #duration_time单位:min,around_distance单位:km
        #mode:标签mode,summary_mode:概要mode
        #duration_time:运动时常,around_num:圈数,around_distance:单圈距离
        i=0
        str=""
        while i <duration_time:
            #duration_time/around_num:单圈用时
            tip_str=self.sport_mode(duration_time/around_num,energy,step)
            around= self.sport_around(start_time,around_distance,(duration_time/around_num)*60)
            str=str+tip_str+around
            i+=duration_time/around_num
        #around_distance*around_num:总距离
        summary=self.sport_summary(summary_mode,start_time,around_distance*around_num,duration_time*60)
        return mode+str+summary

    #游泳标签调用接口
    def swim_tip_data(self,start_time,duration_time,lap_count,lapspeed,strokes,calorie,types,pool_len,energy=15,step=0):
        #duration_time运动时常--单位:min pool_len泳池长度:m
        #lap_count:圈数,strokes:划水次数,calorie:卡路里,types:泳姿
        mode="0084"
        i = duration_time / lap_count
        str = ""
        while i < duration_time:
            #duration_time / lap_count:单圈用时
            tip_str = self.sport_mode(duration_time / lap_count, energy, step)
            lap = self.swim_around(start_time, lapspeed,(duration_time/lap_count)*60,strokes,calorie,types)
            str = str + tip_str + lap
            i += duration_time / lap_count
        #duration_time*60*100/(pool_len*lap_count)--平均配速
        summary = self.swim_summary(start_time,duration_time*60, calorie, duration_time*60*100/(pool_len*lap_count), lap_count,pool_len,types)
        return mode+str + summary


if __name__ == '__main__':
    func11=function()
    head, second_0=func11.start_time("2017/10/12 09:21:00",8)
    print head+func11.swim_tip_data(second_0,6,3,10,30,10,0,25)

