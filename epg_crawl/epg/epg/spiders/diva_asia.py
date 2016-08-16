# -*- coding: utf-8 -*-
import scrapy
import time
import datetime
import re
from epg.items import EpgItem
from epg.function import next_day, trans_format
from scrapy.exceptions import CloseSpider



class DivaAsiaSpider(scrapy.Spider):
    name = "diva-asia"
    allowed_domains = ["divatv.asia"]
    start_urls = (
        'http://www.divatv.asia/schedule/',
    )
    channelname = "Diva Asia"
    formats = "%Y-%m-%d"
    issort = True

    def parse(self, response):

        day = time.strftime(self.formats)
        for i in range(30):
            url = "http://www.divatv.asia/schedule/" + day
            day = next_day(self.formats, day)
            yield scrapy.Request(url, callback=self.parse_epg)

    def parse_epg(self, response):


        content_div = response.xpath("//div[@class='schedule']/div[@class='outer-container']/"
                                     "div[@class='inner-container']/div[contains(@class,'schedule-row')]")
        if len(content_div) == 0:
            raise CloseSpider('no epg info!')
        day = response.url.split("/")[-1];
        nextday = next_day(self.formats, day)
        for div in content_div:
            starttime = div.xpath(".//div[contains(@class,'program-time')]/text()").extract()[0].strip()
            if starttime < "06:00":
                starttime = trans_format(nextday+starttime, self.formats+"%H:%M")
            else:
                starttime = trans_format(day+starttime, self.formats+"%H:%M")

            title = div.xpath(".//div[contains(@class,'program-info')]/h4").extract()[0].strip()
            reg = re.compile(r'\<h4.*?\>\s*(?:\<a href.*?\>)*(.*?)(?:\</a\>)*\s*\</h4\>', re.S)
            s = reg.search(title)
            title = s.group(1)
            meta = div.xpath(".//div[contains(@class,'program-info')]/p/text()").extract()[0]
            meta = meta.split(":")[0].strip()
            name = "%s %s" % (title, meta)

            desc = div.xpath(".//div[contains(@class,'program-info')]/div[contains(@class,'program-synopsis')]/p/text()").extract()[0]

            item = EpgItem()
            item['name'] = name
            item['desc'] = desc.strip()
            item['starttime'] = starttime
            item['endtime'] = ''
            yield item
