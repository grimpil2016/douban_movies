import url_manager, html_downloader, html_parser
#data_processor, html_outputer

class SpiderMain(object):
	def __init__(self):
		self.urls = url_manager.UrlManager()
		self.downloader = html_downloader.HtmlDownloader()
		self.parser = html_parser.HtmlParser()
		#self.processor = data_processor.DataProcessor()
		#self.outputer = html_outputer.HtmlOutputer()



	def craw(self, root_url):
		count = 1
		self.urls.add_new_url(root_url)
		while self.urls.has_new_url():
			'''
			try:
				new_url = self.urls.get_new_url()
				print('Craw {0} : {1}'.format(count, new_url))
				html_cont = self.downloader.download(new_url)
				new_urls, new_data = self.parser.parse(new_url, html_cont)
				self.urls.add_new_urls(new_urls)
				self.processor.add_new_data(new_data)

				if count == 10:
					break

				count += 1
			except:
				print('Craw failed.')
				'''
			new_url = self.urls.get_new_url()
			print('Craw {0} : {1}'.format(count, new_url))
			html_cont = self.downloader.download(new_url)
			new_urls, new_data = self.parser.parse(new_url, html_cont)
			self.urls.add_new_urls(new_urls)
			#self.processor.add_new_data(new_data)
			if count == 10:
				break
			count += 1





if __name__ == '__main__':
	root_url = 'https://movie.douban.com/subject/1292052/'
	obj_spider = SpiderMain()
	obj_spider.craw(root_url)