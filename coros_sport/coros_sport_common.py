# coding:utf-8
import logging
logging.basicConfig(level=logging.ERROR) #DEBUG，INFO，WARNING，ERROR


def get_data(iron_group,coros_func,data_dic,second_1,sport_type):
    #sport start info:start_head/start_length/start_utc
    start_info, start_info_len, utc_second = normal_start_data(coros_func, data_dic, iron_group,second_1,sport_type)
    ori_data, ori_data_list, start_info_len, utc_second = common_get_data(utc_second, start_info_len,data_dic["Sport_time_set"],coros_func, data_dic, sport_type)
    ori_data_list, utc_second = sport_summary(coros_func, data_dic, sport_type, ori_data, start_info_len,ori_data_list, utc_second, iron_group)

    ori_data_all = start_info + ori_data_list[0]
    num_index = 1
    while num_index < len(ori_data_list):
        check_sum=coros_func.check_sum(15, 1, 4, num_index, 99)
        ori_data_all += coros_func.string_4k(15, 1, 4, num_index, check_sum) + ori_data_list[num_index]
        num_index += 1
    return ori_data_all, utc_second, ori_data_list


def common_get_data(second_0, start_len, Sport_time_set, coros_func, data_dic, sport_type):
    gps = ""
    gps_list,lon_list,lat_list,altitude_list = [],[],[],[]
    with open("./init_data/sport_gps.txt", "r") as fp:
        lines = fp.readlines()
    for line in lines:
        lon_list.append(int(float(str(line).strip().split(",")[0]) * 1000000))
        lat_list.append(int(float(str(line).strip().split(",")[1]) * 1000000))
    num_gps,num,num_heart,num_heart_trust,num_step,num_step_len,num_kcal,num_altitude,num_pace,num_lap = 0,0,0,0,0,0,0,0,0,0

    dur_time = int(Sport_time_set) * 60
    while dur_time > 0:
        gps_head = coros_func.gps_head(0, 4, second_0, lon_list[num_gps], lat_list[num_gps], 1, 0)
        dur_time -= 1
        num += 1
        gps_diff_all = ""
        for j in range(len(lon_list)):
            gps_diff = coros_func.gps_diff(0, 1, lon_list[num_gps + 1] - lon_list[num_gps],lat_list[num_gps + 1] - lat_list[num_gps])

            gps_diff_all = gps_diff_all + gps_diff
            second_0 += 1
            num_gps += 1

            if dur_time <= 0:
                break
            if num_gps % 7 == 0:  #每7s写入gps_head
                second_0 += 1
                if sport_type==3:  #泳池游泳忽略gps写入
                    gps_head=""
                    gps_diff_all=""
                gps, gps_list, start_len = add_4k_end(gps, gps_head + gps_diff_all, start_len, gps_list)

                #1s出值
                if num % 28 == 0:
                    """
                    record_peroid_t = {
                        "tag": 4,  # 记录标签
                        "num": 4,
                        "c_value_type": 5,  # 周期数据类型
                        "d_value_reserve": 3,
                        "e_value_tag": 1,  # 0":peroid_time_t  1":周期数据
                        "f_value_valid_num": 7,  # value_tag=0":数据最大位数  value_tag=1":周期数据有效个数
                    }  # 结构体数据存储的大小为num*mtu
                    """
                    speed=""
                    heart = coros_func.peroid_t(1, 8, 2, 0, 1, 29) + coros_func.heart(29, num_heart, "heart")
                    if sport_type!=3:
                        #speed 2s出值
                        speed = coros_func.peroid_t(1, 8, 6, 0, 1, 14) + coros_func.pace(14, num_pace, "speed")
                    gps, gps_list, start_len = add_4k_end(gps, heart + speed, start_len, gps_list)

                #5s存储一个值，55s存储一组数据
                if num % 56 == 0:
                    step,step_len="",""
                    if sport_type != 3 and sport_type != 4:
                        step = coros_func.peroid_t(1, 4, 0, 0, 1, 11) + coros_func.step_cadence(11, num_step,"step")
                        step_len = coros_func.peroid_t(1, 4, 1, 0, 1, 11) + coros_func.step_len(11, num_step_len,"step_len")
                    altitude = coros_func.peroid_t(1, 8, 5, 0, 1, 14) + coros_func.altitude(14, num_altitude,"altitude")
                    gps, gps_list, start_len = add_4k_end(gps, step + step_len + altitude, start_len, gps_list)

                # 1s存储一个值，可信度116个，对应心率4组
                if num % 112 == 0:
                    trust = coros_func.peroid_t(1, 8, 3, 0, 1, 116) + coros_func.trust_level(116,num_heart_trust,"trust")
                    gps, gps_list, start_len = add_4k_end(gps, trust, start_len, gps_list)
                if num % 360 == 0:
                    kcal = coros_func.peroid_t(1, 4, 4, 0, 1, 6) + coros_func.calories(6, num_kcal, "kcal")
                    gps, gps_list, start_len = add_4k_end(gps,kcal, start_len, gps_list)
                break
            if num_gps == len(lon_list) - 1:
                #循环获取经纬度信息
                lon_list.reverse()
                lat_list.reverse()
                altitude_list.reverse()
                num_gps = 0
            dur_time -= 1
            num += 1

        gps, gps_list, start_len, num_lap = sport_lap(num, data_dic, coros_func, num_lap, second_0, gps, gps_list,start_len, sport_type)
    return gps, gps_list, start_len, second_0

def sport_lap(num, data_dic, coros_func, num_lap, second_0, gps, gps_list, start_len, sport_type):
    lap_info=""
    if num % ((int(data_dic["Sport_time_set"]) * 60) / int((data_dic["distance0"] / data_dic["around0"]))) < 8:
        around = coros_func.tag_sport_type(2, 9, sport_type, 4)  # 2:sportinfo_struct ，mtu:4 ,sport_type:0,sport_state：0
        num_lap += 1
        if sport_type == 0:  # 室外跑步
            lap_info = around + coros_func.lap_run_info(second_0, num_lap, (int(data_dic["Sport_time_set"]) * 60) / int((data_dic["distance0"] / data_dic["around0"])), data_dic["around0"] * 100000, 170,data_dic["kcal0"] * 1000, 170,180, 0)

        if sport_type == 2 or sport_type == 3  :  # 公开水域
            lap_info = around + coros_func.lap_swim_info(second_0, num_lap,(int(data_dic["Sport_time_set"]) * 60) / int((data_dic["Lap_count"])),data_dic["around0"] * 100, 60, data_dic["Swim_type"], data_dic["Stroke_count"],data_dic["Kcal"] / data_dic["Lap_count"], 180,0)

        if sport_type == 4:  # 骑行
            lap_info = around + coros_func.lap_bicycle_info(second_0, num_lap,(int(data_dic["Sport_time_set"]) * 60) / int((data_dic["distance0"] / data_dic["around0"])),data_dic["around0"] * 100000, data_dic["kcal0"] * 1000, 0,180, 0, 0)

        gps, gps_list, start_len=add_4k_end(gps, lap_info, start_len, gps_list)
    return gps, gps_list, start_len, num_lap


#运动概要数据
def sport_summary(coros_func, data_dic, sport_type, gps, start_len, gps_list, second_0, iron_group):
    sum = coros_func.tag_sport_type(2, 12, sport_type, 5)
    sum_info=""
    #室外跑步
    if sport_type == 0:
        sum_info = sum + coros_func.sport_run_summary(data_dic["distance0"] * 100000, data_dic["Sport_time_set"] * 60,
                                                      data_dic["distance0"] / data_dic["around0"],
                                                      data_dic["kcal0"] * 1000,
                                                      data_dic["avg_heart0"], 70, 170, 300, data_dic["elevation0"],
                                                      data_dic["decline0"], 80, data_dic["most_step0"],
                                                      data_dic["most_heart0"], 90,
                                                      data_dic["most_speed0"], data_dic["avg_speed0"], 0)
    #游泳模式
    if sport_type == 2 or sport_type == 3:
        sum_info = sum + coros_func.sport_swim_summary(data_dic["distance0"] * 100,
                                                       data_dic["Sport_time_set"] * 60, data_dic["Lap_count"], data_dic["Kcal"], 170, 0,
                                                       data_dic["Stroke_count"], data_dic["Most_pace"], data_dic["Avg_pace"],
                                                       data_dic["Most_str_rate"], data_dic["Avg_str_rate"], data_dic["Most_swolf"],
                                                       data_dic["Avg_swolf"],0)
    #骑行
    if sport_type == 4:
        sum_info = sum + coros_func.sport_bicycle_summary(data_dic["distance0"] * 100000,
                                                          data_dic["Sport_time_set"] * 60,
                                                          data_dic["distance0"] / data_dic["around0"],
                                                          data_dic["kcal0"] * 1000, data_dic["avg_heart0"], 0, 0, 0,
                                                          data_dic["elevation0"], data_dic["decline0"],
                                                          data_dic["most_step0"], data_dic["most_heart0"], 90,
                                                          data_dic["most_speed0"], data_dic["avg_speed0"], 0)

    gps, gps_list, start_len = add_4k_end(gps, sum_info, start_len, gps_list)

    # 结束
    end = coros_func.tag_sport_type(2, 4, sport_type, 3)
    end_info = end + coros_func.stop_time(second_0)
    gps, gps_list, start_len = add_4k_end(gps, end_info, start_len, gps_list)
    gps_list=Triathlon_4k_end(iron_group,gps,gps_list,sport_type,start_len)
    return gps_list, second_0


#运动开始信息
def normal_start_data(coros_func, data_dic, iron_group, sec_utc,sport_type):
    str_4k = coros_func.string_4k(15, 1, 4, 0, 35)
    peroid_time0 = ""
    interval_list = [5, 5, 1, 1, 60, 2]
    bit_max = [9, 9, 8, 2, 16, 16]
    index_type = [0, 1, 2, 3, 4, 6]
    if sport_type==2 or sport_type==3:
        around0=data_dic["around0"]*100 #游泳单圈信息单位设置
    else:
        around0 = data_dic["around0"]*100000  #跑步、骑行单圈信息单位设置
    start_time, second_0 = coros_func.start_time(data_dic["Start_time"], data_dic["Time_zone"], around0,iron_group, sec_utc)

    start_info0 = coros_func.tag_sport_type(2, 4, sport_type, 0)  # 2:sportinfo_struct ，mtu:4 ,sport_type:0,sport_state：0
    for i in range(6): #暂时没有区分每项运动中周期数据是否存在(游泳无计步等)
        peroid_time0 += (coros_func.peroid_t(1, 3, index_type[i],0, 0, bit_max[i])
                         + coros_func.peroid_time_t(second_0 + i, interval_list[i], 0))  # 1:peroid_struct  0:gps
    data = str_4k + start_info0 + start_time + peroid_time0
    return data, len(data)-len(str_4k), second_0


#单项运动4k数据长度补全
def add_4k_end(gps, lap_info, start_len, gps_list):
    gps_len = gps + lap_info
    if len(gps_len) >= 8184 - start_len:
        gps_list = none_4k_get(gps, start_len, gps_list)
        gps = lap_info
        start_len = 0
    else:
        gps = gps + lap_info
    return gps, gps_list,start_len


#铁人三项4k数据长度补全
def Triathlon_4k_end(iron_group,gps,gps_list,sport_type,start_len):
    if iron_group != 0 and sport_type!=0:
        gps_list=none_4k_get(gps,start_len,gps_list)
    else:
        gps_list.append(gps)  #解决单项运动最后一段数据小于4k时被丢弃的问题
    return gps_list


# 运动结束时填充无效数据(4k补全)，减少工作量
def none_4k_get(gps,start_len,gps_list):
    if (8184 - len(gps) - start_len) / 120 > 0:
        for i in range(int((8184 - len(gps) - start_len) / 120)):
            gps = gps + "f" * 120
        if (8184 - len(gps) - start_len) % 120 != 0:
            gps_list.append(
                gps + "%sf" % ('%01x' % (((8184 - len(gps) - start_len) % 120) / 8)) + (((8184 - len(gps) - start_len) % 120 - 2) *"f"))
    else:
        if (8184 - len(gps) - start_len) % 120 != 0:
            gps_list.append(
                gps + "%sf" % ('%01x' % ((8184 - len(gps) - start_len) / 8)) + ((8182 - len(gps) - start_len) * "f"))
    return gps_list