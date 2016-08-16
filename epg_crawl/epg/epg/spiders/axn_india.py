# -*- coding: utf-8 -*-
import scrapy
import time
import re
from epg.function import  time12to24
from epg.items import EpgItem

class AxnIndiaSpider(scrapy.Spider):
    name = "axn-india"
    allowed_domains = ["axn-india.com"]
    start_urls = (
        'http://www.axn-india.com/schedule/',
    )
    channelname = 'AXN India'
    issort = True

    def parse(self, response):
        date_position = response.xpath("//div[@id='flexslider-1']/ul")
        all_date = date_position.xpath(".//li/div[@class='day']/@data-date").extract()
        today = time.strftime("%Y/%m/%d")
        date = [d for d in all_date if d >= today]
        for d in date:
            url = 'http://www.axn-india.com/schedule/ajax/in/data/listings/' + d
            yield scrapy.Request(url, callback=self.parse_epg)

    def parse_epg(self, response):
        items = parse_items(response)
        return items

def parse_items(response):
    items = []
    list_pos = response.xpath("//ul[@class='schedule-listings']/li[@class='listing']")
    for li in list_pos:
        try:
            title = li.xpath("./div[@class='content']/h2[@class='title']").extract()[0]
            reg = re.compile(r'\<h2.*?\>\s*(?:\<a href.*?\>)*(.*?)(?:\</a\>)*\s*\</h2\>', re.S)
            s = reg.search(title)
            title = s.group(1)

            meta = li.xpath("./div[@class='content']/div[@class='meta']/text()").extract()[0]
            name = title + " " + meta
        except IndexError:
            print "Xpath parse name error!"
            name = title
        except AttributeError:
            print "re parse name error!"
            continue

        try:
            desc = li.xpath("./div[@class='content']/div[@class='synopsis']/text()").extract()[0]
        except IndexError:
            print "description is none!"
            desc = ""

        try:
            timeStr = li.xpath("./div[@class='date-time']/time/text()").extract()[0]
            dateStr = li.xpath("./div[@class='date-time']/span/text()").extract()[0]

            #将6.00am 这种格式转化为24小时制
            timeStr = time12to24(timeStr)

            times = "%s,%s,%s" % (time.strftime('%Y'), dateStr.strip(), timeStr)
            time_struct = time.strptime(times, "%Y,%A, %d %b,%H:%M")
            ftime = time.strftime("%Y.%m.%d %H:%M:%S", time_struct)
        except IndexError:
            print "Xpath parse time error!"
            continue
        except ValueError:
            print "time values error!"
            continue

        item = EpgItem()
        item['name'] = name
        item['starttime'] = ftime
        item['endtime'] = ''
        item['desc'] = desc.strip()
        items.append(item)


    return items
