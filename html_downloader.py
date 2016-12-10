# coding:utf8

from urllib import request
import urllib
import re
import sqlite3

class HtmlDownloader(object):

	def __init__(self):
		self.conn = sqlite3.connect('douban_movies.sqlite')
		self.cur = self.conn.cursor()

	def download(self, url):
		if url is None:
			return None
			
		'''			
		response = urllib.request.urlopen(url)

		if response.getcode() != 200:
			douban_id = re.search(r'(\d+)', url).group(0)
			
			self.cur.execute('UPDATE craw_list SET status = ? WHERE douban_id = ?', (-1, douban_id, ) )
			self.conn.commit()
			self.cur.close()
			
			print('Open url failed.')

			return None

		return response.read()'''

		try:
			response = urllib.request.urlopen(url)
			if response.getcode() != 200:
				return None
			return response.read()

		except:
			douban_id = re.search(r'(\d+)', url).group(0)
			
			self.cur.execute('UPDATE craw_list SET status = ? WHERE douban_id = ?', (-1, douban_id, ) )
			self.conn.commit()
			self.cur.close()
			
			print('Open url failed.')
			return None



