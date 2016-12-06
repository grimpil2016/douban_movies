# coding:utf8

from bs4 import BeautifulSoup
import urllib.parse
import re

class HtmlParser(object):

	def _get_new_urls(self, page_url, soup):
		new_urls = set()
		#<a  href="https://movie.douban.com/subject/26683290/?from=showing" class="">你的名字。</a>
		#<a class="item" target="_blank" href="https://movie.douban.com/subject/26329796/?tag=热门&amp;from=gaia">
		links = soup.find_all('a', href=re.compile(r'^https://movie.douban.com/subject/\d+/'))
		#print('links: ', links)
		#print(len(links))
		for link in links:
			url = link['href']
			new_url = re.match(r'^(https://movie.douban.com/subject/\d+/)', url).group(0)
			#print(new_url)
			new_urls.add(new_url)
		#print(new_urls)
		return new_urls


	def _get_new_data(self, page_url, soup):
		res_data = {}

		res_data['url'] = page_url

		# two ways used to get the id of the movie from the page url
		# https://movie.douban.com/subject/26683290/
		#douban_id = page_url.split('/')[-2]
		douban_id = re.match(r'^https://movie.douban.com/subject/(\d+)/', page_url).group(1)
		res_data['douban_id'] = douban_id

		# get the title and year
		title_node = soup.find('div', id="content").find('h1').find_all('span')
		res_data['title'] = title_node[0].get_text()
		res_data['year'] = title_node[1].get_text()[1:-1]

		# get the director and the imbd code

		info_node = soup.find('div', id="info")
		res_data['director'] = info_node.find('span').find_all('span')[1].find('a').get_text()
		res_data['imdb'] = info_node.find('a', href=re.compile('^http://www.imdb.com/title/')).string
		
		# get the rating number
		# <strong class="ll rating_num" property="v:average">7.8</strong>
		rate_node = soup.find('strong', class_="ll rating_num")
		res_data['rate'] = rate_node.get_text()

		# get the summary
		summary_node = soup.find('span', property="v:summary")
		#res_data['summary'] = summary_node.get_text()

		print(res_data)

		return res_data

	def parse(self, page_url, html_cont):
		if page_url is None or html_cont is None:
			return
		#print(html_cont)
		soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
		new_urls = self._get_new_urls(page_url, soup)
		new_data = self._get_new_data(page_url, soup)

		return new_urls, new_data