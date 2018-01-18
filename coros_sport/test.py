# coding=utf-8
from weloop_daily.weloop_common import *

def bit_to_hex(bit_list,value_list):
    str_hex=""
    bit_list.reverse()
    value_list.reverse()
    for i in range(len(bit_list)):
        zero=""
        str=('{0:0%sb}' %bit_list[i]).format(value_list[i])
        str=hex(int(str, 2)).split("0x")[1]
        for i in range((bit_list[i]/4-len(str))):
            zero+="0"
        str_hex=str_hex+zero+str
    return rever_bytes(str_hex)

def period_bit_to_hex(bit_num,data):
    str_data=""
    for i in range(len(data)):
        str_data=str_data+('{0:0%sb}' %bit_num).format(int(data[i]))
    return str_data


def heart(seconds,index=0):  # 心率1byte
    with open("../cadence_data.txt", "r") as fp:
        cadence_list = fp.readline().strip("\n").split()
        cadence_str = ""

    num = seconds  # 每存四组心率（30s）则存一组步频
    cadence_0 = []
    cadence_1 = []
    for i in range(num):
        cadence_0.append(cadence_list[index])
        index += 1
        if index == 11:  # 11个值存一组
            cadence_1.append(cadence_0)
            cadence_0 = []
            break

        if index > len(cadence_list):  # 循环获取
            index = 0
    if cadence_0 != []:
        while len(cadence_0) < 11:  # 不够--存0
            cadence_0.append(0)
            cadence_1.append(cadence_0)
    cadence_str = cadence_str + period_bit_to_hex(9,(cadence_1[0]))
    cadence_str = rever_bytes(hex(int(cadence_str+"00000", 2)).split("0x")[1].split("L")[0])
    return cadence_str

def peroid_data(file_name,number,bit,data_count,seconds,index=0):  # 心率1byte
    with open(file_name, "r") as fp:
        peroid_list = fp.readline().strip("\n").split()
        peroid_str = ""
    zero="0"*(data_count*8-(number*bit))

    num = seconds  # 每存四组心率（30s）则存一组步频
    peroid_0 = []
    peroid_1 = []
    for i in range(num):
        peroid_0.append(peroid_list[index])
        index += 1
        if index == number:  # 11个值存一组
            peroid_1.append(peroid_0)
            cadence_0 = []
            break

        if index > len(peroid_list):  # 循环获取
            index = 0
    if peroid_0 != []:
        while len(cadence_0) < number:  # 不够--存0
            cadence_0.append(0)
            peroid_1.append(cadence_0)

    peroid_str = peroid_str + period_bit_to_hex(bit,(peroid_1[0]))
    peroid_str = rever_bytes(hex(int(peroid_str+zero, 2)).split("0x")[1].split("L")[0])
    return peroid_str

