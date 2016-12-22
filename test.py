# -*- coding:utf-8 -*-

import pymysql
import re


conn = pymysql.connect(host='localhost', user='root', password='r00t2oi6',db='douban_movies', port=3306, charset='utf8')
cur = conn.cursor()

#cur.execute('''INSERT INTO movies (douban_id, imdb_id, title, year, runtime, release_time, other_names, summary) 
#	VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', (344567, 'tt0395169', '卢旺达饭店 Hotel Rwanda', 2004, str(['121 分钟']), 
#			str(['2004-09-11']), str(['卢安达饭店(台)']), '影片来源于一个真实的故事。保罗•卢斯赛伯吉纳(唐•钱德尔 Don Cheadle 饰)在乱世中开了一家饭店') )

cur.execute('''INSERT INTO movies
			(douban_id, imdb_id, title, year, runtime, release_time, other_names, summary, 
			watched_num, to_watch_num, comments_num, reviews_num, questions_num, img_url, website)
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
			(33445566, 'tt0395169', '卢旺达饭店 Hotel Rwanda', '45', str(['121 分钟']), 
			str(['2004-09-11']), str(['卢安达饭店(台)']), '影片来源于一个真实的故事。保罗•卢斯赛伯吉纳(唐•钱德尔 Don Cheadle 饰)在乱世中开了一家饭店', 133355, 
			58742, 22059, 533, 6, 'https://img3.doubanio.com/view/movie_poster_cover/lpst/public/p2159368352.jpg', 'http://www.mgm.com/ua/hotelrwanda/main.html') )
conn.commit()

'''
new_data['douban_id'], new_data['imdb_id'], new_data['title'], new_data['year'], new_data['runtime'], 
			new_data['release_time'], new_data['other_names'], new_data['summary'], new_data['watched_num'], 
			new_data['to_watch_num'], new_data['comments_num'], new_data['reviews_num'], new_data['questions_num'], 
			new_data['img_url'], new_data['website'], 
'''


'''
conn = sqlite3.connect('test.sqlite')
cur = conn.cursor()
status = ''
cur.execute('INSERT OR IGNORE INTO craw_list (douban_id, status) VALUES ( 3333, ?)', ('', ) )
conn.commit()
'''