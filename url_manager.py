# -*- coding:utf-8 -*-

import sqlite3
import pymysql
import re

# url 管理器，用于管理待爬取和已爬取的url
#共包含一个初始化程序和四个方法
class UrlManager(object):

	# 初始化
	def __init__(self):
		#豆瓣电影url的格式为：https://movie.douban.com/subject/5327268/
		#为避免重复存储，只提取最后的数字串部分保存
		#同时将前面相同的部分保存在变量 root_url 中
		self.root_url = 'https://movie.douban.com/subject/'

		#创建连接打开sqlite数据库文件
		#self.conn = sqlite3.connect('douban_movies.sqlite')
		self.conn = pymysql.connect(host='localhost', user='root', password='r00t2oi6',db='douban_movies', port=3306, charset='utf8')
		self.cur = self.conn.cursor()

	#添加单条url到表craw_list中
	def add_new_url(self, url):
		if url is None:
			return

		#从url参数中提取数字串，可作为唯一id区别每一部电影
		douban_id = re.search(r'(\d{4,})', url).group(0)

		#从表craw_list中查询当前的douban_id
		self.cur.execute('SELECT douban_id FROM craw_list WHERE douban_id = %s', (douban_id, ) )
		row = self.cur.fetchone()
		
		#如果返回结果不为空，则说明表中已有此douban_id
		if row is not None:
			return

		#否则，就将此douban_id添加到表craw_list中，并标记状态为 0
		else:
			self.cur.execute('''INSERT IGNORE INTO craw_list (douban_id, status)
				VALUES ( %s, 0)''', (douban_id, ) )
			self.conn.commit()


	#从每个页面提取到的多个url，批量添加到表craw_list中
	def add_new_urls(self, urls):

		# 如果urls为空，则返回空值
		if urls is None or len(urls) == 0:
			return

		try:
			#urls是个list变量，用for读取每一个url
			for url in urls:
				#调用add_new_url()，将url加入表craw_list中
				self.add_new_url(url)
			print('== Add urls successfully. ==')
		except Exception as e:
			print('Add urls failed: ', e)

	# 查询表craw_list中是否还有未爬取的url
	# 返回true则为有，返回false则没有
	def has_new_url(self):
		
		#执行sql语句，检索状态为0（未爬取）的douban_id
		self.cur.execute('SELECT douban_id FROM craw_list WHERE status = 0')
		row = self.cur.fetchone()

		#检索结果不为空，则说明有，否则为没有	
		if row is not None:
			return True
		else: return False

	#提取一个未爬取的url
	def get_new_url(self):

		#执行sql语句，检索并返回一条未爬取的douban_id
		self.cur.execute('SELECT douban_id FROM craw_list WHERE status = 0 ORDER BY RAND() LIMIT 1')
		row = self.cur.fetchone()[0]
		#print(row)
		#如果检索结果不为空，则把获取的douban_id和root_url合并，组成真正的url
		if row is not None:
			new_url = self.root_url + str(row) +'/'
			return new_url
		else:
			print('Get uncrawed url failed.')
			return None

