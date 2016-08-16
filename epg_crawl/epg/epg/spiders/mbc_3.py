# -*- coding: utf-8 -*-
import scrapy
import time
from epg.items import EpgItem
from epg.function import next_day, time12to24, trans_format
import datetime
from scrapy.exceptions import CloseSpider


class Mbc3Spider(scrapy.Spider):
    name = "mbc-3"
    allowed_domains = ["http://mbc3.mbc.net"]
    start_urls = (
        'http://mbc3.mbc.net/grid_US_Sun.html',
    )
    channelname = "MBC 3"
    issort = True

    def parse(self, response):
        program_position = response.xpath("//div[@class='box-container-wrapper']/div[contains(@class,'date-program-wrapper')]")
        for dates in program_position:
            date = dates.xpath("./div[@class='box-inner-container-header']/h2/text()").extract()[0][-10:]
            date = trans_format(date, "%d-%m-%Y", "%Y.%m.%d")
            programs = dates.xpath("./div[@class='box-inner-container-wrapper']/div")
            for program in programs:
                name = program.xpath("./div[@class='title']/h2/text()").extract()[0]
                times = program.xpath("./div[@class='timing']/time/text()").extract()[0]
                times = times.split("/")[0][0:7].strip().replace(":", ".")
                times = time12to24(times)
                starttime = trans_format("%s %s" % (date, times), "%Y.%m.%d %H:%M")
                ftime = datetime.datetime.strptime(starttime, "%Y.%m.%d %H:%M:%S")
                ftime = ftime + datetime.timedelta(hours=8)
                starttime = ftime.strftime("%Y.%m.%d %H:%M:%S")

                item = EpgItem()
                item['name'] = name
                item['starttime'] = starttime
                item['endtime'] = ''
                item['desc'] = ''
                yield item



