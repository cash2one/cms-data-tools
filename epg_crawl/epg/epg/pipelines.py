# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import xlwt

class EpgPipeline(object):
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):

        self.items.append(item)
        return item

    def close_spider(self, spider):
        print spider.channelname
        self.channelname = spider.channelname
        if spider.issort:
            self.items.sort(key=lambda x: x['starttime'])
            for i in range(len(self.items) - 1):
                self.items[i]["endtime"] = self.items[i + 1]["starttime"]
        self.output_excel(self.items)

    def output_excel(self, items):
        if len(items) == 0:
            return
        workbook = xlwt.Workbook(encoding="utf-8", style_compression=2)
        sheet = workbook.add_sheet("epg", cell_overwrite_ok=True)
        head = ["预告名称", "开始时间", "结束时间", "系统录制文件保存天数", "是否允许系统录制", "TVOD计费方式", "TVOD计费单位", " ", "是否允许个人录制", "个人录制计费方式",
                "个人计费单位", "个人录制价格", "预告简介"]
        for i in range(len(head)):
            sheet.write(0, i, head[i], self.set_style("head"))

        index = 1
        for item in items:
            sheet.write(index, 0, item["name"], self.set_style("body"))
            sheet.write(index, 1, item["starttime"], self.set_style("body"))
            sheet.write(index, 2, item["endtime"], self.set_style("body"))
            sheet.write(index, 3, "3", self.set_style("body"))
            sheet.write(index, 4, "1", self.set_style("body"))
            sheet.write(index, 5, "0", self.set_style("body"))
            sheet.write(index, 6, "1", self.set_style("body"))
            sheet.write(index, 7, "0", self.set_style("body"))
            sheet.write(index, 8, "0", self.set_style("body"))
            sheet.write(index, 9, "0", self.set_style("body"))
            sheet.write(index, 10, "0", self.set_style("body"))
            sheet.write(index, 11, "0", self.set_style("body"))
            sheet.write(index, 12, item["desc"], self.set_style("body"))
            index += 1
        workbook.save(self.channelname + ".xls")

    def set_style(self, t):
        style = xlwt.XFStyle()
        font = xlwt.Font()
        if t == "head":
            font.name = "Time New Roman"
            font.height = 220
            font.bold = True
            font.color_index = 4
        elif t == "body":
            font.name = "Time New Roman"
            font.height = 220
            font.bold = False
            font.color_index = 4
        style.font = font
        return style