#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import re
import json
import os

class AnswerPart1:
    level = ""
    name = ""
    phoneNumber = ""
    
class AnswerPart2:
    province = ""
    city = ""
    area = ""
    town = ""
    detail = ""
    road = ""
    number = ""
    preciseAddress = ""

def getIn():
    str = input()
    return str

def getOut(ap1,ap2):#关键字杀我，output不能用，我没得起名了

    data = {"姓名": "",
            "手机": "",
            "地址": []
            }
    data["姓名"] = ap1.name
    data["手机"] = ap1.phoneNumber

    if ap1.level == "1":
        # 五级地址
        data["地址"] = [ap2.province, ap2.city, ap2.area, ap2.town, ap2.detail]
        json_str = json.dumps(dict(data), ensure_ascii=False)
        print(json_str)
    else:
        # 七级地址
        ap2.road = getroad(ap2.detail)
        user = cutSame(ap2.detail, ap2.road)
        ap2.number = getnumber(user)
        # 如果号找不到的话
        if ap2.number == "":
            ap2.number = ""
            ap2.preciseAddress = user
        else:
            ap2.preciseAddress = cutSame(user, ap2.number)
        data["地址"] = [ap2.province, ap2.city, ap2.area, ap2.town, ap2.road,
                      ap2.number,
                      ap2.preciseAddress]
        json_str = json.dumps(dict(data), ensure_ascii=False)
        print(json_str)

def getBasisMessage(s):
    ap1=AnswerPart1()
    ap1.level=getLevel(s)
    ap1.name=getName(s)
    ap1.phoneNumber=getPhoneNumber(s)
    return ap1

def getLevel(s):
    return s[0]

def getName(s):
    name=s[s.index('!')+1:s.index(',')]
    return name

def getPhoneNumber(s):
    pat = re.compile(r'[1-9]\d{10}')
    phonematch = pat.search(s)
    phone = phonematch.group(0)
    return phone

def cutSame(s1,s2):
    if s2=="":
        return s1
    if len(s1) < len(s2):
        leng = len(s1)
    else:
        leng = len(s2)
    i = 0
    while i < leng:
        if s1[i] != s2[i]:
            break
        i = i + 1
    return s1[i:]

def getroad(user4):
    p = re.compile(r'.+(路|街|巷|桥|岛){1}')
    roadmatch = p.search(user4)

    if roadmatch != None:
        road = roadmatch.group(0)
    else :
        road = ""
    #print(road)
    return road


def getnumber(user6):
    pp = re.compile(r'.+(号|\d){1}')
    numbermatch = pp.search(user6)
    if numbermatch != None:
        number = numbermatch.group(0)
    else :
        number = ""
    return number

def findarea(aareas,user2):
    #areas是现在的所有的县，user2是现在只有乡以后的地址
    atown = user2[0:2]
    for aarea in aareas:#县
        atowns = aarea['children']
        for aatown in atowns:#县下面的镇/乡
            if aatown['name'].find(atown) != -1:
                return aarea['children']

def findcity(cities,user1):
    #cities是现在所有的市，user1是现在的县的地址
    aarea = user1[0:2]
    for acity in cities:
        #市
        aareas = acity['children']
        for abrea in aareas:
            if abrea['name'].find(aarea) != -1:
                return acity['children']



def getAddress(address):
    answerPart2=AnswerPart2()
    #导入外部的json地理数据
    data_json = {}
    filepath = os.path.split(os.path.realpath(__file__))[0]
    filepath = filepath + "\\" + "pcas-code.json"
    with open(filepath, "r+", encoding='utf-8_sig')as f:
        data_json = json.load(f)


        for province in data_json:  # 省份
            one = address[0:2]
            if one in province['name']:
                answerPart2.province = province['name']
                user1 = cutSame(address, answerPart2.province)
                user3 = user1
                user2 = user1

                # 如果是直辖市的话
                if answerPart2.province == "北京" or answerPart2.province == "重庆" or answerPart2.province == "天津" or answerPart2.province == "上海":
                    user1 = answerPart2.province + user1
                cities = province['children']
        if answerPart2.province == "":
            json_str = json.dumps(dict(data), ensure_ascii=False)
            print(json_str)
            return


        for city in cities:  # 市
            two = user1[0:2]
            if two in city['name']:
                answerPart2.city = city['name']
                user2 = cutSame(user1, answerPart2.city)
                areas = city['children']
                user3 = user2
        if answerPart2.city == "":
            answerPart2.city = ""
            areas = findcity(cities, user1)
            user3 = user1
            if areas == {}:
                return


        for area in areas:  # 县
            three = user2[0:2]
            if three in area['name']:
                answerPart2.area = area['name']
                user3 = cutSame(user2, answerPart2.area)
                towns = area['children']
        if answerPart2.area == "":
            answerPart2.area = ""
            towns = findarea(areas, user2)
            user4 = user3
            if towns == {}:
                return


        for town in towns:  # 乡
            four = user3[0:2]
            if four in town['name']:
                answerPart2.town = town['name']
                # print(answerPart2.town)
                user4 = cutSame(user3, answerPart2.town)
        if answerPart2.town == "":
            answerPart2.town = ""
            user4 = user3
            # 如果乡没有被找到的话
            # print(user4)
        answerPart2.detail = user4[:user4.index('.')]

    return answerPart2




def main():
    while 1:
    #准备工作
        userString = getIn()#输入

        if(userString=="END"):
                break
        else:
            answerPart1=AnswerPart1()

            answerPart1=getBasisMessage(userString)

            address=userString[userString.index(','):].replace('!',' ').replace(',','').replace(getPhoneNumber(userString),'')
    #开始处理地址
            answerPart2=AnswerPart2()

            answerPart2=getAddress(address)

            getOut(answerPart1,answerPart2)#输出

main()
