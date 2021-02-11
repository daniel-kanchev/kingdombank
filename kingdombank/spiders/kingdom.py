import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from kingdombank.items import Article


class KingdomSpider(scrapy.Spider):
    name = 'kingdom'
    start_urls = ['https://www.kingdom.bank/news']

    def parse(self, response):
        links = response.xpath('//div[@role="listitem"]/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1[@class="heading"]/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//div[@class="h3"]/text()').get()
        if date:
            date = datetime.strptime(date.strip(), '%B %d, %Y')
            date = date.strftime('%Y/%m/%d')

        content = response.xpath('//div[@class="rich-text-block w-richtext"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
