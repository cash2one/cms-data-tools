# -*- coding: utf-8 -*-
import scrapy
import time
import re
from epg.items import EpgItem
from epg.function import next_day, time12to24, trans_format
import datetime
from scrapy.exceptions import CloseSpider


class Mbc3Spider(scrapy.Spider):
    name = "star_sports"
    allowed_domains = ["www.in.com"]
    start_urls = (
        'http://www.in.com/tv/channel/star-sports-3-103.html',
    )
    channelname = "STAR SPORTS 3"
    formats = "%Y%m%d"
    issort = True

    def parse(self, response):
        day = time.strftime(self.formats)
        for i in range(10):
            url = "http://www.in.com/ajax/getChannelSchedule.php?cid=103&dt=" + day
            day = next_day(self.formats, day)
            yield scrapy.Request(url, callback=self.parse_epg)

    def parse_epg(self, response):
        date_str = response.url[-8:]
        program_position = response.xpath("//div[@class='schedule_grid ']")
        reg = re.compile(r"\s\s+")
        for dates in program_position:
            program = dates.xpath("./div[@class='schedule_details']")
            program_time = program.xpath("./p[@class='info']/text()").extract()[0]
            title = program.xpath("./p[@class='title']/a/text()").extract()[0]
            try:
                subtitle = program.xpath("./p[@class='title']/a/span/text()").extract()[0]
            except IndexError:
                subtitle = ""
            except ValueError:
                subtitle = ""

            program_time = time12to24(reg.sub("", program_time).replace(" ",""))
            starttime = trans_format("%s %s" % (date_str, program_time), self.formats+" %H:%M")

            item = EpgItem()
            item['name'] = reg.sub("", title.strip() + subtitle.strip())
            item['starttime'] = starttime
            item['endtime'] = ''
            item['desc'] = ''
            yield item



