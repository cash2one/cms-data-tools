# -*- coding: utf-8 -*-
import scrapy
import time
from epg.function import parse_items, time12to24

class GemtvasiaThSpider(scrapy.Spider):
    name = "gemtvasia-th"
    allowed_domains = ["gemtvasia-th.com"]
    start_urls = (
        'http://www.gemtvasia-th.com/schedule/',
    )
    channelname = 'Gem TV Asia'
    issort = True

    def parse(self, response):
        date_position = response.xpath("//div[@id='flexslider-1']/ul")
        all_date = date_position.xpath(".//li/div[@class='day']/@data-date").extract()
        today = time.strftime("%Y/%m/%d")
        date = [d for d in all_date if d >= today]
        for d in date:
            url = 'http://www.gemtvasia-th.com/schedule/ajax/hk/data/listings/' + d
            yield scrapy.Request(url, callback=self.parse_epg)

    def parse_epg(self, response):
        items = parse_items(response)
        return items
