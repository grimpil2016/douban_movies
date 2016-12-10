# _*_ coding:utf-8 _*_

import sqlite3

#数据处理器，用于存储解析器获取到的电影数据
class DataProcessor(object):

	# 初始化程序
	def __init__(self):

		#创建连接打开sqlite数据库文件
		self.conn = sqlite3.connect('douban_movies.sqlite')
		self.cur = self.conn.cursor()

		#执行sql语句，如果数据库中没有表movies则创建，有则忽略
		self.cur.execute('''CREATE TABLE IF NOT EXISTS movies
			(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
			 douban_id TEXT NOT NULL UNIQUE,
			 title TEXT NOT NULL,
			 year TEXT,
			 director TEXT,
			 imdb TEXT,
			 rate TEXT)''')

	# 把新数据加入数据库中
	def add_new_data(self, new_data):
		#如果获取到的数据为空则返回
		if new_data is None:
			return

		#执行sql语句，检索表movies中是否已保存有对应电影的数据
		self.cur.execute('SELECT * from movies WHERE douban_id =?', (new_data['douban_id'], ) )
		row = self.cur.fetchone()

		#如果有，则返回
		if row is not None:
			print('Data exists, try next.')
			return

		#没有则继续
		else:
			#此处写入数据为关键部分，加入异常处理
			try:
				#执行sql，写入数据
				self.cur.execute('''INSERT OR IGNORE INTO movies
					(douban_id, title, year, director, imdb, rate) 
					VALUES ( ? , ? , ? , ? , ? , ? )''', 
					(new_data['douban_id'], new_data['title'], new_data['year'],
					 new_data['director'], new_data['imdb'], new_data['rate']) )

				#数据写入成功之后，把表craw_list对应的douban_id标记为1（已爬取）
				self.cur.execute('UPDATE craw_list SET status = ? WHERE douban_id = ?', (1, new_data['douban_id'], ) )
				self.conn.commit()
				print('==Add data successed.==')

			except:
				#数据写入失败，把表craw_list对应的douban_id标记为-2（数据写入失败）
				self.cur.execute('UPDATE craw_list SET status = ? WHERE douban_id = ?', (-1, new_data['douban_id'], ) )
				self.conn.commit()
				print('Store data failed.')
				return
		
