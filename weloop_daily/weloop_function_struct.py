# coding=utf-8

DAILY_STATUS = {
    'STATUS_DATA_L': 0x0000,  # //0xxx xxxx xxxx xxxx  能量值L、步数L
    'STATUS_MODE': 0x8000,  # 10xx xxxx xxxx xxxx    标签模式
    'STATUS_DATE': 0xC000,  # 110x xxxx xxxx xxxx    年月日
    'STATUS_TIME': 0xD800,  # 1101 1xxx xxxx xxxx    时分
    'STATUS_DATA_H': 0xE000,  # 1110 0xxx xxxx xxxx
    'STATUS_SYNC': 0xE800,  # 1110 1xxx xxxx xxxx    SYS_ID
    'STATUS_HR': 0xF000,  # 1111 000x xxxx xxxx     心率
    'STATUS_START': 0xF800,  # 1111 1000 xxxx xxxx  数据头时间戳及时区
    'STATUS_REVERSE': 0xFFFF  # 保留
}

DAILY_SIZE = {
    'STATUS_MODE': 2,
    'STATUS_DATE': 2,
    'STATUS_TIME': 2,
    'STATUS_DATA': 2,
    'STATUS_SYNC': 2,
    'STATUS_HR': 2,
    'STATUS_START': 10,
    'swim_around_t':16,
    'swim_summary_t':16,
    'STATUS_REVERSE': 2
}
SWIM_STROCK_TYPE={
     0:"混合泳",
     1:"自由泳",
     2:"蛙泳",
     3:"仰泳",
     4:"蝶泳",
     255:"混合泳"
     }

DAILY_MODE = {
    0x0001: "摘下",  # off
    0x0002: "睡眠",  # sleep
    0x0010: "散步",  # walk
    0x0020: "健走",  # run  健走
    0x0040: "低运动量",  # low sport
    0x0080: "运动",  # sport
    0x0100: "跑步",  # RUN2  跑步模式
    0x0200: "骑行",  # RIDE  骑行模式
    0x0400: "游泳",  # SWIM 游泳模式
    0x0700: "reverse"
}
struct_map = {
    'F804': 'sport_ride_summary_t',
    'F814': 'sport_run_summary_t',
    'F824': 'sport_around_t',
    'F834': 'sport_start_time_t',
    'F844': 'battery_t',
    'F866': 'swim_around_t',
    'F877': 'swim_summary_t',
    'F867': 'swim_around_t',
    'F878': 'swim_summary_t'
}

RECORD_SPORT_TAG = {
    0: "RECORD_TAG_GPS_HEAD",
    1: "RECORD_TAG_GPS_DIFF",
    2: "RECORD_TAG_SPORT_CADENCE_SMALL",
    3: "RECORD_TAG_SPORT_CADENCE",
    4: "RECORD_TAG_SPORT_INFO",
    15: "RECORD_TAG_EXTEND",
    16: "RECORD_TAG_INVALID"
}

RECORD_SPORT_CADENCE_TAG = {
    0: "record_time_t",
    1: "record_peroid_t"
}
RECORD_SPORT_PEROID = {
    0: "peroid_heartrate_t",
    1: "peroid_step_t",
    2: "peroid_step_len_t",
    3: "peroid_step_speed_t",  # 踏频
    4: "peroid_trust_level_t"
}
SPORT_SIZE = {
    "RECORD_TAG_GPS_HEAD": 16,
    "RECORD_TAG_GPS_DIFF": 8,
    "RECORD_TAG_SPORT_CADENCE": 16,
    "RECORD_TAG_EXTEND": 16,
    "RECORD_TAG_INVALID": 16
}

choice_sport_type={
    0:"create_run_gps_data",
    1:"create_cycle_gps_data"
}

choice_sport_around={
    0:"0081",
    1:"0082"
}

choice_sport_summary={
    0:"14f8",
    1:"04f8"
}

mode_name = {
    "摘下": "0180",
    "睡眠": "0280",
    "散步": "1080",
    "健走": "2080",
    "低运动量": "4080",
    "运动": "8080",
    "跑步": "0081",
    "骑行": "0082",
    "游泳": "0084"
}
