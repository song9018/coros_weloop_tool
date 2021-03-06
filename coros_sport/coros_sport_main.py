# coding:utf-8
import sys
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.Qt import *
from coros_run_set import Ui_Form as run_ui_form
from coros_cycle_set import Ui_Form as cycle_ui_form
from coros_pool_swim_set import Ui_Form as pool_swim_ui_form
from coros_open_water_set import Ui_Form as open_water_ui_form
from coros_data_show import Ui_Form as data_show_ui_form
from coros_functions import coros_function
from coros_sport_common import *
from pace_sport_main import decode_sport_data
reload(sys)
sys.setdefaultencoding('utf-8')

map_path="./build/handle.html"
map_path_none="./build/handle_none.html"

Sport_time_set=0
distance=0
start_time=0

#经纬度数据写入html文件
class Lat_Lon(object): #list格式：[[113.12122,23.12131,0],[113.12122,23.12131,0]]
    @classmethod
    def write_lat_lon(self, file_name, list):
        # GPS偏移处理
        for i in range(len(list)):
            list[i][0] = list[i][0] + 0.004843
            list[i][1] = list[i][1] - 0.002995

        with open(file_name, 'r') as fp:
            lines=fp.readlines()
            len_t = len(lines) - 1
        for i in range(len_t):
            # 地图中心点设置
            if "center" in lines[i]:
                data = lines[i].split(':')[1]
                lines[i] = lines[i].replace(data, str(list[0]) + ",\n")
            if 'var lineArr' in lines[i]:
                data = lines[i].split('=')[1]
                lines[i] = lines[i].replace(data, str(list) + "\n")
        with open(file_name, 'w') as fp:
            fp.writelines(lines)

    # 加载地图
    @classmethod
    def run_map(self,file_name,run_ui):
        sc = BrowserScreen(file_name)
        graphicscene = QGraphicsScene()
        graphicscene.addWidget(sc)
        run_ui.graphicsView.setScene(graphicscene)
        run_ui.graphicsView.show()

#pyqt加载浏览器
class BrowserScreen(QtWebKit.QWebView):
    def __init__(self, file_name):
        QtWebKit.QWebView.__init__(self)
        self.resize(851, 381)
        self.setUrl(QUrl(file_name))

        
class CorosRun(QtGui.QWidget, run_ui_form):
    _translate = QtCore.QCoreApplication.translate
    closeWidget = pyqtSignal()
    #lon_lat_list=[]


    def __init__(self,second_utc=0):
        super(CorosRun, self).__init__()
        self.setupUi(self)  # 加载窗体
        self.finish.hide()
        #self.gps_data = Lat_Lon()
        self.coros_func=coros_function()
        self.second_utc=second_utc
        self.data_dic={}

    #加载地图
    def run_map(self, file_name):
        sc = BrowserScreen(file_name)
        graphicscene = QGraphicsScene()
        graphicscene.addWidget(sc)
        self.run_ui.graphicsView.setScene(graphicscene)
        self.run_ui.graphicsView.show()

    def get_ui_data(self):
        #运动时间获取
        self.data_dic["Start_time"] = str(self.start_time.text())
        self.data_dic["Time_zone"] = int(str(self.time_zone.text()))
        self.data_dic["Sport_time_set"]=int(str(self.sport_time_set.text()))
        #总距离、单圈距离获取
        self.data_dic["distance0"]=int(self.distance.text())
        self.data_dic["around0"]=int(self.around.text())
        self.data_dic["kcal0"]=int(self.kcal.text())
        self.data_dic["avg_heart0"]=int(self.heart.text())
        self.data_dic["elevation0"]=int(self.elevation.text())
        self.data_dic["decline0"] = int(self.decline.text())
        self.data_dic["most_step0"] = int(self.most_step.text())
        self.data_dic["most_heart0"] = int(self.most_heart.text())
        self.data_dic["most_speed0"] = int(self.most_pace.text())
        self.data_dic["avg_speed0"] = int(self.avg_pace.text())
        #轨迹地区获取
        self.data_dic["locus_box_status"]=str(self.locus_box.currentText())
        self.data_dic["account"] = str(self.account.text())

        CorosRun.distance=self.data_dic["distance0"]
        CorosRun.Sport_time_set = self.data_dic["Sport_time_set"]

    @pyqtSlot()
    def on_commit_clicked(self):#确认按钮
        self.get_ui_data()
        self.__data,second_1,list_gps=get_data(0,self.coros_func,self.data_dic,self.second_utc,sport_type=0)
        upload_server(self.__data, self.data_dic["Sport_time_set"]*60, self.data_dic["distance0"], self.data_dic["Start_time"],self.data_dic['account'],"跑步")

        #数据展示
        self.run_ui = ShowData()
        self.run_ui.show()
        self.run_ui.sport_data.setText(self.__data)
        Lat_Lon.write_lat_lon(map_path,decode_sport_data(self.__data,"run"))
        Lat_Lon.run_map(map_path,self.run_ui)
        #self.run_map(map_path)  # 加载轨迹地图

    @pyqtSlot()
    def on_finish_clicked(self):  # 确认按钮
        self.get_ui_data()
        self.ori_data_all, self.second_utc, self.list_gps= get_data(3,self.coros_func,self.data_dic,self.second_utc,sport_type=0)
        #logging.info(self.ori_data_all)

        run_data= CorosOpenWater.open_water_data + CorosCycle.cycle_data + self.ori_data_all
        upload_server(run_data, (CorosRun.Sport_time_set+CorosCycle.Sport_time_set+CorosOpenWater.Sport_time_set)*60, (CorosRun.distance+CorosCycle.distance+CorosOpenWater.distance/1000.0), CorosOpenWater.start_utc,self.data_dic['account'],"铁人三项")
        # 数据展示
        self.run_ui = ShowData()
        self.run_ui.show()
        self.run_ui.sport_data.setText(run_data)
        Lat_Lon.write_lat_lon(map_path, decode_sport_data(run_data, "Triathlon"))
        self.run_map(map_path)  # 加载轨迹地图
        self.close()

class CorosCycle(QtGui.QWidget, cycle_ui_form):
    _translate = QtCore.QCoreApplication.translate
    closeWidget = pyqtSignal()
    #cycle_data=""
    #lon_lat_list = []

    def __init__(self,second_utc):
        super(CorosCycle, self).__init__()
        self.setupUi(self)  # 加载窗体
        self.cycle_next.hide()
        self.data_dic={}

        self.coros_func = coros_function()
        self.second_utc=second_utc
        self.gps_data = Lat_Lon()

    # 加载地图
    def run_map(self, file_name):
        sc = BrowserScreen(file_name)
        graphicscene = QGraphicsScene()
        graphicscene.addWidget(sc)
        self.cycle_ui.graphicsView.setScene(graphicscene)
        self.cycle_ui.graphicsView.show()

    def get_ui_data(self):
        # 运动时间获取
        self.data_dic["Start_time"] = str(self.start_time.text())
        self.data_dic["Time_zone"] = int(str(self.time_zone.text()))
        self.data_dic["Sport_time_set"] = int(str(self.sport_time_set.text()))
        # 总距离、单圈距离获取
        self.data_dic["distance0"] = int(self.distance.text())
        self.data_dic["around0"] = int(self.around.text())
        self.data_dic["kcal0"] = int(self.kcal.text())
        self.data_dic["avg_heart0"] = int(self.heart.text())
        self.data_dic["elevation0"] = int(self.elevation.text())
        self.data_dic["decline0"] = int(self.decline.text())
        self.data_dic["most_step0"] = int(self.most_step.text())
        self.data_dic["most_heart0"] = int(self.most_heart.text())
        self.data_dic["most_speed0"] = int(self.most_speed.text())
        self.data_dic["avg_speed0"] = int(self.avg_speed.text())
        # 轨迹地区获取
        self.data_dic["locus_box_status"] = str(self.locus_box.currentText())
        self.data_dic["account"] = str(self.account.text())

        CorosCycle.distance = self.data_dic["distance0"]
        CorosCycle.Sport_time_set = self.data_dic["Sport_time_set"]
    @pyqtSlot()
    def on_commit_clicked(self):  # 确认按钮
        # 获取运动界面相关数据
        self.get_ui_data()
        self.__data,second_1,list_gps = get_data(0,self.coros_func,self.data_dic,self.second_utc,sport_type=4)
        # 数据展示
        upload_server(self.__data, self.data_dic["Sport_time_set"]*60, self.data_dic["distance0"], self.data_dic["Start_time"],self.data_dic['account'],"骑行")

        self.cycle_ui = ShowData()
        self.cycle_ui.show()
        self.cycle_ui.sport_data.setText(self.__data)
        Lat_Lon.write_lat_lon(map_path, decode_sport_data(self.__data, "cycle"))
        self.run_map(map_path)  # 加载轨迹地图

    @pyqtSlot()
    def on_cycle_next_clicked(self):  #
        self.get_ui_data()
        self.ori_data_all, self.second_1, self.list_gps= get_data(2,self.coros_func,self.data_dic,self.second_utc,sport_type=4)
        CorosCycle.cycle_data =self.ori_data_all
        #logging.info(self.ori_data_all)
        self.coros_run1 = CorosRun(self.second_1 + 5)
        self.coros_run1.setWindowTitle(u"coros铁人三项--跑步数据")
        self.coros_run1.show()
        self.coros_run1.commit.hide()
        self.coros_run1.finish.show()
        self.close()


class CorosPoolSwim(QtGui.QWidget, pool_swim_ui_form):
    _translate = QtCore.QCoreApplication.translate
    closeWidget = pyqtSignal()

    def __init__(self,second_utc):
        super(CorosPoolSwim, self).__init__()
        self.setupUi(self)  # 加载窗体
        self.str=""
        self.coros_func = coros_function()
        self.data_dic={}
        self.second_utc=second_utc

    def get_ui_data(self):
        self.data_dic["Start_time"] = str(self.start_time.text())  # 开始时间
        self.data_dic["Time_zone"] = int(self.time_zone.text())  # 时区
        self.data_dic["Sport_time_set"] = int(self.sport_time_set.text())  # 游泳时常设置

        self.data_dic["around0"] = int(self.dis_len.text())  # 泳池长度
        self.data_dic["Lap_count"] = int(self.lap_count.text())  # 游泳圈数设置
        self.data_dic["distance0"] = self.data_dic["around0"] * self.data_dic["Lap_count"]
        self.data_dic["Stroke_count"] = int(self.stroke_count.text())  # 划水次数设置(默认每趟一致)
        self.data_dic["Swim_type"] = int(self.swim_style.text())  # 泳姿设置

        self.data_dic["Kcal"] = int(self.kcal.text()) * 1000  # 卡路里单位:cal
        self.data_dic["Most_pace"] = int(self.most_pace.text()) * 60
        self.data_dic["Avg_pace"] = int(self.avg_pace.text()) * 60  # 配速单位:s
        self.data_dic["Most_str_rate"] = int(self.most_str_rate.text())
        self.data_dic["Avg_str_rate"] = int(self.avg_str_rate.text())
        self.data_dic["Most_swolf"] = int(self.most_str_rate.text())
        self.data_dic["Avg_swolf"] = int(self.avg_swolf.text())
        self.data_dic["account"] = str(self.account.text())
    @pyqtSlot()
    def on_commit_clicked(self):  # 确认按钮
        # 获取运动界面相关数据
        self.get_ui_data()
        self.__data, second_utc, ori_list =get_data(0,self.coros_func,self.data_dic,self.second_utc,sport_type=3)
        #上传服务器
        upload_server(self.__data, self.data_dic["Sport_time_set"]*60, self.data_dic["distance0"]/1000.0, self.data_dic["Start_time"],self.data_dic['account'],"室内游泳")
        # 数据展示
        self.data_set.setText(self.__data)
        decode_sport_data(self.__data, "poolswim")

class CorosOpenWater(QtGui.QWidget, open_water_ui_form):
    _translate = QtCore.QCoreApplication.translate
    closeWidget = pyqtSignal()
    gps_str = ""
    #open_water_data = ""
    #lon_lat_list = []

    def __init__(self,second_utc):
        super(CorosOpenWater, self).__init__()
        self.setupUi(self)  # 加载窗体
        self.open_water_next.hide()
        self.coros_func = coros_function()
        self.data_dic={}
        self.second_utc=second_utc

    # 加载地图
    def run_map(self, file_name):
        sc = BrowserScreen(file_name)
        graphicscene = QGraphicsScene()
        graphicscene.addWidget(sc)
        self.open_water_ui.graphicsView.setScene(graphicscene)
        self.open_water_ui.graphicsView.show()

    def get_ui_data(self):
        self.data_dic["Start_time"] = str(self.start_time.text())  # 开始时间
        self.data_dic["Time_zone"] = int(self.time_zone.text())  # 时区
        self.data_dic["Sport_time_set"] = int(self.sport_time_set.text())  # 游泳时常设置

        self.data_dic["around0"] = int(self.dis_len.text())  # 泳池长度
        self.data_dic["Lap_count"] = int(self.lap_count.text())  # 游泳圈数设置
        self.data_dic["distance0"]=self.data_dic["around0"]*self.data_dic["Lap_count"]
        self.data_dic["Stroke_count"] = int(self.stroke_count.text())  # 划水次数设置(默认每趟一致)
        self.data_dic["Swim_type"] = int(self.swim_style.text())  # 泳姿设置

        self.data_dic["Kcal"] = int(self.kcal.text()) * 1000  # 卡路里单位:cal
        self.data_dic["Most_pace"] = int(self.most_pace.text()) * 60
        self.data_dic["Avg_pace"] = int(self.avg_pace.text()) * 60  # 配速单位:s
        self.data_dic["Most_str_rate"] = int(self.most_str_rate.text())
        self.data_dic["Avg_str_rate"] = int(self.avg_str_rate.text())
        self.data_dic["Most_swolf"] = int(self.most_str_rate.text())
        self.data_dic["Avg_swolf"] = int(self.avg_swolf.text())
        self.data_dic["account"] = str(self.account.text())

        CorosOpenWater.Sport_time_set=self.data_dic["Sport_time_set"]
        CorosOpenWater.distance = self.data_dic["distance0"]


    @pyqtSlot()
    def on_commit_clicked(self):  # 确认按钮
        # 获取运动界面相关数据
        self.get_ui_data()
        self.__data, self.second_utc, list_gps =get_data(0,self.coros_func,self.data_dic,self.second_utc,sport_type=2)
        upload_server(self.__data, self.data_dic["Sport_time_set"]*60, self.data_dic["distance0"]/1000.0, self.data_dic["Start_time"],self.data_dic['account'],"公开水域")
        # 数据展示
        self.open_water_ui = ShowData()
        self.open_water_ui.show()
        self.open_water_ui.sport_data.setText(self.__data)
        Lat_Lon.write_lat_lon(map_path, decode_sport_data(self.__data, "openwater"))
        self.run_map(map_path)  # 加载轨迹地图

    @pyqtSlot()
    def on_open_water_next_clicked(self):  # 铁三下一项操作按钮
        self.get_ui_data()
        self.ori_data_all, self.second_utc, self.list_gps=get_data(1,self.coros_func,self.data_dic,self.second_utc,sport_type=2)
        CorosOpenWater.open_water_data=self.ori_data_all
        CorosOpenWater.start_utc = self.data_dic["Start_time"]


        #logging.info(self.ori_data_all)
        self.coros_cycle1=CorosCycle(self.second_utc + 5)
        self.coros_cycle1.setWindowTitle(u"coros铁人三项--骑行数据")
        self.coros_cycle1.show()
        self.coros_cycle1.commit.hide()
        self.coros_cycle1.cycle_next.show()
        self.close()

#运动数据、日常标签数据展示
class ShowData(QtGui.QWidget, data_show_ui_form):
    _translate = QtCore.QCoreApplication.translate
    closeWidget = pyqtSignal()

    def __init__(self):
        super(ShowData, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = CorosRun(0)

    ui.setWindowTitle(u"运动数据")
    ui.show()
    app.installEventFilter(ui)
    sys.exit(app.exec_())
