#coding:utf-8

class yf_time_struct(object):
    year = 0
    month = 0
    day = 0
    hour = 0
    minute = 0
    sec = 0
    dayOfWeek = 0#0:Monday

    def trup2str(self, trup):
        s = ''
        for tmp in trup:
            s += '%02d' % tmp
        return s

    def show(self, view = False, rt_str = True):
        out = (self.year, self.month, self.day, self.hour, self.minute, self.sec, self.dayOfWeek)
        if view:
            print out
        if rt_str:
            return self.trup2str(out)
        else:
            return out

class utc_time(object):
    monthtable = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    monthtable_leap = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    
    def __init__(self):
        self.time = yf_time_struct()
        self.MIN_YEAR = 14
        self.MAX_YEAR = 29
        self.JAN1WEEK = 3#2014.1.1-->wed
        self.year = 2000
        #print 'utc_init'

    def modify_utc_start_time(self, min_year=14, jan1week=3, start_year=2000):
        self.MIN_YEAR = min_year
        self.JAN1WEEK = jan1week
        self.year = start_year

    def isleap(self, year):
        year += self.year
        return (((year%400)==0) or (((year%4) == 0) and not((year%100)==0)))

    def seconds_to_utc(self, seconds):
        sec = seconds %60
        minute = seconds / 60
        hour = minute / 60
        day = hour / 24

        self.time.sec = sec
        self.time.minute = minute % 60
        self.time.hour = hour % 24
        self.time.dayOfWeek = (day + self.JAN1WEEK)%7

        year = self.MIN_YEAR
        while(1):
            leap = self.isleap(year)
            if day < (365 + leap):
                break
            day -= 365 + leap
            year += 1

        self.time.year = year%100

        mtbl = self.monthtable_leap if leap > 0 else self.monthtable

        for month in range(12):
            if day < mtbl[month]:
                break
            day -= mtbl[month]

        self.time.day = day + 1
        self.time.month = month + 1

        return self.time
	
	
    def utc_to_seconds(self, year, mon, day, hour, min, sec):
        t_day = 0
        
        if year < self.MIN_YEAR or year > self.MAX_YEAR:
            return 0

        for i in range(year - self.MIN_YEAR):
            t_day += 365 + self.isleap(self.MIN_YEAR + i)
        
        mtbl = self.monthtable_leap if self.isleap(year) > 0 else self.monthtable
        
        for i in range(mon - 1):
            t_day += mtbl[i]
        
        t_day += day - 1
        
        seconds = ((t_day * 24 + hour) * 60 + min) * 60 + sec
        #print rever_bytes('%08x' % seconds)
        #print '%08x' % seconds
        return seconds

def show_utc(your_utc_sec):
    t = utc_time()
    t.seconds_to_utc(your_utc_sec).show(True)
    t.utc_to_seconds(17,5,15,12,51,0)

def gps_utc(your_utc_hour):
    t = utc_time()
    t.modify_utc_start_time(80, 2, 1900)#gps 1980.1.6
    t.seconds_to_utc(your_utc_hour*3600 + 3600*24*5).show(True)
    
if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        print sys.argv[1]
        show_utc(eval(sys.argv[1]))
    else:
        show_utc(0x44427f5d/10)
    

    
