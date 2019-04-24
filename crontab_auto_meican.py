#!/usr/bin/python
# --*-- coding:utf-8 --*--
import json
import ssl
import string
import urllib
import urllib2
import datetime
import time
import jastmencrypt
import requests
from sendEmail import SendEmail
import conf.config as cf

# 获取当前基础时间：年月日
year = datetime.datetime.now().year
month = datetime.datetime.now().month
day = datetime.datetime.now().day

# 周一到周五才订餐
today=time.localtime()
today_number=int(time.strftime("%w", today))
print today_number
# 暂时取消，周六日也订餐，看看啥效果？哈哈
##if today_number in [6,7]:
#if today_number in cf.weekends:
#    exit()

# 0、选择送餐地点
getmulticorpaddress_url = cf.getmulticorpaddress_url

# 1、首先拿到当天所有餐厅列表
targetTime = str(year) + '-' + str(month) + '-' + str(day) + "+15:10"
restaurants_url=cf.restaurants_url + targetTime
values = {
	  'tabUniqueId': cf.tabUniqueId,
      'targetTime': targetTime
    }

headers = cf.headers
getmulticorpaddress_req = urllib2.Request(getmulticorpaddress_url, headers = headers)
getmulticorpaddress_res = urllib2.urlopen(getmulticorpaddress_req).read()
getmulticorpaddress_list = json.loads(getmulticorpaddress_res)
#print getmulticorpaddress_list["data"]
restaurants_req = urllib2.Request(restaurants_url, headers = headers)
restaurants_res = urllib2.urlopen(restaurants_req).read()
restaurants_list = json.loads(restaurants_res)
#print restaurants_list["restaurantList"]

# 2、开始订餐
chose_food_post_url = cf.chose_food_post_url
want_flag = 0
req = 0
i_want_dishId = 0
i_want_dishName = ''
tmp_want_foodlists = []
for restaurant in restaurants_list["restaurantList"]:
    restaurantUniqueId = restaurant["uniqueId"]
    restaurants_show_foodslist_url = cf.restaurants_show_foodslist_url + targetTime + "&restaurantUniqueId=" + restaurantUniqueId
    restaurants_show_foodslist_req = urllib2.Request(restaurants_show_foodslist_url, headers = headers)
    restaurants_show_foodslist_res = urllib2.urlopen(restaurants_show_foodslist_req).read()
    restaurants_show_foodslist_list = json.loads(restaurants_show_foodslist_res)
    dishList = restaurants_show_foodslist_list["dishList"]
    i_want_list = []
    for dish in dishList:
        if dish["name"] == cf.base_dish:
            continue
        if cf.like_dishs[0] in dish["name"] or cf.like_dishs[1] in dish["name"]:
            i_want_list.append(dish["id"])
            i_want_dishName = dish["name"]
            break
        else:
            continue
    tmp_want_foodlists.append(restaurants_show_foodslist_list["sectionList"][0]["dishIdList"])
    if len(i_want_list) > 0:
        want_flag = 1
        # 直接下单，不再往下看了
        i_want_dishId = i_want_list[0]
        order = [{"count":1,"dishId":i_want_dishId}]
        remarks = [{"dishId":str(i_want_dishId),"remark":""}]
        targetTime_new = str(year) + '-' + str(month) + '-' + str(day) + ' 15:10:00'
        values = {
            "tabUniqueId": cf.tabUniqueId,
            "targetTime": targetTime_new,
            "userAddressUniqueId": cf.userAddressUniqueId,
            "corpAddressUniqueId": cf.userAddressUniqueId,
            "remarks": remarks,
            "order": order
        }
        data  = urllib.urlencode(values)
        response = None
        req = requests.Session().post(url = chose_food_post_url, data = data, headers = headers)
        print req.text
        break
print tmp_want_foodlists
if want_flag == 0:
    i_want_dishId = tmp_want_foodlists[0][0]
    order = [{"count":1,"dishId":i_want_dishId}]
    remarks = [{"dishId":str(i_want_dishId),"remark":""}]
    values = {
        "tabUniqueId": cf.tabUniqueId,
        "targetTime": targetTime,
        "userAddressUniqueId": cf.userAddressUniqueId,
        "corpAddressUniqueId": cf.userAddressUniqueId,
        "remarks": remarks,
        "order": order
    }
    data  = urllib.urlencode(values)
    req = requests.Session().post(url = chose_food_post_url, data = data, headers = headers)
    print req.text
    
# sendmail
test = SendEmail()
test.user = "youremail@xxx.com"
# 填写加密后的密码
test.passwd = jastmencrypt.decrypt(119,"XXXXXXXXXXXXXXXXXXXXXXXXXXXX") 
test.to_list = ["xxx@xxx.com"]
test.cc_list = []
test.tag = "【今日订餐结果】" + "周"+ str(today_number) + "订餐"
mailBody = "【订餐结果】：" + "周"+ str(today_number) + "订餐"
if req.status_code != 200 and ("CORP_MEMBER_ORDER_EXISTS" not in str(req.text)):
    test.tag += '失败！'
    mailBody += '失败！<br>【失败原因】： ' + req.text
elif ("CORP_MEMBER_ORDER_EXISTS" in str(req.text)): 
    test.tag += '成功！'
    mailBody += '成功！<br>' + "主人，今天已给您订好了！无法重复预订！"
else:
    test.tag += '成功！'
    if i_want_dishName == '':
        mailBody += '成功！<br>' + "主人，今天随便给您订了一份！就当是惊喜吧！"
    else:
        mailBody += '成功！<br>' + "主人，今天给您订了： " + i_want_dishName
test.send(mailBody)
