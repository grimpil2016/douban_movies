# douban_movies
Craw some movie info from Douban Movie

这是一个Python新手的学习作业，参考网上一个百度百科爬虫的教程，本人把它改写成了一个豆瓣电影爬虫。

基本流程是这样的：由指定的电影页面开始（我选的是排名第一的《肖申克的救赎》），提取页面上电影相关的信息（目前只获取少量主要数据，稍后会进行改进，获取尽可能全面的数据），同时提取页面中指向其他电影页面的链接，然后把获取的链接和数据加入SQLite数据库。然后从待爬取的链接中取出一个，继续爬取数据。
