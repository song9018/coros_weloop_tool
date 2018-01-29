# coding:utf-8
from functions import Functions
from weloop_daily.functions_daily import function
import sys
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.Qt import *
from sport_ui import Ui_Form
from sport_data_show import Sport_Data_Show
from weloop_daily.weloop_function_struct import choice_sport_type,choice_sport_around,choice_sport_summary
from weloop_daily.weloop_sport_main import read_sport

reload(sys)
sys.setdefaultencoding('utf-8')

map_path="./build/handle.html"
map_path_none="./build/handle_none.html"


#经纬度数据写入html文件
class Lat_Lon(object):
    #list格式：[[[113.12122,23.12131,0],[113.12122,23.12131,0]]]
    def write_lat_lon(self, file_name, list=None, list1=None, list2=None, list3=None): 
        if len(list) == 1:
            list1 = list[0]
        elif len(list) == 2:
            list1 = list[0]
            list2 = list[1]
        elif len(list) == 3:
            list1 = list[0]
            list2 = list[1]
            list3 = list[2]

        file = open(file_name, 'r')
        lines = file.readlines()
        len_t = len(lines) - 1

        for i in range(len_t):
            # 地图中心点设置
            if "center" in lines[i]:
                data = lines[i].split(':')[1]
                lines[i] = lines[i].replace(data, str(list1[0]) + ",\n")
            if 'var lineArr' in lines[i]:
                data = lines[i].split('=')[1]
                lines[i] = lines[i].replace(data, str(list1) + "\n")
            if 'var lineArr1' in lines[i]:
                data = lines[i].split('=')[1]
                lines[i] = lines[i].replace(data, str(list2) + "\n")
            if 'var lineArr2' in lines[i]:
                data = lines[i].split('=')[1]
                lines[i] = lines[i].replace(data, str(list3) + "\n")
        file = open(file_name, 'w')
        file.writelines(lines)
        file.close()


#pyqt加载浏览器
class BrowserScreen(QtWebKit.QWebView):
    def __init__(self, file_name):
        QtWebKit.QWebView.__init__(self)
        self.resize(721, 302)
        self.setUrl(QUrl(file_name))

        
class sport_data(QtGui.QWidget, Ui_Form):
    _translate = QtCore.QCoreApplication.translate
    closeWidget = pyqtSignal()
    gps_str=""

    lon_lat_list=[]
    def __init__(self,sport_type):
        super(sport_data, self).__init__()
        self.setupUi(self)  # 加载窗体

        self.func=Functions()  #运动数据functions文件(weloop_sport)
        self.func_daily=function()  #日常数据数据functions文件(weloop_daily)
        self.run_map(map_path_none)
        self.gps_data=Lat_Lon()
        self.timer =QtCore.QBasicTimer()  #定时器设置
        self.step = 0
        self.sport_type=sport_type  #运动类型：0：跑步、1：骑行

    def timerEvent(self, event):  #进度条设置
            if self.step >= 100:
                self.progressBar.setValue(100)
                self.timer.stop()
                return
            self.step = self.step + 30
            self.progressBar.setValue(self.step)
            
    def onStart(self): #进度条满100%设置
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(100, self)

    #加载地图
    def run_map(self, file_name):
        sc = BrowserScreen(file_name)
        graphicscene = QGraphicsScene()
        graphicscene.addWidget(sc)
        self.graphicsView.setScene(graphicscene)
        self.graphicsView.show()

    # GPS偏移处理
    def add_gps(self, list1):
        for i in range(len(list1)):
            list1[i][0] = list1[i][0] + 0.004843
            list1[i][1] = list1[i][1] - 0.002995
        return list1

    def get_ui_data(self):

        #运动时间获取
        self.Start_time = str(self.start_time.text())
        self.Time_zone = int(str(self.time_zone.text()))
        self.Sport_time_set=int(str(self.sport_time_set.text()))
        #单选框状态获取
        self.heart_checked=int(self.heart.checkState())
        self.cadence_checked=int(self.cadence.checkState())
        self.pace_checked = int(self.pace.checkState())
        #总距离、单圈距离获取
        self.distance0=int(self.distance.text())
        self.around0=int(self.around.text())
        #轨迹地区获取
        self.locus_box_status=str(self.locus_box.currentText())

    @pyqtSlot()
    def on_commit_clicked(self):#确认按钮
        #获取运动界面相关数据
        self.get_ui_data()

        #gps数据生成,self.time_seconds为十进制时间戳
        self.gps_str,self.data_head,self.time_seconds=getattr(self, choice_sport_type[self.sport_type])(self.Start_time, self.Time_zone, self.Sport_time_set)

        #运动数据标签生成,self.second_daily为十进制时间戳
        self.sport_summary=self.func_daily.sport_tip_data(self.time_seconds, self.Sport_time_set, choice_sport_around[self.sport_type], choice_sport_summary[self.sport_type], self.distance0 / self.around0,self.around0, 10, 10)
        self.daily_head,self.second_daily=self.func_daily.start_time(self.Start_time, self.Time_zone)
        
        #数据展示
        self.ui = data_show()
        self.ui.show()
        self.ui.sport_data.setText(self.gps_str)
        self.ui.daily_data.setText(self.daily_head+self.sport_summary)

    @pyqtSlot()
    def on_verify_clicked(self): #验证按钮
        self.progressBar.show()  #进度条
        self.get_ui_data()       #获取运动界面相关数据
        self.onStart()       
        #gps数据生成,self.time_seconds为十进制时间戳
        self.gps_str,self.data_head,self.time_seconds=getattr(self, choice_sport_type[self.sport_type])(self.Start_time, self.Time_zone, self.Sport_time_set)
        
        lon_lat_list=[]  #轨迹数据清零
        
        #解析运动数据,轨迹偏移量设置,默认文件名：1
        lon_lat_list.append(self.add_gps(read_sport(self.gps_str.strip("\n"),"1")))  
        self.gps_data.write_lat_lon(map_path,lon_lat_list)  #html文件写入
        self.run_map(map_path) #加载轨迹地图
    
    #骑行数据
    def create_cycle_gps_data(self,start_time,time_zone,duration_time): #duration_time单位:min
        lon_list=[]
        lat_list=[]
        altitude_list=[]
        #获取文件规划的经纬度数据
        with open("./init_data/sport_gps.txt","r") as fp:
            lines=fp.readlines()
        for line in lines:
            lon_list.append(float(str(line).strip().split(",")[0])*1000000)  #经纬度数值放大
            lat_list.append(float(str(line).strip().split(",")[1]) * 1000000)
            altitude_list.append(float(str(line).strip().split(",")[2]))
        
        #获取文件规划的配速数据
        if self.pace_checked==2:
            with open("./init_data/sport_speed.txt", "r") as fp:
                speed_list = fp.readline().strip("\n").split()
        else:
            speed_list=[0,0,0,0,0,0,0,0,0]  #默认配速为零
        
        #data_head为运动数据头，time_seconds为十进制时间戳
        data_head,time_seconds=self.func.start_time(start_time,time_zone)
        num_gps=0
        num_heart=0
        dur_time=int(duration_time)*60  #duration以s为单位

        gps_str=data_head
        speed_index=0
        while dur_time>0:
            gps_head=self.func.gps_head(time_seconds, lon_list[num_gps], lat_list[num_gps],int(float(speed_list[speed_index])*100), altitude_list[num_gps])
            dur_time-=1
            num_heart+=1
            gps_diff_all=""
            speed_index += 1
            for j in range(len(lon_list)):
                gps_diff=self.func.gps_diff(lon_list[num_gps+1]-lon_list[num_gps],lat_list[num_gps+1]-lat_list[num_gps],int(float(speed_list[speed_index])*100),altitude_list[num_gps+1]-altitude_list[num_gps])
                gps_diff_all=gps_diff_all+gps_diff
                time_seconds+=num_gps

                num_gps+=1
                dur_time -= 1
                num_heart += 1
                speed_index += 1
                if speed_index > len(speed_list) - 2:  #循环写入速度值数据
                    speed_index = 0

                if num_gps%7==0: #每7s(7组gps_diff)写入一组gps_head
                    gps_str=gps_str+gps_head+gps_diff_all
                    if self.heart_checked==2:
                        if num_heart == 280:
                            heart_trust = self.func.heart_and_trust(num_heart)
                            gps_str = gps_str + heart_trust
                            num_heart = 0
                    break
                if num_gps==len(lon_list)-1:  #gps轨迹数据写完循环写入
                    lon_list.reverse()
                    lat_list.reverse()
                    altitude_list.reverse()
                    num_gps=0
                    #break
            #if num_gps==len(lon_list)-1: #gps轨迹数据写完循环写入
                #break
                
        if self.heart_checked == 2:
            if num_heart%280!=0:     #每七组gps数据写入一组心率、可信度
                heart_trust = self.func.heart_and_trust(num_heart)
                gps_str = gps_str + heart_trust
        return gps_str,data_head, time_seconds
    
    #跑步数据
    def create_run_gps_data(self, start_time, time_zone, duration_time):  # duration_time单位：min
        lon_list = []
        lat_list = []
        altitude_list = []
        with open("./init_data/sport_gps.txt", "r") as fp:
            lines = fp.readlines()
        for line in lines:
            lon_list.append(float(str(line).strip().split(",")[0]) * 1000000)
            lat_list.append(float(str(line).strip().split(",")[1]) * 1000000)
            altitude_list.append(float(str(line).strip().split(",")[2]))
        if self.pace_checked==2:
            with open("./init_data/sport_speed.txt", "r") as fp:
                speed_list = fp.readline().strip("\n").split()
        else:
            speed_list=[0,0,0,0,0,0,0,0,0]

        data_head, time_seconds = self.func.start_time(start_time, time_zone)
        num_gps = 0
        num_heart = 0
        dur_time = int(duration_time) * 60
        gps_str = data_head
        speed_index = 0
        while dur_time > 0:
            gps_head = self.func.gps_head(time_seconds, lon_list[num_gps], lat_list[num_gps], int(float(speed_list[speed_index])*100),altitude_list[num_gps])
            dur_time -= 1
            num_heart += 1
            gps_diff_all = ""
            speed_index+=1
            for j in range(len(lon_list)):
                gps_diff = self.func.gps_diff(lon_list[num_gps + 1] - lon_list[num_gps],
                                              lat_list[num_gps + 1] - lat_list[num_gps], int(float(speed_list[speed_index])*100),
                                              altitude_list[num_gps + 1] - altitude_list[num_gps])
                gps_diff_all = gps_diff_all + gps_diff
                time_seconds += num_gps
                num_gps += 1
                dur_time -= 1
                num_heart += 1
                speed_index+=1
                if speed_index>len(speed_list)-2:
                    speed_index=0

                if num_gps % 7 == 0:
                    gps_str = gps_str + gps_head + gps_diff_all
                    if num_heart == 280:
                        cadence=''
                        step_len=''
                        heart_trust=''
                        if self.heart_checked == 2:
                            heart_trust = self.func.heart_and_trust(num_heart)
                        if self.cadence_checked == 2:
                            cadence = self.func.step_cadence(num_heart)
                            step_len = self.func.step_len(num_heart)

                        gps_str = gps_str +cadence + step_len + heart_trust
                        num_heart = 0
                    break
                if num_gps == len(lon_list) - 1:
                    lon_list.reverse()
                    lat_list.reverse()
                    altitude_list.reverse()
                    num_gps=0
                    #break

            #if num_gps == len(lon_list) - 1:
               # break

        if num_heart % 280 != 0: #每七组gps数据写入一组心率、可信度、步频、步长
            cadence1 = ''
            step_len1 = ''
            heart_trust1 = ''
            if self.heart_checked == 2:
                heart_trust1 = self.func.heart_and_trust(num_heart)
            if self.cadence_checked == 2:
                cadence1 = self.func.step_cadence(num_heart)
                step_len1 = self.func.step_len(num_heart)
            gps_str = gps_str + cadence1 + step_len1 + heart_trust1

        return gps_str,data_head, time_seconds

#运动数据、日常标签数据展示
class data_show(QtGui.QWidget, Sport_Data_Show):
    _translate = QtCore.QCoreApplication.translate
    closeWidget = pyqtSignal()

    def __init__(self):
        super(data_show, self).__init__()
        self.setupUi(self)

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = sport_data(1)

    ui.setWindowTitle(u"运动数据仿真工具")
    ui.show()
    app.installEventFilter(ui)
    sys.exit(app.exec_())
