# _*_ coding:utf-8 _*_

import url_manager, html_downloader, html_parser, data_processor
#, html_outputer

#爬虫主对象
class SpiderMain(object):

	#初始化程序，实例化各个对象
	def __init__(self):

		#创建url管理器
		self.urls = url_manager.UrlManager()

		#创建html下载器
		self.downloader = html_downloader.HtmlDownloader()

		#创建html解析器
		self.parser = html_parser.HtmlParser()

		#创建数据处理器
		self.processor = data_processor.DataProcessor()

		#创建html输出器
		#self.outputer = html_outputer.HtmlOutputer()

	#爬虫主程序
	def craw(self, start_url):

		#创建计数器
		count = 1

		#获取想要爬取电影的数量
		craw_num = int(input('Enter a number: '))

		# 添加启动页面到url列表中
		self.urls.add_new_url(start_url)

		#如果url列表中有未爬取的url，就循环执行以下代码
		while self.urls.has_new_url():

			try:
				#获取新的待爬取url
				new_url = self.urls.get_new_url()
				print('\nCraw {0}/{1}: {2}'.format(count, craw_num, new_url))
				
				#获取下载器返回的html页面数据
				html_cont = self.downloader.download(new_url)
				print('html cont is not None: ', html_cont is not None)

				#获取解析器返回的url和电影信息
				new_urls, new_data = self.parser.parse(new_url, html_cont)
				print('new_urls is not None: ', new_urls is not None)
				print('new_data is not None: ', new_data is not None)

				#将获取到的url和电影信息写入数据库
				self.urls.add_new_urls(new_urls)
				self.processor.add_new_data(new_data)

				#如果计数器达到指定的爬取数量，跳出循环，结束任务
				if count == craw_num:
					break
				count += 1

			#异常处理，有异常则输出'Craw failed.'，执行下一条
			except:
				print('Craw failed.')

if __name__ == '__main__':
	# 启动页面为目前排名第一的电影：肖申克的救赎 The Shawshank Redemption
	# 向经典致敬！
	start_url = 'https://movie.douban.com/subject/1292052/'
	obj_spider = SpiderMain()
	obj_spider.craw(start_url)