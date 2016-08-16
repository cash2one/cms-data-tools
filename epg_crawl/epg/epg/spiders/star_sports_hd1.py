# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider, CrawlSpider
from scrapy.loader import ItemLoader
import time
import json
from epg.items import EpgItem
from epg.function import next_day, time12to24, trans_format
import datetime
from scrapy.exceptions import CloseSpider

class StarSportsHd1Spider(Spider):
    name = "star-sports-hd1"
    allowed_domains = ["tvguide.starsports.com"]
    start_urls = (
        'http://tvguide.starsports.com/',
    )
    channelname = "STAR SPORTS HD 1"
    formats = "%m%d%Y"
    issort = False

    def parse(self, response):
        day = time.strftime(self.formats)
        for i in range(10):
            url = "http://tvguide.starsports.com/data/%s.json" % day
            day = next_day(self.formats, day)
            yield scrapy.Request(url, callback=self.parse_epg)

    def parse_epg(self, response):
        json_str = json.loads(response.body)
        for channel in json_str:
            if channel['channelName'] == "si1a":
                programs = channel['channels']

        for program in programs:
            name = program['genre']
            starttime = program['date'] + program['start_time']
            endtime = program['date'] + program['end_time']

            starttime = trans_format(starttime, "%m/%d/%Y%H:%M:%S")
            endtime = trans_format(endtime, "%m/%d/%Y%H:%M:%S")

            item = EpgItem()
            item['name'] = name
            item['starttime'] = starttime
            item['endtime'] = endtime
            item['desc'] = ''
            yield item

