# -*- coding: utf-8 -*-
import scrapy
import time
import re
import datetime
from epg.items import EpgItem
from epg.function import parse_items

class AnimaxTaiwanSpider(scrapy.Spider):
    name = "animax-taiwan"
    allowed_domains = ["animax-taiwan.com"]
    start_urls = (
        'http://www.animax-taiwan.com/schedule/',
    )
    channelname = 'Animax Taiwan'
    issort = True

    def parse(self, response):
        date_position = response.xpath("//div[@id='flexslider-1']/ul")
        all_date = date_position.xpath(".//li/div[@class='day']/@data-date").extract()
        today = time.strftime("%Y/%m/%d")
        date = [d for d in all_date if d >= today]
        for d in date:
            url = 'http://www.animax-taiwan.com/schedule/ajax/tw/data/listings/' + d
            yield scrapy.Request(url, callback=self.parse_epg)

    def parse_epg(self, response):
        items = parse_items(response)
        return items

##根据返回的response，解析item
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

            desc = li.xpath("./div[@class='content']/div[@class='synopsis']/text()").extract()[0]

            timeStr = li.xpath("./div[@class='date-time']/time/text()").extract()[0]
            dateStr = li.xpath("./div[@class='date-time']/span/text()").extract()[0]
            reg = re.compile(r'(\d{1,2}).*?(\d{1,2}).*?')
            m = reg.search(dateStr)
            mm = m.group(1)
            d = m.group(2)

            times = "%s %s %s %s" % (time.strftime('%Y'), mm, d, timeStr)
            time_struct = time.strptime(times, "%Y %m %d %H:%M")
            ftime = time.strftime("%Y.%m.%d %H:%M:%S", time_struct)

            item = EpgItem()
            item['name'] = name
            item['starttime'] = ftime
            item['endtime'] = ''
            item['desc'] = desc.strip()
            items.append(item)

        except IndexError:
            print "Xpath parse error!",li
            continue
        # except ValueError:
        #     print "time values error!"
        #     continue
        except AttributeError:
            print "re parse error!"
            continue
        except Exception as e:
            print "extract error: ", e
            continue
    return items