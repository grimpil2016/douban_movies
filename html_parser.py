# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import urllib.parse
import re
import time

# html解析器，用于解析下载器成功下载到的html页面数据
# 并提取出未爬取的url列表，和当前页面内电影的相关信息
class HtmlParser(object):

	#自有方法，用于提取未爬取的url
	def _get_new_urls(self, page_url, soup):

		#用于临时存储页面中提取到的未爬取的url
		new_urls = set()

		#页面中链接好几种不同的url格式，以下是最常见的两种
		#<a  href="https://movie.douban.com/subject/26683290/?from=showing" class="">你的名字。</a>
		#<a class="item" target="_blank" href="https://movie.douban.com/subject/26329796/?tag=热门&amp;from=gaia">
		
		#用正则表达式提取出所有指向电影页面的链接
		links = soup.find_all('a', href=re.compile(r'^https://movie.douban.com/subject/\d+/'))
		#print('links: ', links)
		#print(len(links))

		for link in links:

			#获取到链接中原始的url
			url = link['href']

			#匹配出‘https://movie.douban.com/subject/26683290/’这一部分
			new_url = re.match(r'^(https://movie.douban.com/subject/\d+/)', url).group(0)
			#print(new_url)

			#将获取到的url添加进new_urls
			new_urls.add(new_url)

		return new_urls

	#自有方法，用于提取当前html页面中对应电影的相关信息
	#目前只提取
	def _get_new_data(self, page_url, soup):
		
		#定义res_data这个dict变量，用于临时存储电影的信息
		res_data = {}

		#从url中提取当前电影对应douban_id
		douban_id = re.search(r'(\d{4,})', page_url).group(0)
		#添加进res_data中
		res_data['douban_id'] = int(douban_id)

		#获取电影标题和年份
		try:
			title_node = soup.find('div', id="content").find('h1').find_all('span')
			if len(title_node) == 1:
				res_data['title'] = title_node[0].get_text()
			if len(title_node) > 1:
				res_data['title'] = title_node[0].get_text()
				res_data['year'] = title_node[1].get_text()[1:-1]
			print('Title: ', res_data['title'])
		except:
			pass

		#获取海报图片的url
		try:
			img_node = soup.find('div', id='mainpic').find('img')
			res_data['img_url'] = img_node.get('src')
		except:
			pass

		#获取电影相关信息，豆瓣网页海报右侧部分
		info_nodes = str(soup.find('div', id='info')).split('<br/>')		
		for node in info_nodes:
			node = BeautifulSoup(node, "html.parser")
			#print(node.get_text())
			#print(node)
			
			#如果有‘导演’这一项，则提取导演信息
			if node.find('span', text='导演') is not None:
				director_links = node.find_all('a')
				#print('links: ', director_links)

				#有的电影不止一个导演，所以用list存储多位导演
				directors = []
				for link in director_links:
					director = {}
					if link.get('href').startswith('/search/'):
						director['celebrity_id'] = 0
					else:
						celebrity_id = re.search(r'(\d{4,})', link.get('href'))
						if celebrity_id is not None:
							director['celebrity_id'] = int(celebrity_id.group())
						else:
							director['celebrity_id'] = 0
					director['celebrity_name'] = link.get_text()
					directors.append(director)
				#print('directors: ', directors)
				res_data['directors'] = directors

			#如果有‘编剧’这一项，则提取编剧信息
			if node.find('span', text='编剧') is not None:
				writer_links = node.find_all('a')
				#print('links: ', writer_links)

				#有的电影不止一个编剧，所以用list存储多位编剧
				#每个编剧的信息用dict保存，包含
				writers = []
				for link in writer_links:
					writer = {}
					if link.get('href').startswith('/search/'):
						writer['celebrity_id'] = 0
					else:
						celebrity_id = re.search(r'(\d{4,})', link.get('href'))
						if celebrity_id is not None:
							writer['celebrity_id'] = int(celebrity_id.group())
						else:
							writer['celebrity_id'] = 0
					writer['celebrity_name'] = link.get_text()
					writers.append(writer)
				#print('writers: ', writers)
				res_data['writers'] = writers

			#如果有‘主演’这一项，则提取主演信息
			if node.find('span', text='主演') is not None:
				star_links = node.find_all('a')
				#print('links: ', star_links)

				#一部电影不止一个主演，所以用list存储多位主演
				#每个主演的信息用dict保存，包含
				stars = []
				for link in star_links:
					star = {}
					if link.get('href').startswith('/search/'):
						star['celebrity_id'] = 0
					else:
						celebrity_id = re.search(r'(\d{4,})', link.get('href'))
						if celebrity_id is not None:
							star['celebrity_id'] = int(celebrity_id.group())
						else:
							star['celebrity_id'] = 0
					star['celebrity_name'] = link.get_text()
					stars.append(star)
				#print('stars: ', stars)
				res_data['stars'] = stars

			#如果有‘类型’这一项，则提取类型信息
			if node.find('span', text='类型:') is not None:
				genres = []
				genre_nodes = node.find_all('span')[1:]
				for genre_node in genre_nodes:
					genres.append(genre_node.get_text())
				#print('genre: ', genres)
				res_data['genres'] = genres

			#如果有‘制片国家/地区：’这一项，则提取类型信息
			if node.find('span', text='制片国家/地区:') is not None:
				locations = node.get_text().split(':')[1].replace(' ', '').split('/')
				#print('location: ', location)
				res_data['locations'] = locations

			#如果有‘语言:’这一项，则提取语言信息
			if node.find('span', text='语言:') is not None:
				# node.contents = ['\n', <span class="pl">制片国家/地区:</span>, ' 德国']
				languages = node.get_text().split(':')[1].replace(' ', '').split('/')
				#print('language: ', language)
				res_data['languages'] = languages

			#如果有‘上映日期:’这一项，则提取上映日期信息
			if node.find('span', text='上映日期:') is not None:
				release_time = node.get_text().split(':')[1].replace(' ', '').split('/')
				#print('release time: ', release_time)
				res_data['release_time'] = release_time

			#如果有‘片长:’这一项，则提取片长信息
			if node.find('span', text='片长:') is not None:
				runtime = node.get_text()[5:].split('/')
				#print('runtime: ', runtime)
				res_data['runtime'] = runtime

			#如果有‘官方网站:’这一项，则提取网址信息
			if node.find('span', text='官方网站:') is not None:
				website = node.find('a').get_text()
				#print('website: ', website)
				res_data['website'] = website

			#如果有‘又名:’这一项，则提取名字信息
			if node.find('span', text='又名:') is not None:
				other_names = node.get_text()[5:].split('/')
				#print('other names: ', other_names)
				res_data['other_names'] = other_names

			#如果有‘IMDb链接:’这一项，则提取名字信息
			if node.find('span', text='IMDb链接:') is not None:
				imdb_id = node.find('a').get_text()
				#print('imdb id: ', imdb_id)
				res_data['imdb_id'] = imdb_id

		#获取电影评分
		# <strong class="ll rating_num" property="v:average">7.8</strong>
		try:
			rate_node = soup.find('strong', class_="ll rating_num")
			rate = rate_node.get_text()
			res_data['rate'] = float(rate)
		except:
			pass

		#获取评分人数
		#<a href="collections" class="rating_people"><span property="v:votes">243787</span>人评价</a>
		try:
			rate_num_node =soup.find('a', class_='rating_people').find('span')
			rate_num = rate_num_node.get_text()
			res_data['rate_num'] = int(rate_num)
		except:
			pass

		#获取评分中各个分数的百分比
		try:
			rate_per_nodes = soup.find('div', class_="rating_wrap clearbox").find_all('span', class_="rating_per")
			rate_percent = []
			for rate_per_node in rate_per_nodes:
				rate_percent.append(float(rate_per_node.get_text()[:-1]))
			res_data['rate_percent'] = rate_percent
		except:
			pass

		#获取看过的人数和想看的人数
		try:
			watch_node = soup.find('div', class_='subject-others-interests-ft').find_all('a')
			
			#已看人数
			watched_num = watch_node[0].get_text()[:-3]
			res_data['watched_num'] = int(watched_num)

			#想看人数
			to_watch_num = watch_node[1].get_text()[:-3]
			res_data['to_watch_num'] = int(to_watch_num)
		except:
			pass

		#获取豆瓣用户常用标签
		try:
			tag_nodes = soup.find('div', class_='tags-body').find_all('a')
			tags = []
			for tag_node in tag_nodes:
				tags.append(tag_node.get_text())
			res_data['tags'] = tags
		except:
			pass

		# 获取电影简介
		try:
			summary_node = soup.find('span', property="v:summary")
			summary = re.sub(' +', ' ', summary_node.get_text()).replace('\n', '').replace('\u3000', '')
			res_data['summary'] = summary
			#print(res_data['summary'])
		except:
			pass

		# 获取短评数量
		# <a href="https://movie.douban.com/subject/1304447/comments?status=P">全部 62431 条</a>
		try:
			comments_num = soup.find('div', id="comments-section").find('h2').find('a').get_text()[3:-2]
			#print('comments_num: ', comments_num)
			res_data['comments_num'] = int(comments_num)
		except:
			pass

		# 获取影评数量
		# <a href="https://movie.douban.com/subject/1304447/reviews">全部1051</a>
		try:
			reviews_num = soup.find('section', class_="reviews mod movie-content").find('h2').find('a').get_text()[2:-1]
			res_data['reviews_num'] = int(reviews_num)
		except:
			pass

		# 获取问题的数量
		# <a href="https://movie.douban.com/subject/1304447/questions/?from=subject">全部42个</a>
		try:
			questions_num = soup.find('div', id="askmatrix").find('h2').find('a').get_text().replace(' ' or '\n', '')[3:-2]
			res_data['questions_num'] = int(questions_num)
		except:
			pass

		return res_data

	# 解析程序，利用BeautifulSoup 和上面两个自有方法，
	# 提取需要的数据并存储在new_urls和new_data中
	def parse(self, page_url, html_cont):
		
		#print('parser got ', page_url, html_cont )
		if page_url is None or html_cont is None:
			return

		#用BeautifulSoup解析给定的html页面数据
		soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
		new_urls = self._get_new_urls(page_url, soup)
		new_data = self._get_new_data(page_url, soup)
		return new_urls, new_data