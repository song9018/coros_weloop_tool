# coding:utf-8

record_4k_t = {
    "a_tag": 4,  # tag = 0xF
    "b_num": 4,  # 存储单元个数
    "c_mtu": 6,  # 存储单元大小 recordsize = mtu * num,
    "d_blockid": 10,  # 块ID
    "e_checksum": 8,  # 标记校验
}  # 每4K的块标记

record_gps_head_t = {
    "a_tag": 4,
    "b_num": 4,
    "c_utc": 32,
    "d_lon": 32,
    "e_lat": 32,
    "f_interval": 8,
    "g_reserve": 16,
}  # 16byte

record_gps_diff_t = {
    "a_tag": 4,
    "b_num": 4,
    "c_lonsign": 1,  # 差值符号
    "d_lon": 11,  # 差值最大2048 当超过范围时会重新存储head
    "e_latsign": 1,
    "f_lat": 11,
}  # 4byte

# 运动周期记录数据": 步频 步长 心率 卡路里 海拔 速度等
# 周期数据格式

record_peroid_t = {
    "a_tag": 4,  # 记录标签
    "b_num": 4,
    "c_value_type": 5,  # 周期数据类型
    "d_value_reserve": 3,
    "e_value_tag": 1,  # 0":peroid_time_t  1":周期数据
    "f_value_valid_num": 7,  # value_tag=0":数据最大位数  value_tag=1":周期数据有效个数
}  # 结构体数据存储的大小为num*mtu

peroid_time_t = {
    "a_utc": 4,  # 同步周期数据时间戳
    "b_interval": 1,  # 数据时间间隔, 单位可能为秒或者分钟
    "c_reserve": 4,
}  # 9+3

peroid_step_t = {
    "step": 13,  # 13*8/9=11
}  # 13+3 步频spm 9bit interval=5s

peroid_step_len_t = {
    "step_len": 13,  # 13*8/9=11
}  # 13+3 步长cm 9bit interval=5s

peroid_heartrate_t = {
    "heartrate": 29,  # 29*8/8=29
}  # 29+3 心率bpm 8bit interval=1s

peroid_trust_level_t = {
    "trust_level": 29,  # 29*8/2=116
}  # 29+3 心率可信度0~3 2bit interval=1s

peroid_calories_t = {
    "calories": 13,  # 13*8/16=6
}  # 13+3 卡路里cal 16bit interval=60s

peroid_altitude_t = {
    "altitude": 29,  # 29*8/16=14
}  # 29+3 海拔m 16bit带符号 interval=5s

peroid_pace_t = {
    "pace": 29,  # 29*8/16=14
}  # 29+3 速度 100*km/h 16bit interval=2s


# 运动信息记录
record_sport_info_t = {
    "a_tag": 4,  # 记录标签
    "b_num": 4,  # size=num*mtu
    "c_sport_type": 4,  # 运动类型 SPORT_TYPE_XX
    "d_sport_state": 4,  # 运动状态 SPORT_STATUS_XX
}  # size=num*mtu

sport_start_info_t = {
    "a_start_utc": 4,  # 开始记录时间戳
    "b_metric_inch": 1,  # 当前运动公英制 #0":公制 1":英制
    "c_time_zone": 1,  # 当前运动时区
    "d_lap_distance_setting": 4,  # 单圈距离设置 公制cm
    "e_iron_group":1,
    "f_reverse": 3,  # 保留
}  # 14+2

sport_stop_info_t = {
    "a_stop_utc": 4,  # 停止时间戳
    "b_save_flag": 1,  # 0":丢弃数据 1":保存数据
    "c_reverse": 9,  # 保留
}  # 14+2

lap_run_info_t = {
    "a_current_utc": 4,  # 单圈记录时间戳
    "b_lap_index": 1,  # 单圈序号
    "c_lap_duration": 4,  # 单圈活动时间
    "d_lap_distance": 4,  # 单圈活动距离cm(除最后一圈外都等于单圈距离)
    "e_lap_step": 4,  # 单圈活动步数
    "f_lap_kcal": 4,  # 单圈活动卡路里 小卡
    "g_lap_avg_cadence": 1,  # 单圈平均步频
    "h_lap_avg_heartrate": 1,  # 单圈平均心率
    "i_reverse": 11,  # 保留
}  # 34+2

lap_bicycle_info_t = {
    "a_current_utc": 4,  # 单圈记录时间戳
    "b_lap_index": 1,  # 单圈序号
    "c_lap_duration": 4,  # 单圈活动时间
    "d_lap_distance": 4,  # 单圈活动距离cm(除最后一圈外都等于单圈距离)
    "e_lap_kcal": 4,  # 单圈活动卡路里 小卡
    "f_lap_avg_cadence": 1,  # 单圈平均踏频
    "g_lap_avg_heartrate": 1,  # 单圈平均心率
    "h_lap_avg_power": 2,  # 单圈平均功率
    "i_reverse": 13,  # 保留
}  # 34+2

lap_swim_info_t = {
    "a_current_utc": 4,  # 单圈记录时间戳
    "b_lap_index": 1,  # 单圈序号
    "c_lap_duration": 4,  # 单圈活动时间
    "d_lap_distance": 4,  # 单圈活动距离cm(除最后一圈外都等于单圈距离)

    "e_lap_pace": 2,  # 单圈配速(游泳的配速由算法计算)
    "f_lap_swim_type": 1,  # 单圈泳姿
    "g_lap_stroke": 2,  # 单圈划水次数
    "h_lap_kcal": 4,  # 单圈活动卡路里 小卡
    "i_lap_avg_heartrate": 1,  # 单圈平均心率

    "j_reverse": 11,  # 保留
}  # 34+2

sport_run_summary_info_t = {
    "a_total_distance": 4,  # 当前活动总距离cm
    "b_sport_duration": 4,  # 活动总时间 = stop_utc - start_utc - 暂停时间
    "c_total_lap_num": 1,  # 活动总圈数(包括最后半圈)
    "d_total_kcal": 4,  # 活动总卡路里 小卡
    "e_avg_heartrate": 1,  # 活动平均心率
    "f_hrm_vo2max": 4,  # 活动最大摄氧量

    "g_avg_cadence": 1,  # 活动平均步频
    "h_total_step": 4,  # 活动总步数
    "i_total_elevation": 2,  # 活动总上升高度m
    "j_total_decline": 2,  # 活动总下降高度m

    "k_avg_step_len": 2,  # 平均步长
    "l_max_cadence": 2,  # 最大步频
    "m_max_heartrate": 1,  # 最大心率
    "n_min_heartrate": 1,  # 最小心率
    "o_max_pace": 2,  # 最大配速
    "p_avg_pace": 2,  # 平均配速
    "q_reverse": 9,  # 保留
}  # 46+2Byte

sport_swim_summary_info_t = {
    "a_total_distance": 4,  # 当前活动总距离cm
    "b_sport_duration": 4,  # 活动总时间 = stop_utc - start_utc - 暂停时间
    "c_total_lap_num": 1,  # 活动总圈数(包括最后半圈)
    "d_total_kcal": 4,  # 活动总卡路里 小卡
    "e_avg_heartrate": 1,  # 活动平均心率
    "f_hrm_vo2max": 4,  # 活动最大摄氧量
    "g_total_stroke": 4,  # 活动总划水数
    "h_max_pace": 2,  # 最大配速
    "i_avg_pace": 2,  # 平均配速
    "j_max_strk_rate_len": 1,  # 最大单趟划水率
    "k_avg_strk_rate_len": 1,  # 平均单趟划水率
    "l_max_swolf_len": 2,  # 最大swolf
    "m_avg_swolf_len": 2,  # 平均swolf
    "n_reverse": 14,  # 保留
}  # 46+2Byte

sport_bicycle_summary_info_t = {
    "a_total_distance": 4,  # 当前活动总距离cm
    "b_sport_duration": 4,  # 活动总时间 = stop_utc - start_utc - 暂停时间
    "c_total_lap_num": 1,  # 活动总圈数(包括最后半圈)
    "d_total_kcal": 4,  # 活动总卡路里 小卡
    "e_avg_heartrate": 1,  # 活动平均心率
    "f_hrm_vo2max": 4,  # 活动最大摄氧量

    "g_avg_cadence": 1,  # 活动平均踏频
    "h_lap_avg_power": 2,  # 活动平均功率

    "i_total_elevation": 2,  # 活动总上升高度m
    "j_total_decline": 2,  # 活动总下降高度m

    "k_max_cadence": 2,  # 最大踏频
    "l_max_heartrate": 1,  # 最大心率
    "m_min_heartrate": 1,  # 最小心率
    "n_max_speed": 2,  # 最大速度*100
    "o_avg_speed": 2,  # 平均速度*100

    "p_reverse": 13,  # 保留
}  # 46+2Byte
