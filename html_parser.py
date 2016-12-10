# _*_ coding:utf-8 _*_

from bs4 import BeautifulSoup
import urllib.parse
import re

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
		douban_id = re.search(r'(\d+)', page_url).group(0)
		#添加进res_data中
		res_data['douban_id'] = douban_id

		# 获取电影的标题和发行年份
		# 这里需要根据html内各元素的结构进行精确定位
		# 如果网页结构发生改变，需进行相应的调整，否则会获取失败，以下几项亦如是
		title_node = soup.find('div', id="content").find('h1').find_all('span')
		res_data['title'] = title_node[0].get_text()
		res_data['year'] = title_node[1].get_text()[1:-1]

		# 获取电影的导演
		info_node = soup.find('div', id="info")
		res_data['director'] = info_node.find('span').find_all('span')[1].find('a').get_text()

		#获取电影的imdb编号和评分
		#部分电影没有此两项或其中一项，需加入异常处理
		try:
			#获取imdb
			res_data['imdb'] = info_node.find('a', href=re.compile('^http://www.imdb.com/title/')).string
			
			#获取评分
			# <strong class="ll rating_num" property="v:average">7.8</strong>
			rate_node = soup.find('strong', class_="ll rating_num")
			res_data['rate'] = rate_node.get_text()

		except:
			#获取imdb和评分失败则返回字符串'None'
			res_data['imdb'] = 'None'
			res_data['rate'] = 'None'

		# 获取电影简介
		#summary_node = soup.find('span', property="v:summary")
		#res_data['summary'] = summary_node.get_text()

		#print(res_data)

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