# coding:utf8

from urllib import request
import urllib
import re
import sqlite3

# html下载器，用于从指定的url下载html数据
# 包含一个初始化程序和一个download()方法
class HtmlDownloader(object):

	#初始化程序
	def __init__(self):
		#创建连接打开sqlite数据库文件
		self.conn = sqlite3.connect('douban_movies.sqlite')
		self.cur = self.conn.cursor()

	#从指定的url地址下载html数据
	def download(self, url):
		if url is None:
			return None

		try:
			#打开给定的url
			response = urllib.request.urlopen(url)

			#如果返回状态不是200，则打开异常，返回空值
			if response.getcode() != 200:
				return None

			#如果正常打开，则返回读取到的html数据
			return response.read()

		#如果在打开url的过程中出现其他异常，则执行下面的代码
		except:
			#从当前需要打开的url中提取douban_id
			douban_id = re.search(r'(\d+)', url).group(0)
			
			#执行sql语句，在craw_list中将当前url对应的douban_id的状态标记为-1（爬取失败）
			self.cur.execute('UPDATE craw_list SET status = ? WHERE douban_id = ?', (-1, douban_id, ) )
			self.conn.commit()
			self.cur.close()
			
			print('Open url failed.')
			return None



