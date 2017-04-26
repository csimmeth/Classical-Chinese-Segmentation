# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class RecipesSpider(scrapy.Spider):
	name = "guwen"
	start_urls = [
		"http://m.gushiwen.org/type.aspx?p=1",
	]

	def start_requests(self):
		for url in self.start_urls:
			yield scrapy.Request(url, callback=self.parse)


	def parse(self, response):
		links = response.css('a+ p a::attr(href)').extract()
		for link in links:
			content_page = response.urljoin("http://m.gushiwen.org/" + link)
			yield scrapy.Request(content_page, callback=self.parse_item)

		url = response.css('.pages span+ a::attr(href)').extract()[0]
		next_page = response.urljoin("http://m.gushiwen.org" + url)
		# print next_page
		yield scrapy.Request(next_page, callback=self.parse)


	def parse_item(self, response):
		strs = response.css('#cont::text').extract()
		content = ""
		for s in strs:
			content += s
		if len(content.split()) == 0:
			strs = response.css('#cont p::text').extract()
			content = ""
			for s in strs:
				content += s
		# if len(content.split()) == 0:
		# 	return

		content = "".join(content.replace('(', ')').split(')')[::2])
		yield {
			'title': response.css('h1::text').extract()[0],
			'guwen': "".join(content.split())
		}
			

