# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-12-10 21:54:18
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2020-12-18 10:22:06
import os
import json
import base64
try:
	import pymysql
except:
	os.popen("pip install pymysql -i https://mirrors.ustc.edu.cn/pypi/web/simple/").read()


class UseMysql(object):
	def __init__(self):
		db = pymysql.connect("10.69.12.184","maoyongfan",base64.b64decode('bTEyMzQ1Ng==').decode(),"helloBikeDB")
		self.cursor = db.cursor()


	def getTokenInfos(self):
		sql = "select helloBikeToken,user_agent from helloBikeDB.helloBikeUserInfo where id=1" 
		try:
			self.cursor.execute(sql)
			results = self.cursor.fetchall()[0]
			# print(results)
			return results[0],results[1]
		except Exception as e:
			raise Exception("Failed to obtain token information")

	def getFixturePort(self,num):
		sql = "select port FROM helloBikeDB.firture_config where num={}".format(num)

		try:
			self.cursor.execute(sql)
			results = self.cursor.fetchall()[0]
			# print(results)
			return results[0]
		except Exception as e:
			raise Exception("Get jig port abnormal")

if __name__ == '__main__':
	us = UseMysql()
	print(us.getTokenInfos())