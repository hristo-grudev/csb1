import scrapy

from scrapy.loader import ItemLoader

from ..items import Csb1Item
from itemloaders.processors import TakeFirst


class Csb1Spider(scrapy.Spider):
	name = 'csb1'
	start_urls = ['https://www.csb1.com/about-csb/press-releases']

	def parse(self, response):
		post_links = response.xpath('//a[@data-link-type-id="page"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()

		item = ItemLoader(item=Csb1Item(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
