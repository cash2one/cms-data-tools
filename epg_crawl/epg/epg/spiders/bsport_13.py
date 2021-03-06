# -*- coding: utf-8 -*-
import scrapy
import time
from epg.items import EpgItem
from epg.function import next_day
from scrapy.exceptions import CloseSpider


class Bsport13Spider(scrapy.Spider):
    name = "bsport-13"
    #allowed_domains = ["http://tv-guide.bein.net"]
    start_urls = (
        'http://tv-guide.bein.net/views/epg?region=mena&lang=en#',
    )
    channelname = 'beIN Sport HD 13-FR'
    formats = "%Y%m%d"
    issort = False

    def parse(self, response):
        day = time.strftime(self.formats)
        for i in range(10):
            url = "https://api.beinsports-social.com/views/epg?date=%s&lang=en&region=mena&tzo=-480&isdst=false&list=1" % day
            day = next_day(self.formats, day)
            yield scrapy.Request(url, callback=self.parse_epg)


    def parse_epg(self, response):
        channel_list = response.xpath("//ul[@class='prog_list']/li")
        if len(channel_list) == 0:
            raise CloseSpider('no epg info!')
        findflag = 0
        for channel in channel_list:
            pic_name = channel.xpath("./div[contains(@class,'channel_visu')]/a/span/img[@class='channel_icn']/@src").extract()[0]
            if pic_name.find("13HD") > -1:
                findflag = 1
                break
        if findflag != 1:
            return
        programs = channel.xpath(".//div[contains(@class,'programmes_items')]/div[@class='progs_wrapper']/div[contains(@class,'prog_items_cover')]/div")
        for pro in programs:
            starttime = pro.xpath("@data-start-time").extract()[0].replace("-", ".")
            endtime = pro.xpath("@data-end-time").extract()[0].replace("-", ".")
            name = pro.xpath("./a/span[@class='top_infos']/span[@class='prog_infos']/span[@class='prog_title']/@title").extract()[0]

            item = EpgItem()
            item['name'] = name.strip()
            item['starttime'] = starttime
            item['endtime'] = endtime
            item['desc'] = ''
            yield item

