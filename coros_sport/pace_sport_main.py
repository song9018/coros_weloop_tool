# coding=utf-8
import pace_struct, glob
from pace_common import *
from pace_function_struct import *
from pace_create_kml import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 4k头判断
def string_4k(data):
    head_4k_list = []
    pstr_list = []
    lenth = len(data)
    num_4k = int((lenth / 2) / (4 * 1024))
    if num_4k < lenth / (4 * 1024):
        num_4k += 1
    i = 0
    j = 1
    while num_4k > 0:
        head_4k = data[i:i + 8]
        head_4k_list.append(head_4k)
        if num_4k > 1:
            pstr = data[(j - 1) * 2 * 4 * 1024:j * 2 * 4 * 1024]

            j += 1
        else:
            pstr = data[(j - 1) * 2 * 4 * 1024:]
        pstr = pstr[8:]
        pstr_list.append(pstr)
        i += 2 * 4 * 1024
        num_4k -= 1

    return head_4k_list, pstr_list

def read_sport_4k(filename, path):
    gps_file = open("../result/%s_gps_data.txt" % path, "w")
    sport_file = open("../result/%s_sport_data.txt" % path, "w")

    with  open(filename, "r") as fp:
        data = fp.readlines()
        data = data[0].replace(" ", "")

        head_4k_list, pstr_list = string_4k(data)
        for i in range(len(head_4k_list)):
            bit_list = [4, 4, 6, 10, 8]
            (tag, num, mtu, blockid, checksum) = app_bitmap_read_bit(head_4k_list[i], bit_list)
            read_sport_data(pstr_list[i], mtu, gps_file, sport_file)
    gps_file.close()
    sport_file.close()

def read_sport_data(pstr, mtu, gps_file, sport_file):
    i = 0
    size = 1
    SPORT = pace_struct.sport_struct(gps_file, sport_file)
    while i < len(pstr):
        tag = (eval("0x" + pstr[i:i + size * 2][0:2])) & 0x0f
        num = (eval("0x" + pstr[i:i + size * 2][0:2]) >> 4) & 0x0f
        size = num * mtu

        ppstr = pstr[i:i + size * 2]
        i += size * 2
        assert len(ppstr) == mtu * num * 2
        getattr(SPORT, TAG[tag])(ppstr)

def run_sport_info():
    file = glob.glob("*.txt")
    for i in range(len(file)):
        filename = file[i]
        path_name = filename.split(".txt")[0]
        with  open(filename, "r") as fp:
            data = fp.readlines()
            data = data[0].replace(" ", "")

        if data[0:2].upper() == "1F" and "system_log" not in path_name:
            read_sport_4k(filename, path_name)
            gps_file_fenduan("../result/%s_gps_data.txt" % path_name)

def remove():
    file0 = glob.glob("../result/*")
    for i in range(len(file0)):
        os.remove(file0[i])


if __name__ == '__main__':
    #remove()
    run_sport_info()
    print("解析完成！！！")
