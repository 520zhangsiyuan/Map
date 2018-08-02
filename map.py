#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import sys
import scrapy
import urllib2
import MySQLdb
import requests
from scrapy.utils.project import get_project_settings
import time

mysqlcli = MySQLdb.connect(host = "192.168.1.69", port = 3306, user = "root", passwd = "root", db = "charges" ,charset="utf8")
cursor = mysqlcli.cursor()
headers={
            'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',

}
url = 'https://restapi.amap.com/v3/place/polygon?polygon='
left_long = 113.98754139
left_lat = 22.8192292510
right_long = 114.02177139
right_lat = 22.792259251
location = str(left_long)+','+str(left_lat)+'|'+str(right_long)+','+str(right_lat)
types = '010000'
key = '&output=json&offset=25&extensions=all&key=你的Key&page='
page = 1
a = 1
pages = 0
new_url = ''
settings = get_project_settings()
#start_url = url + location +'&types='+type+key+str(page)
for i in range (1,18):
	if left_long < 114.3237433428:
		left_long += 0.03423
		right_long += 0.03423
		print '*************************************'
		right_lat = 22.792259251
		left_lat = 22.8192292510
		for j in range (1,18):
			time.sleep(1)
			left_lat -= 0.02697
			right_lat -= 0.02697
			if a == 1:
				left_lat = 22.684379251
				right_lat = 22.657409251
				a +=1
			
			print location
			if left_lat < 22.3477008346:
				break
			for k in range (0,166):
				types = settings['TYPES'][k]
				#time.sleep(0.2)
				print '----------------------------------------'
				a = ''
				pages = 0
				boolean = True
				while boolean:
					#result = ''
					try:
						#time.sleep(0.1)
						pages += 1
						location = str(left_long)+','+str(left_lat)+'|'+str(right_long)+','+str(right_lat)
						new_url = url + location +'&types='+types+key+str(pages)
						#print new_url + '=================================='
				

#						print '================================='
						res =  urllib2.Request(new_url,headers=headers)
						result = urllib2.urlopen(res)
						#r1 = json.loads(result,strict=False)
				        	result = result.read()		
					
						r1 = json.loads(result,strict=False)
						print new_url
						#a = r1['count']
						#print id[a]
						#print id['0']
						#if r1['count'] == '0':
						#	print '没有了***********************************************
						for d in range (0,24):
							try:
								#唯一ID
        							pid = r1['pois'][d]['id']
					   			 #名称
					       			name = "".join(r1['pois'][d]['name']).replace('\'','') 
					     			 #类型
					       			types1 = "".join(r1['pois'][d]['type']).replace('\'','')
					       			#地址
					       			address = "".join(r1['pois'][d]['address']).replace('\'','')
					       			#经纬度
					       			location = "".join(r1['pois'][d]['location']).replace('\'','')
					       			#电话
					       			tel = "".join(r1['pois'][d]['tel']).replace('\'','')
					       			#邮编
					       			postcode = "".join(r1['pois'][d]['postcode']).replace('\'','')
					       			#email 邮箱
					       			email = "".join(r1['pois'][d]['email']).replace('\'','')
					       			#所在省份名称
					       			pname = "".join(r1['pois'][d]['pname']).replace('\'','')
					       			#城市名
					       			cityname = "".join(r1['pois'][d]['cityname']).replace('\'','')
					       			#区域名称
					       			adcode = "".join(r1['pois'][d]['adname']).replace('\'','')
					       			#入口经纬度
					       			entr_location = "".join(r1['pois'][d]['entr_location']).replace('\'','')
					       			#出口经纬度
					      			exit_location = "".join(r1['pois'][d]['exit_location']).replace('\'','')
					      			#特色
					       			tag = "".join(r1['pois'][d]['tag']).replace('\'','')[0:500]
					       			#评分
					       			rating = "".join(r1['pois'][d]['biz_ext']['rating']).replace('\'','')
								sql = "INSERT INTO map(pid,name,types,address,location,tel,postcode,email,pname,cityname,adcode,entr_location,exit_location,tag,rating) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(pid,name,types1,address,location,tel,postcode,email,pname,cityname,adcode,entr_location,exit_location,tag,rating)
								#print new_url
								#print sql
								cursor.execute(sql)
			                            			# 提交事务
                        		           		mysqlcli.commit()     
							    
							except IndexError,e:
								#print e.message
								boolean = False
								break
							except urllib2.URLError,e:
								time.sleep(1)
								continue
							except KeyError,e:
								time.sleep(1)
								continue
								#print boolean
					except :
						time.sleep(60)
						continue
#关闭游标
cursor.close()
