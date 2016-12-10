import url_manager, html_downloader, html_parser, data_processor
#, html_outputer

class SpiderMain(object):

	def __init__(self):
		self.urls = url_manager.UrlManager()
		self.downloader = html_downloader.HtmlDownloader()
		self.parser = html_parser.HtmlParser()
		self.processor = data_processor.DataProcessor()
		#self.outputer = html_outputer.HtmlOutputer()

	def craw(self, start_url):
		count = 1
		error = 0
		self.urls.add_new_url(start_url)
		while self.urls.has_new_url():

			try:
				new_url = self.urls.get_new_url()
				current_url = new_url
				print('\nCraw {0} : {1}'.format(count, new_url))
				
				html_cont = self.downloader.download(new_url)

				print('html cont is not None: ', html_cont is not None)

				new_urls, new_data = self.parser.parse(new_url, html_cont)

				print('new_urls is not None: ', new_urls is not None)
				print('new_data is not None: ', new_data is not None)
				self.urls.add_new_urls(new_urls)
				self.processor.add_new_data(new_data)

				if count == 20:
					break

				count += 1
			except:
				print('Craw failed.')
				
			'''
			new_url = self.urls.get_new_url()
			print('\nCraw {0} : {1}'.format(count, new_url))
			html_cont = self.downloader.download(new_url)
			new_urls, new_data = self.parser.parse(new_url, html_cont)
			self.urls.add_new_urls(new_urls)
			self.processor.add_new_data(new_data)

			if count == 5:
				break

			count += 1'''


if __name__ == '__main__':
	# start from the page of the most famous movie
	# 肖申克的救赎 The Shawshank Redemption
	start_url = 'https://movie.douban.com/subject/1292052/'
	obj_spider = SpiderMain()
	obj_spider.craw(start_url)