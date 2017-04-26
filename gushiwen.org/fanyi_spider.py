# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class RecipesSpider(scrapy.Spider):
	name = "fanyi"
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
		if len(response.css('.son5 a+ a::attr(href)').extract()) >= 2:
			url = response.css('.son5 a:nth-child(1)::attr(href)').extract()[0]
			fanyi_page = response.urljoin("http://m.gushiwen.org" + url)
			yield scrapy.Request(fanyi_page, callback=self.parse_item)
		else:
			strs = response.css('.shangxicont p:nth-child(2)::text').extract()
			content = ""
			for s in strs:
				content += s
			if len(content.split()) == 0:
				return
			content = "".join(content.replace('(', ')').split(')')[::2])
			yield {
				'title': response.css('a+ p a::text').extract()[0],
				'fanyi': "".join(content.split())
			}
			

