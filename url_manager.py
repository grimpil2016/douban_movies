# coding:utf8
import sqlite3
import re

class UrlManager(object):

	def __init__(self):
		#self.new_urls = set()
		#self.old_urls = set()
		self.root_url = 'https://movie.douban.com/subject/'

		self.conn = sqlite3.connect('douban_movies.sqlite')
		self.cur = self.conn.cursor()

		
		self.cur.execute('''CREATE TABLE IF NOT EXISTS craw_list
			(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
			 douban_id TEXT NOT NULL UNIQUE, 
			 status INTEGER NOT NULL)''')

	def add_new_url(self, url):
		if url is None:
			return
		'''
		if url not in self.new_urls and url not in self.old_urls:
			self.new_urls.add(url)'''

		douban_id = re.search(r'(\d+)', url).group(0)

		self.cur.execute('SELECT douban_id FROM craw_list WHERE douban_id = ?', (douban_id, ) )
		row = self.cur.fetchone()
		#print('fetch the uncrawed row', row)
		if row is not None:
			return
		else:
			self.cur.execute('''INSERT OR IGNORE INTO craw_list (douban_id, status)
				VALUES ( ?, 0)''', (douban_id, ) )
			self.conn.commit()
			print('add new url successed.')

	def add_new_urls(self, urls):
		if urls is None or len(urls) == 0:
			return
		for url in urls:
			self.add_new_url(url)

	def has_new_url(self):
		#return len(self.new_urls) != 0

		self.cur.execute('SELECT douban_id FROM craw_list WHERE status == 0')
		row = self.cur.fetchone()
		#print(row)
		if row is not None:
			return True
		else: return False

	def get_new_url(self):
		'''
		new_url = self.new_urls.pop()
		self.old_urls.add(new_url)
		return new_url'''

		self.cur.execute('SELECT douban_id FROM craw_list WHERE status == 0 LIMIT 1')
		row = self.cur.fetchone()

		if row is not None:
			new_url = self.root_url + row[0] +'/'
			return new_url
		else:
			print('Got no uncrawed movie from the  craw list.')
			return

