# coding:utf8

import sqlite3

class DataProcessor(object):

	def __init__(self):
		self.conn = sqlite3.connect('douban_movies.sqlite')
		self.cur = self.conn.cursor()

		self.cur.execute('''CREATE TABLE IF NOT EXISTS movies
			(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
			 douban_id TEXT NOT NULL UNIQUE,
			 title TEXT NOT NULL,
			 year TEXT,
			 director TEXT,
			 imdb TEXT,
			 rate TEXT)''')

	def add_new_data(self, new_data):
		if new_data is None:
			return

		self.cur.execute('SELECT * from movies WHERE douban_id =?', (new_data['douban_id'], ) )
		row = self.cur.fetchone()
		if row is not None:
			print('Movie exists, craw next.')
		else:
			try:
				self.cur.execute('''INSERT OR IGNORE INTO movies
					(douban_id, title, year, director, imdb, rate) 
					VALUES ( ? , ? , ? , ? , ? , ? )''', 
					(new_data['douban_id'], new_data['title'], new_data['year'],
					 new_data['director'], new_data['imdb'], new_data['rate']) )

				self.cur.execute('UPDATE craw_list SET status = ? WHERE douban_id = ?', (1, new_data['douban_id'], ) )
				self.conn.commit()
			except:
				self.cur.execute('UPDATE craw_list SET status = ? WHERE douban_id = ?', (-1, new_data['douban_id'], ) )
				self.conn.commit()
				print('Store data failed.')
		
