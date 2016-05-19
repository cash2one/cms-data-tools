# -*- coding: utf-8 -*-
import scrapy
import time
import datetime
import re
import sys
from scrapy.selector import Selector

class ExampleSpider(scrapy.Spider):
    name = "epg"
    allowed_domains = ["animax-asia.com"]
    start_urls = (
        'http://www.animax-asia.com/schedule',
    )

    def parse(self, response):
        date_position =  response.xpath("//div[@id='flexslider-1']/ul")
        all_date = date_position.xpath(".//li/div[@class='day']/@data-date").extract()
        today = time.strftime("%Y/%m/%d")
        date = [d for d in all_date if d > today]
        for d in date:
            url = 'http://www.animax-asia.com/schedule/ajax/seasia/data/listings/' + d
            yield scrapy.Request(url, callback=self.parse_epg)

    def parse_epg(self, response):
        list_pos = response.xpath("//ul[@class='schedule-listings']/li")
        for li in list_pos:
            try:
                title = li.xpath("./div[@class='content']/h2[@class='title']").extract()[0]
                reg = re.compile(r'\<h2.*?\>\s*(?:\<a href.*?\>)*(.*?)(?:\</a\>)*\s*\</h2\>', re.S)
                s = reg.search(title)
                title = s.group(1)
                meta = li.xpath("./div[@class='content']/div[@class='meta']/text()").extract()[0]
                name = title + " " + meta

                desc = li.xpath("./div[@class='content']/div[@class='synopsis']/text()").extract()[0]

                timeStr = li.xpath("./div[@class='date-time']/time/text()").extract()[0]
                dateStr = li.xpath("./div[@class='date-time']/span/text()").extract()[0]
                times = "%s,%s,%s" % (time.strftime('%Y'), dateStr.strip(), timeStr.strip())
                print times
                time_struct = time.strptime(times, "%Y,%d %b, %a,%H.%M%p")
                ftime = time.strftime("%Y.%m.%d %H:%M:%S", time_struct)
                print ftime

            except IndexError:
                print "Xpath parse error!"
                continue
            except ValueError:
                print "time values error!"
                continue
            except AttributeError:
                print "re parse error!"
                continue
            # except Exception as e:
            #     print "extract error: ", e
            #     continue

    # 01:30pm -> 13:30
    def time12to24(self,timestr):
        time.strptime(timestr, "%H.%M%p")
        times = timestr[:-2]
        if timestr.find("am") > -1:
            if times >= '12:00':
                ftime = datetime.datetime.strftime("%H:%M", times)
                ftime = ftime - datetime.timedelta(hours=12)

        elif timestr.find("pm") > -1:
            if times < '12:00':
                ftime = datetime.datetime.strftime("%H:%M", times)
                ftime = ftime + datetime.timedelta(hours=12)
        else:
            raise ValueError
        times = ftime.strftime("%H:%M")
        return times



