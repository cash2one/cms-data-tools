# -*- coding: utf-8 -*-
import scrapy
import time
from epg.function import parse_items

class AxnPhSpider(scrapy.Spider):
    name = "axn-ph"
    allowed_domains = ["axn-asia.com"]
    start_urls = (
        'http://www.axn-asia.com/schedule/ph',
    )
    channelname = 'AXN Philippines'
    issort = True

    def parse(self, response):
        date_position = response.xpath("//div[@id='flexslider-1']/ul")
        all_date = date_position.xpath(".//li/div[@class='day']/@data-date").extract()
        today = time.strftime("%Y/%m/%d")
        date = [d for d in all_date if d >= today]
        for d in date:
            url = 'http://www.axn-asia.com/schedule/ajax/ph/data/listings/' + d
            yield scrapy.Request(url, callback=self.parse_epg)

    def parse_epg(self, response):
        items = parse_items(response)
        return items
