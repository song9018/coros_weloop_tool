#coding:utf-8
from weloop_daily.yf_time import utc_time
from weloop_daily.weloop_common import rever_bytes

class Functions(object):
    def __init__(self):
        self.yf_time = utc_time()
        self.str=""
    def start_time(self,date_time,time_zone): #"日期：2017/10/12 09:21:00  时区：8"
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
        second_0 = self.yf_time.utc_to_seconds(year - 2000, mon, day, hour, min, sec)  #十进制时间戳：1240001010
        sub_head=r_sec+"01000000000000000000"
        sub_head1 = r_sec + "05000000000000000000"
        head="0305"+sub_head+"4305"+sub_head+"1305"+sub_head1+"2305"+sub_head1  #运动数据头
        return head,second_0

    def tip_mode(self,mode_str,seconds,energe,step):  #mode+能量值+步数：6bytes
        for i in range(int(seconds)):
            mode_str=mode_str+rever_bytes('%02x'%(int(step)))+rever_bytes('%02x'%(int(energe)))
            self.str=mode_str
        return self.str

    def heart_and_trust(self,seconds):  #心率1byte+可信度2bit
        with open("./init_data/heart_data.txt","r") as fp:
            heart_list=fp.readline().strip("\n").split()
        heart_str=""
        j=0
        trust_num=0
        num=seconds/5   #5s存一个值
        heart_0=[]
        heart_1=[]
        for i in range(num):
            heart_0.append(heart_list[j])
            j+=1
            if j==14:
                j=0
                heart_1.append(heart_0)  #14个值存一组
                heart_0=[]
        if heart_0!=[]:
            heart_1.append(heart_0)
        for i in range(len(heart_1)):
            heart_head="83"+rever_bytes('%02x' %int(len(heart_1[i]))) #心率mode:83
            trust_num+=1
            str=self.get_frequency(heart_1[i])
            heart_str=heart_str+heart_head+str

            if trust_num%4==0:
                trust_head = "c3" + rever_bytes('%02x' % int(56)) #可信度mode：c3
                heart_str=heart_str+trust_head+"ffffffffffffffffffffffffffff"  #可信度默认为3：ffff

        if trust_num%4!=0:
            num= heart_str.split("830")[-1][0]  #不足14个值，单独存。83+个数(1byte)
            for i in range(14-int(num,16)):
                heart_str=heart_str+rever_bytes('%02x' % int(0))

            trust_head = "c3" + rever_bytes('%02x' % int(trust_num%4))
            heart_and_trust=heart_str+trust_head+"ffffffffffffffffffffffffffff"
        else:
            heart_and_trust = heart_str

        return heart_and_trust

    def step_cadence(self, seconds): #步频数据存储:1byte
        with open("./init_data/cadence_data.txt", "r") as fp:
            cadence_list = fp.readline().strip("\n").split()
            cadence_str = ""
        j = 0

        num = seconds/5/4 #每存四组心率（20s）则存一组步频
        cadence_0 = []
        cadence_1 = []
        for i in range(num):
            cadence_0.append(cadence_list[j])
            j += 1
            if j == 14:  #14个值存一组
                j = 0
                cadence_1.append(cadence_0)
                cadence_0 = []
        if cadence_0 != []:
            cadence_1.append(cadence_0)

        for i in range(len(cadence_1)):
            cadence_head = "93" + rever_bytes('%02x' % int(len(cadence_1[i]))) #步频mode:93
            str = self.get_frequency(cadence_1[i])
            cadence_str = cadence_str + cadence_head + str
            if len(cadence_1[i])!=14:
                str =""
                for j in range(14-len(cadence_1[i])):
                    str =str+ rever_bytes('%02x' % int(0))
                cadence_str=cadence_str+str
        return cadence_str

    def step_len(self, seconds):  #步长数据存储：1byte
        with open("./init_data/step_len_data.txt", "r") as fp:
            step_len_list = fp.readline().strip("\n").split()
            step_len_str = ""
        j = 0
        num = seconds / 5/4 #每存四组心率（20s）则存一组步长
        step_len_0 = []
        step_len_1 = []
        for i in range(num):
            step_len_0.append(step_len_list[j])
            j += 1
            if j == 14:   #14个值存一组
                j = 0
                step_len_1.append(step_len_0)
                step_len_0 = []
        if step_len_0 != []:
            step_len_1.append(step_len_0)
        for i in range(len(step_len_1)):
            step_len_head = "a3" + rever_bytes('%02x' % int(len(step_len_1[i])))
            str = self.get_frequency(step_len_1[i])
            step_len_str = step_len_str + step_len_head + str

            if len(step_len_1[i])!=14:
                str =""
                for j in range(14-len(step_len_1[i])):
                    str =str+ rever_bytes('%02x' % int(0))
                step_len_str=step_len_str+str

        return step_len_str

    def get_frequency(self,heart_list):  #获取频率数据
        str=""
        for i in range(len(heart_list)):
            str=str+rever_bytes('%02x' %int(heart_list[i]))
        return str

    def gps_head(self,start_time,lon,lat,speed,altitude): #gps头：16byte
        if altitude<0:
            altitude=256+altitude  #负海拔
        gps_head = ("0" + '{0:011b}'.format(int(speed)) +'{0:04b}'.format(int(0))) #0表示gps_head标记

        gps_head = (hex(int(gps_head, 2)).split("0x")[1])
        gps_head = rever_bytes("0" * (4 - len(gps_head)) + gps_head)
        gps_data=rever_bytes('%08x' %int(lon))+rever_bytes('%08x' %int(lat))  #lon:4byte+lat:4byte
        gps_altitude=rever_bytes('%04x' %int(altitude))  #海拔2byte
        gps_time=rever_bytes('%08x' %int(start_time))

        gps_str=gps_head+gps_data+gps_altitude+gps_time
        return gps_str

    def gps_diff(self,lon,lat,speed,altitude):
        if altitude<0:
            altitude=256+altitude  #负海拔
        if lon<0:
            lon=65536+lon
        if lat<0:
            lat=65536+lat

        if speed<1:
            gps_head="0100"
        else:
            gps_head = ("0" + '{0:011b}'.format(int(speed)) + '{0:04b}'.format(int(1)))  #1表示gps_diff标记
            gps_head = (hex(int(gps_head, 2)).split("0x")[1])
            gps_head = rever_bytes("0" * (4 - len(gps_head)) + gps_head)
        gps_data = rever_bytes('%04x' % int(lon)) + rever_bytes('%04x' % int(lat))  #lon 2byte，lat 2byte为偏移量
        gps_altitude = rever_bytes('%02x' % int(altitude)) #altitude为偏移量
        gps_time = rever_bytes('%02x' % 1)  #默认1s出值
        gps_str = gps_head + gps_data + gps_altitude + gps_time
        return gps_str


if __name__ == '__main__':
    func=Functions()
    func.step_cadence(285)


