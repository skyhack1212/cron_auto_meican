#!/usr/bin/python
# --*-- coding:utf-8 --*--

# 周末不订餐 6即周六，0即周日----不用改
weekends = [6,0]

# 0、选择送餐地点的url----不用改
getmulticorpaddress_url = "https://meican.com/preorder/api/v2.1/corpaddresses/getmulticorpaddress?namespace=123123123"

# 1、restaurants_url-----不用改
restaurants_url="https://meican.com/preorder/api/v2.1/restaurants/list?tabUniqueId=caf67ef1-3364-4bb2-bb4f-1c871311c187&targetTime="

# 2、'tabUniqueId': 'caf67ef1-3364-4bb2-bb4f-xxxxxxxxxxxxxx'
# tabUniqueId是唯一key，可能每个人的还不一样-----需要改成你自己的
tabUniqueId = 'caf67ef1-3364-4bb2-bb4f-xxxxxxxxxxx'
# userAddressUniqueId是送餐地址，B座2层即xxxxxxxxxxxxx，其他可以自己通过0 打印输出结果后选填送餐地址在这里-----需要改成你自己的送餐地址
userAddressUniqueId ="xxxxxxxxxxxxxx" 

# 3、headers-----需要改成你自己的
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
	"Cookie": '此处填写你的cookie--抓包可得'
}

# 4-0、选餐url
chose_food_post_url = "https://meican.com/preorder/api/v2.1/orders/add"
base_dish = "套餐"
# 上面两个不用改-----这里需要改成你自己想吃的，目前简单处理，只要dish中包含下面的字符串就订。目前只支持2个可选字符串。
like_dishs = ["鱼", "虾"]

# 4-1、订餐url----不用改
restaurants_show_foodslist_url = "https://meican.com/preorder/api/v2.1/restaurants/show?tabUniqueId=caf67ef1-3364-4bb2-bb4f-xxxxxxxxxxx&targetTime="
