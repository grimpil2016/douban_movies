# -*- coding:utf-8 -*-

import pymysql
import time

class DataManager(object):

	def __init__(self):
		self.conn = pymysql.connect(host='localhost', user='root', password='r00t2oi6',db='douban_movies', port=3306, charset='utf8')
		self.cur = self.conn.cursor()

		self.data_default_values ={'douban_id':'', 'title':'', 'year':0, 'img_url':'', 
					'directors':'', 'writers':'', 'stars':'', 
					'genres':'', 'locations':'', 'languages':'', 
					'release_time':'', 'runtime':'', 'website':'', 
					'other_names':'', 'imdb_id':'', 'rate':-1, 
					'rate_num':-1, 'watched_num':-1, 'to_watch_num':-1, 
					'rate_percent':'', 'summary':'', 'comments_num':-1, 
					'reviews_num':-1, 'questions_num':-1, 'tags':''}

	def add_new_data(self, new_data):
		#如果获取到的数据为空则返回
		if new_data is None:
			return

		#执行sql语句，检索表movies中是否已保存有对应电影的数据
		self.cur.execute('SELECT * from movies WHERE douban_id =%s', (new_data['douban_id'], ) )
		row = self.cur.fetchone()

		#如果有，则返回
		if row is not None:
			self.cur.execute('UPDATE craw_list SET status = 1 WHERE douban_id = %s', (new_data['douban_id'], ) )
			print('Data exists, try next.')
			return

		for key, default_value in self.data_default_values.items():			
			if key not in new_data:
				new_data[key] = self.data_default_values[key]
		
		# 向表movies内写入信息
#		columns = ['douban_id', 'imdb_id', 'title', 'year', 'runtime', 'release_time', 'other_names', 'summary', 'watched_num', 'to_watch_num', 'comments_num', 'reviews_num', 'questions_num', 'img_url', 'website']
#		values = []
#		for column in columns:
#			values.append(new_data[column])
#
#		# make values, column and format be string format
#		values = ', '.join(values)
#		format = ', '.join(['%s'] * len(columns))
#		columns = ', '.join([u'douban_id', u'imdb_id', u'title', u'year', u'runtime', u'release_time', u'other_names', u'summary', u'watched_num', u'to_watch_num', u'comments_num', u'reviews_num', u'questions_num', u'img_url', u'website'])
#		print(columns, format, values)
#		query = "INSERT INTO movies (%s) VALUES (%s)" % (columns, format)
#		self.cur.execute(query, values)

		# 向表movies内写入信息
		self.cur.execute('''INSERT INTO movies
			(douban_id, imdb_id, title, year, runtime, release_time, other_names, summary, 
			watched_num, to_watch_num, comments_num, reviews_num, questions_num, img_url, website)
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
			(new_data['douban_id'], new_data['imdb_id'], new_data['title'], int(new_data['year']), str(new_data['runtime']), 
			str(new_data['release_time']), str(new_data['other_names']), new_data['summary'], new_data['watched_num'], 
			new_data['to_watch_num'], new_data['comments_num'], new_data['reviews_num'], new_data['questions_num'], 
			new_data['img_url'], new_data['website']) )


		# 提取导演的信息，格式为list
		# directors = [{'celebrity_id': 1036917, 'celebrity_name': '特瑞·乔治'}]
		directors = new_data['directors']
		if len(directors) != 0:
			for director in directors:
				# 向表directors内写入信息
				self.cur.execute('''INSERT IGNORE INTO directors (director_douban_id, director_name) 
					VALUES (%s, %s)''', (director['celebrity_id'], director['celebrity_name']) )
				
				#获取该导演在表directors中的id
				self.cur.execute('SELECT director_id FROM directors WHERE director_douban_id = %s and director_name = %s', (director['celebrity_id'], director['celebrity_name']) )
				director_id = self.cur.fetchone()[0]

				# 向表movie_director内写入信息
				self.cur.execute('''INSERT IGNORE INTO movie_director (douban_id, director_id) 
					VALUES (%s, %s )''', (new_data['douban_id'], director_id) )


		# 提取编剧的信息，格式为list
		# writers': [{'celebrity_id': 1294179, 'celebrity_name': '凯尔·皮尔森'}, {'celebrity_id': 1036917, 'celebrity_name': '特瑞·乔治'}]
		writers = new_data['writers']
		#print(writers)
		if len(writers) != 0:
			for writer in writers:
				# 向表writers内写入信息
				self.cur.execute('''INSERT IGNORE INTO writers (writer_douban_id, writer_name) 
					VALUES (%s, %s)''', (writer['celebrity_id'], writer['celebrity_name']) )
				
				#查询编剧在表writers中的的id
				self.cur.execute('SELECT writer_id FROM writers WHERE writer_douban_id = %s and writer_name = %s', (writer['celebrity_id'], writer['celebrity_name']) )
				star_id = self.cur.fetchone()[0]

				# 向表movie_writer内写入信息
				self.cur.execute('''INSERT IGNORE INTO movie_writer (douban_id, writer_id) 
					VALUES (%s, %s )''', (new_data['douban_id'], star_id) )
		self.conn.commit()

		# 获取演员信息，格式为list
		# stars = [{'celebrity_id': 1053573, 'celebrity_name': '唐·钱德尔'}, {'celebrity_id': 1013866, 'celebrity_name': '苏菲·奥康内多'}, {'celebrity_id': 1047979, 'celebrity_name': '杰昆·菲尼克斯'}, {'celebrity_id': 1006989, 'celebrity_name': '尼克·诺特'}, {'celebrity_id': 1109510, 'celebrity_name': '哈基姆·凯-卡西姆'}]
		stars = new_data['stars']
		if len(stars) != 0:
			for star in stars:
				# 向表stars内写入信息
				self.cur.execute('''INSERT IGNORE INTO stars (star_douban_id, star_name) 
					VALUES (%s, %s)''', (star['celebrity_id'], star['celebrity_name']) )
				
				#查询演员在表stars中的的id
				self.cur.execute('SELECT star_id FROM stars WHERE star_douban_id = %s and star_name = %s', (star['celebrity_id'], star['celebrity_name']) )
				star_id = self.cur.fetchone()[0]
				
				# 向表movie_star内写入信息
				self.cur.execute('''INSERT IGNORE INTO movie_star (douban_id, star_id) 
					VALUES (%s, %s )''', (new_data['douban_id'], star_id) )
		self.conn.commit()

		# 获取类型信息，格式为list
		# genres = ['剧情', '历史', '战争']
		genres = new_data['genres']
		if len(genres) != 0:
			for genre in genres:
				# 向表genres内写入信息
				self.cur.execute('''INSERT IGNORE INTO genres (genre) 
					VALUES ( %s )''', (genre, ) )
				
				#查询该类型在表genres中的id
				self.cur.execute('SELECT genre_id FROM genres WHERE genre = %s ', (genre, ))
				genre_id = self.cur.fetchone()[0]
				
				# 向表movie_genre内写入信息
				self.cur.execute('''INSERT IGNORE INTO movie_genre (douban_id, genre_id) 
					VALUES (%s, %s )''', (new_data['douban_id'], genre_id) )
		self.conn.commit()

		# 获取发行地区信息，格式为list
		# locations = ['英国', '南非', '意大利', '美国']
		locations = new_data['locations']
		if len(locations) != 0:
			for location in locations:
				# 向表locations内写入信息
				self.cur.execute('''INSERT IGNORE INTO locations (location) 
					VALUES ( %s )''', (location, ) )
				
				#查询该地区在表location中的id
				self.cur.execute('SELECT location_id FROM locations WHERE location = %s ', (location, ))
				location_id = self.cur.fetchone()[0]
				
				# 向表movie_location内写入信息
				self.cur.execute('''INSERT IGNORE INTO movie_location (douban_id, location_id) 
					VALUES (%s, %s )''', (new_data['douban_id'], location_id) )

		# 获取语言信息，格式为list
		# languages = ['英语', '法语']
		languages = new_data['languages']
		if len(languages) != 0:
			for language in languages:
				# 向表languages内写入信息
				self.cur.execute('''INSERT IGNORE INTO languages (language) 
					VALUES ( %s )''', (language, ) )
				
				#查询该语言在表language中的id
				self.cur.execute('SELECT language_id FROM languages WHERE language = %s ', (language, ))
				language_id = self.cur.fetchone()[0]
				
				# 向表movie_language内写入信息
				self.cur.execute('''INSERT IGNORE INTO movie_language (douban_id, language_id) 
					VALUES (%s, %s )''', (new_data['douban_id'], language_id) )

		# 获取标签信息，格式为list
		# tags = ['爱情', '美国', '温情', '女权', '喜剧', '生活']
		tags = new_data['tags']
		if len(tags) != 0:
			for tag in tags:
				# 向表tags内写入信息
				self.cur.execute('''INSERT IGNORE INTO tags (tag) 
					VALUES ( %s )''', (tag, ) )
				
				#查询该标签在表tags中的id
				self.cur.execute('SELECT tag_id FROM tags WHERE tag = %s ', (tag, ))
				tag_id = self.cur.fetchone()[0]
				
				# 向表movie_tag内写入信息
				self.cur.execute('''INSERT IGNORE INTO movie_tag (douban_id, tag_id) 
					VALUES (%s, %s )''', (new_data['douban_id'], tag_id) )


		# 向表rate内写入信息
		# rate_percent = [50.6, 40.6, 8.2, 0.4, 0.1]
		rate_percent = new_data['rate_percent']
		if len(rate_percent) == 0:
		 	rate_percent = [0, 0, 0, 0, 0]
		self.cur.execute('''INSERT INTO rate 
			(douban_id, rate, rate_num, rate_per_5stars, rate_per_4stars, rate_per_3stars, rate_per_2stars, rate_per_1star)
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', (new_data['douban_id'], new_data['rate'], new_data['rate_num'], rate_percent[0], rate_percent[1], rate_percent[2], rate_percent[3], rate_percent[4]) )

		# 数据添加成功，向表craw_list内标记当前douban_id的状态为1（爬取成功）
		craw_time = time.ctime()
		
		self.cur.execute('UPDATE craw_list SET status = %s, craw_time = %s WHERE douban_id = %s', (1, craw_time, new_data['douban_id']) )
		self.conn.commit()

		print('== Add data successfully. ==')



