# -*- coding: utf-8 -*-
import scrapy
import time
from epg.items import EpgItem
from epg.function import next_day
from scrapy.exceptions import CloseSpider


class UniversalChannelAsiaSpider(scrapy.Spider):
    name = "universal-channel-asia"
    allowed_domains = ["universalchannel.asia"]
    start_urls = (
        'http://www.universalchannel.asia/schedule/day/today',
    )
    channelname = "Universal Channel Asia"
    formats = "%Y%m%d"
    issort = True

    def parse(self, response):
        day = time.strftime(self.formats)
        for i in range(30):
            url = "http://www.universalchannel.asia/schedule/day/" + day
            day = next_day(self.formats, day)
            yield scrapy.Request(url, callback=self.parse_epg)

    def parse_epg(self, response):
        section_div = response.xpath("//main[@id='skip']/div[@class='container ']/section[contains(@class, 'js-schedule')]")
        if len(section_div) == 0:
            raise CloseSpider('no epg info!')
        for section in section_div:
            content_div = section.xpath(".//div[@class='row']/article[@class='row']")
            for div in content_div:
                starttime_stamp = div.xpath(".//div[@class='item']/@data-timestamp").extract()[0].strip()
                starttime = time.strftime("%Y.%m.%d %H:%M:%S", time.localtime(float(starttime_stamp)))

                detail = div.xpath(".//div[@class='item']/div[@class='item__divide']/div[contains(@class,'tram-post')]/"
                                   "div[@class='row']/div[contains(@class, 'stack')]/div[@class='row']/div[contains(@class,'col-md-8')]")

                try:
                    title = detail.xpath(".//h3[@class='h2']/a/text()").extract()[0].strip()
                except IndexError:
                    title = detail.xpath(".//h3[@class='h2']/text()").extract()[0].strip()

                try:
                    meta = detail.xpath(".//h4[@class='h2-sub']/a/text()").extract()[0]
                    meta = meta.split(":")[0].strip()
                    name = "%s %s" % (title, meta)
                except IndexError:
                    name = title

                desc = detail.xpath(".//span[@class='type-delta']/p/text()").extract()[0]

                item = EpgItem()
                item['name'] = name
                item['desc'] = desc.strip()
                item['starttime'] = starttime
                item['endtime'] = ''
                yield item