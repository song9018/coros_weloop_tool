
typedef __packed struct
{
  uint32_t tag:4;      //tag = 0xF 
  uint32_t num:4;      //存储单元个数
  uint32_t mtu:6;      //存储单元大小 recordsize = mtu * num;
  uint32_t blockid:10; //块ID 
  uint32_t checksum:8; //标记校验
}record_magic_t; //每4K的块标记


typedef __packed struct
{
    uint8_t tag: 4; 
    uint8_t num:4; 
  
    uint32_t utc;
    int32_t lon;
    int32_t lat;
    uint8_t interval;
    uint8_t reserve[2];
}record_gps_head_t;//16byte
STATIC_ASSERT(sizeof(record_gps_head_t) == 16);

typedef __packed struct
{
    uint32_t tag: 4; 
    uint32_t num:4; 
  
    uint32_t lonsign:1;//差值符号
    uint32_t lon:11;   //差值最大2048 当超过范围时会重新存储head
    uint32_t latsign:1;
    uint32_t lat:11;
}record_gps_diff_t; //4byte
STATIC_ASSERT(sizeof(record_gps_diff_t) == 4);

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
//运动周期记录数据: 步频 步长 心率 卡路里 海拔 速度等
typedef __packed struct
{
  uint32_t utc;       //同步周期数据时间戳
  uint8_t interval;  //数据时间间隔, 单位可能为秒或者分钟
  uint8_t reserve[4];
}peroid_time_t;//9+3

typedef __packed struct
{
  uint8_t data[13];//13*8/9=11
}peroid_step_t;//13+3 步频spm 9bit interval=5s

typedef __packed struct
{
  uint8_t data[13];//13*8/9=11
}peroid_step_len_t;//13+3 步长cm 9bit interval=5s

typedef __packed struct
{
  uint8_t data[29];//29*8/8=29 
}peroid_heartrate_t;//29+3 心率bpm 8bit interval=1s

typedef __packed struct
{
  uint8_t data[29];//29*8/2=116
}peroid_trust_level_t;//29+3 心率可信度0~3 2bit interval=1s

typedef __packed struct
{
  uint8_t data[13]; //13*8/16=6
}peroid_calories_t;//13+3 卡路里cal 16bit interval=60s

typedef __packed struct
{
  uint8_t data[29];//29*8/16=14
}peroid_altitude_t;//29+3 海拔m 16bit带符号 interval=5s


typedef __packed struct
{
  uint8_t data[29]; //29*8/16=14
}peroid_pace_t;//29+3 速度 100*km/h 16bit interval=2s

//周期数据格式
typedef __packed struct
{
    uint8_t tag: 4; //记录标签
    uint8_t num:4;  
    
    uint8_t value_type:5;     //周期数据类型
    uint8_t value_reserve:3;
    uint8_t value_tag:1;      //0:peroid_time_t  1:周期数据
    uint8_t value_valid_num:7;//value_tag=0:数据最大位数  value_tag=1:周期数据有效个数  
  
    __packed union
    {
      peroid_time_t time;
      peroid_step_t step_cadence;
      peroid_step_len_t step_len;
      peroid_heartrate_t heartrate;
      peroid_trust_level_t trust_level;
      peroid_calories_t cal;
      peroid_altitude_t altitude;
      peroid_pace_t pace;
    }u;
}record_peroid_t; //结构体数据存储的大小为num*mtu

//////////////////////////////////////////////////////////////////////////////////////////////////////////
//运动信息记录
typedef __packed struct{
  uint32_t start_utc;           //开始记录时间戳
  uint8_t  metric_inch;         //当前运动公英制 //0:公制 1:英制
  int8_t  time_zone;            //当前运动时区
  uint32_t lap_distance_setting;//单圈距离设置 公制cm
  uint8_t reverse[4];          //保留
}sport_start_info_t; //14+2
STATIC_ASSERT(sizeof(sport_start_info_t) == 14);

typedef __packed struct{
  uint32_t stop_utc;      //停止时间戳
  uint8_t save_flag;      //0:丢弃数据 1:保存数据
  uint8_t reverse[9];     //保留
}sport_stop_info_t;//14+2
STATIC_ASSERT(sizeof(sport_stop_info_t) == 14);

typedef __packed struct{
  uint32_t pause_utc;      //暂停运动间戳
  uint8_t reverse[10];     //保留
}sport_pause_info_t;//14+2

STATIC_ASSERT(sizeof(sport_pause_info_t) == 14);

typedef __packed struct{
  uint32_t resume_utc;     //恢复运动间戳
  uint8_t reverse[10];     //保留
}sport_resume_info_t;//14+2
STATIC_ASSERT(sizeof(sport_resume_info_t) == 14);

typedef __packed struct{
	uint32_t current_utc;      //单圈记录时间戳
  uint8_t lap_index;         //单圈序号
	uint32_t lap_duration;     //单圈活动时间
  uint32_t lap_distance;     //单圈活动距离cm(除最后一圈外都等于单圈距离)
  
  uint32_t lap_step;         //单圈活动步数
  uint32_t lap_kcal;	       //单圈活动卡路里 小卡
  uint8_t lap_avg_cadence;   //单圈平均步频
  uint8_t lap_avg_heartrate; //单圈平均心率 
  
  uint8_t reverse[11];        //保留
}lap_run_info_t;//34+2
STATIC_ASSERT(sizeof(lap_run_info_t) == 34);

typedef __packed struct{
	uint32_t current_utc;      //单圈记录时间戳
  uint8_t lap_index;         //单圈序号
	uint32_t lap_duration;     //单圈活动时间  
  uint32_t lap_distance;     //单圈活动距离cm(除最后一圈外都等于单圈距离)

  uint32_t lap_kcal;	       //单圈活动卡路里 小卡
  uint8_t lap_avg_cadence;   //单圈平均踏频
  uint8_t lap_avg_heartrate; //单圈平均心率
  uint16_t lap_avg_power;    //单圈平均功率
  
  uint8_t reverse[13];        //保留
}lap_bicycle_info_t; //34+2

STATIC_ASSERT(sizeof(lap_bicycle_info_t) == 34);

typedef __packed struct{
	uint32_t current_utc;      //单圈记录时间戳
  uint8_t lap_index;         //单圈序号
	uint32_t lap_duration;     //单圈活动时间
  uint32_t lap_distance;     //单圈活动距离cm(除最后一圈外都等于单圈距离)
  
  uint16_t lap_pace;         //单圈配速(游泳的配速由算法计算)
  uint8_t lap_swim_type;     //单圈泳姿
  uint16_t lap_stroke;       //单圈划水次数  
  uint32_t lap_kcal;	       //单圈活动卡路里 小卡
  uint8_t lap_avg_heartrate; //单圈平均心率
  
  uint8_t reverse[11];        //保留
}lap_swim_info_t; //34+2
STATIC_ASSERT(sizeof(lap_swim_info_t) == 34);

typedef __packed struct{
  uint32_t total_distance;      //当前活动总距离cm
  uint32_t sport_duration;      //活动总时间 = stop_utc - start_utc - 暂停时间
  uint8_t  total_lap_num;       //活动总圈数(包括最后半圈)
  uint32_t total_kcal;          //活动总卡路里 小卡
  uint8_t  avg_heartrate;       //活动平均心率  
  uint32_t hrm_vo2max;          //活动最大摄氧量  
  
  uint8_t  avg_cadence;         //活动平均步频
  uint32_t total_step;          //活动总步数    
  uint16_t  total_elevation;    //活动总上升高度m
  uint16_t  total_decline;      //活动总下降高度m  
  
  uint16_t  avg_step_len;        //平均步长
  uint16_t max_cadence;         //最大步频
  uint8_t max_heartrate;        //最大心率
  uint8_t min_heartrate;        //最小心率
  uint16_t max_pace;            //最大配速
  uint16_t avg_pace;            //平均配速
   
  uint8_t reverse[9];           //保留
}sport_run_summary_info1_t; //46+2Byte
STATIC_ASSERT(sizeof(sport_run_summary_info1_t) == 46);


typedef __packed struct{
  uint32_t total_distance;      //当前活动总距离cm
  uint32_t sport_duration;      //活动总时间 = stop_utc - start_utc - 暂停时间
  uint8_t  total_lap_num;       //活动总圈数(包括最后半圈)
  uint32_t total_kcal;          //活动总卡路里 小卡
  uint8_t  avg_heartrate;       //活动平均心率  
  uint32_t hrm_vo2max;          //活动最大摄氧量  
  
  uint32_t total_stroke;        //活动总划水数
  
  uint16_t max_pace;            //最大配速
  uint16_t avg_pace;            //平均配速
  uint8_t max_strk_rate_len;    //最大单趟划水率
  uint8_t avg_strk_rate_len;    //平均单趟划水率
  uint16_t max_swolf_len;       //最大swolf
  uint16_t avg_swolf_len;       //平均swolf 
  
  uint8_t reverse[14];           //保留
}sport_swim_summary_info1_t; //46+2Byte
STATIC_ASSERT(sizeof(sport_swim_summary_info1_t) == 46);

typedef __packed struct{
  uint32_t total_distance;      //当前活动总距离cm
  uint32_t sport_duration;      //活动总时间 = stop_utc - start_utc - 暂停时间
  uint8_t  total_lap_num;       //活动总圈数(包括最后半圈)
  uint32_t total_kcal;          //活动总卡路里 小卡
  uint8_t  avg_heartrate;       //活动平均心率  
  uint32_t hrm_vo2max;          //活动最大摄氧量  
  
  uint8_t  avg_cadence;         //活动平均踏频
  uint16_t lap_avg_power;       //活动平均功率
  
  uint16_t  total_elevation;    //活动总上升高度m
  uint16_t  total_decline;      //活动总下降高度m
  
  uint16_t max_cadence;         //最大踏频
  uint8_t max_heartrate;        //最大心率
  uint8_t min_heartrate;        //最小心率
  uint16_t max_speed;           //最大速度*100
  uint16_t avg_speed;           //平均速度*100
   
  uint8_t reverse[13];           //保留
}sport_bicycle_summary_info1_t; //46+2Byte
STATIC_ASSERT(sizeof(sport_bicycle_summary_info1_t) == 46);

typedef __packed struct
{
    uint8_t tag: 4;         //记录标签
    uint8_t num:4;          //size=num*mtu 
   
    uint8_t sport_type: 4;  //运动类型 SPORT_TYPE_XX
    uint8_t sport_state: 4; //运动状态 SPORT_STATUS_XX

    __packed union
    {
       sport_start_info_t start;   //开始运动信息
       sport_stop_info_t stop;     //结束运动信息
       sport_pause_info_t pause;   //暂停运动信息
       sport_resume_info_t resume; //恢复运动信息
      
       lap_run_info_t lap_run;         //跑步单圈信息
       lap_swim_info_t lap_swim;       //游泳单圈信息
       lap_bicycle_info_t lap_bicycle; //自行车单圈信息
      
       sport_run_summary_info1_t run_summary1;         //跑步运动详情1
       sport_swim_summary_info1_t swim_summary1;       //游泳运动详情1
       sport_bicycle_summary_info1_t bicycle_summary1; //自行车运动详情1
       //...
    } u;
	
	
} record_sportinfo_t; //size=num*mtu
typedef __packed struct{
  uint32_t start_utc;           //开始记录时间戳
  uint8_t  metric_inch;         //当前运动公英制 //0:公制 1:英制
  int8_t  time_zone;            //当前运动时区
  uint32_t lap_distance_setting;//单圈距离设置 公制cm
  uint8_t iron_group;	         //铁人三项，
  //0表示非铁人三项，1,2,3代表铁三的3次运动，序号递增,具体运动类型查询sport_type
  uint8_t reverse[3];          //保留
}sport_start_info_t; //14+2
STATIC_ASSERT(sizeof(sport_start_info_t) == 14);

