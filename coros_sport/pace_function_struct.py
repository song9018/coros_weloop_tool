# coding=utf-8



TAG = {
        0: 'gps_info_struct',
        1: 'peroid_struct', 
        2: 'sportinfo_struct',
        14: 'RECORD_SPORT_TAG_IDLE', 
        15: "RECORD_SPORT_TAG_MAGIC"
        }

GPS_STRUCT = {
            4: "record_gps_diff_t", 
            16: "record_gps_head_t"
            }

SPORT_TYPE = {
            0: '户外跑步', 
            1: '室内跑步', 
            2: '户外游泳', 
            3: '泳池游泳',
            4: '骑行', 
            5: "间歇训练"
            }
              
SWIM_TYPE={
            0:"None",
            1:"自由泳",
            2:"蛙泳",
            3:"仰泳",
            4:"蝶泳"
            }


RECORD_SPORT_TAG_PEROID = {
                            0: "peroid_step_t",
                            1: "peroid_step_len_t",
                            2: "peroid_heartrate_t",
                            3: "peroid_trust_level_t",
                            4: "peroid_calories_t",
                            5: "peroid_altitude_t",
                            6: "peroid_pace_t"
                            }

SPORT_STATE = {
            0: 'sport_start_info_t', 
            1: 'sport_pause_info_t', 
            2: 'sport_resume_info_t', 
            3: 'sport_stop_info_t',
            4: 'Lap_info', 
            5: "sport_summary_info"
            }
               
SPORT_STATUS_DETAILS = {
                    0: "sport_run_summary_info_t", 
                    1: "sport_run_summary_info_t", 
                    2: "sport_swim_summary_info_t",
                    3: "sport_swim_summary_info_t", 
                    4: "sport_bicycle_summary_info_t"
                    }

LAP_INFO = {
            0: "lap_run_info_t", 
            1: "lap_run_info_t", 
            2: "lap_swim_info_t", 
            3: "lap_swim_info_t",
            4: "lap_bicycle_info_t"
            }


INCH = ['公制', '英制']
SAVE = ['丢弃', '保存']
iron_group=["正常模式","铁人三项","铁人三项","铁人三项"]