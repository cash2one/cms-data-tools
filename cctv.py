
#coding:utf-8
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import NavigableString
import re
import time
import urllib
import urllib2
import datetime
import xlwt
#import chardet
import codecs

class Cctv:
	def __init__(self,homeUrl,name):
		self.homeUrl = homeUrl
		#profile = webdriver.FirefoxProfile()
		#profile.set_preference('network.proxy.type',1)
		#profile.set_preference('network.proxy.http','171.39.234.38')
		#profile.set_preference('network.proxy.http_port',80)
		#profile.update_preferences()
		self.browser = webdriver.Firefox()
		self.epgInfo = []
		self.baseurl = "http://www.tvmao.com"
		self.basename = name
		self.pageSource = []
		self.nextDay = datetime.date.today() + datetime.timedelta(days=1)
	def close(self):
		self.browser.close()
		
	def get_program_info(self):
		
		self.browser.get(self.homeUrl)
		self.get_page_source()
		for ps in self.pageSource:
			pl = self.get_epg_info(ps)
			if len(pl) > 0:
				self.epgInfo.append(pl)       #all epg
		if len(self.epgInfo) == 0:
			return
		for i in range(len(self.epgInfo)-1):
			epg = self.epgInfo[i]
			self.epgInfo[i][len(epg)-1]["endtime"] = self.epgInfo[i+1][0]["starttime"]

	def get_page_source(self):
		reg = re.compile(r'\((.*?)\)')
		while True:
			fresh = False
			try:
				elements = self.browser.find_elements_by_xpath("//div[@class='epghdc lt']/dl/dd")
			except Exception as e:
				print e
				break
			for e in elements:
				d = reg.search(e.text)
				if d:
					if d.group(1) == str(self.nextDay)[5:]:
						self.nextDay = self.nextDay + datetime.timedelta(days=1)
						e.click()
						fresh = True
						self.browser.implicitly_wait(5)
						break
					else:
						continue
				if e.text.encode("utf-8") == "下周":
					self.nextDay = self.nextDay + datetime.timedelta(days=1)
					e.click()
					fresh = True
					self.browser.implicitly_wait(5)
					break
				#if e.text.encode("utf-8") == "本周":
				#	e.click()
				#	fresh = True
				#	self.browser.implicitly_wait(5)
				#	break;
			if fresh == False:
				break
			self.pageSource.append(self.browser.page_source)

	def get_epg_info(self,html):
		programList = []              #one day epg
		soup = BeautifulSoup(html,'lxml')
		date = self.get_date(soup)
		for li in soup.find('ul', id='pgrow').children:
			if isinstance(li,NavigableString):
				continue
			program = {}
			time = ''
			programName = ''
			desc = ''
			s = 0        #only the first link as program name

			if li.a:
				url = self.baseurl + li.a["href"]
				if li.div:
					try:
						for d in li.div.p.children:
							if d.name != "a":
								desc += d.string
					except:
						desc = ''
				else:
					desc = self.get_description(url)
			for info in li.children:
				if isinstance(info,NavigableString):
					programName = programName + info.string
				elif info.name == "span":
					time = info.string
					time = date + " " + time.strip()+":00"
				elif info.name == "a" and s == 0:
					programName = programName + info.string
					s = 1
				elif info.name == None:
					programName = programName + info.string
			if time == '':
				continue
			program["name"] = programName.strip()
			program["starttime"] =time 
			program["desc"] = desc
			programList.append(program)

		if len(programList) == 0:
			return []
		for i in range(len(programList)-1):
			programList[i]["endtime"] = programList[i+1]["starttime"]
		programList[len(programList)-1]["endtime"] = ''
		return programList
	
	def get_description(self,url):
		desc = ''
		header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
				'Host':'www.tvmao.com'}
		request = urllib2.Request(url,headers = header)
		html = urllib2.urlopen(request).read().decode("utf-8")
		reg = re.compile(r'<div class="clear more_c".*?<p>(.*?)</p>',re.S)
		r = reg.search(html)
		if r:
			desc = r.group(1)
		return desc

	def get_date(self,soup):
		dateInfo = soup.find('div',class_="mt10 clear").contents
		if len(dateInfo) > 0:
			date = str(dateInfo[0])[3:8]
			date = "2016-" + date
			date = date.replace("-",".")
		else:
			date = ''
		return date

	def output_excel(self):
		if len(self.epgInfo) == 0:
			return
		workbook = xlwt.Workbook(encoding="utf-8",style_compression=2)
		sheet = workbook.add_sheet("epg",cell_overwrite_ok=True)
		head = ["预告名称","开始时间","结束时间","系统录制文件保存天数","是否允许系统录制","TVOD计费方式","TVOD计费单位"," ","是否允许个人录制","个人录制计费方式","个人计费单位","个人录制价格","预告简介"]
		for i in range(len(head)):
			sheet.write(0,i,head[i],self.set_style("head"))

		index = 1
		for epg in self.epgInfo:
			for program in epg:
				sheet.write(index,0,program["name"],self.set_style("body"))
				sheet.write(index,1,program["starttime"],self.set_style("body"))
				sheet.write(index,2,program["endtime"],self.set_style("body"))
				sheet.write(index,3,"3",self.set_style("body"))
				sheet.write(index,4,"1",self.set_style("body"))
				sheet.write(index,5,"0",self.set_style("body"))
				sheet.write(index,6,"1",self.set_style("body"))
				sheet.write(index,7,"0",self.set_style("body"))
				sheet.write(index,8,"0",self.set_style("body"))
				sheet.write(index,9,"0",self.set_style("body"))
				sheet.write(index,10,"0",self.set_style("body"))
				sheet.write(index,11,"0",self.set_style("body"))
				sheet.write(index,12,program["desc"],self.set_style("body"))
				index += 1

		workbook.save(self.basename + ".xls")


	def set_style(self,t):
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


def main():
	urlList = ['http://www.tvmao.com/program_satellite/BTV1-w4.html','http://www.tvmao.com/program_satellite/HUNANTV1-w5.html',
			'http://www.tvmao.com/program/CHC-CHC1-w3.html','http://www.tvmao.com/program/CCTV-CCTV8-w3.html',
			'http://www.tvmao.com/program_satellite/DONGFANG1-w5.html','http://www.tvmao.com/program/GDTV',
	        	'http://www.tvmao.com/program/SZTV','http://www.tvmao.com/program/CHC-CHC2-w3.html',
			'http://www.tvmao.com/program/CHC-CHC3-w3.html','http://www.tvmao.com/program/CCTV-CCTV3-w3.html',
			'http://www.tvmao.com/program/CCTV-CCTV5-w3.html','http://www.tvmao.com/program/CCTV-CCTV6-w3.html',
			'http://www.tvmao.com/program_satellite/ZJTV1-w5.html','http://www.tvmao.com/program/PHOENIX/PHOENIX1',
			'http://www.tvmao.com/program/PHOENIX/PHOENIX1','http://www.tvmao.com/program/PHOENIX/PHOENIXHK',
			'http://www.tvmao.com/program/PHOENIX/PHOENIX-INFONEWS','http://www.tvmao.com/program/PHOENIX/PHOENIX-INFONEWS']
	nameList = ['Beijing','Hunan','CHC Action','CCTV 8','Dongfang','Guangdong','Shenzhen','CHC Family','CHC HD','CCTV 3','CCTV 5','CCTV 6','Zhejiang',
			'PHX Chinese HD','PHX Chinese','PHX HK HD','PHX Infonews HD','PHX Infonews']
#	urlList = ['http://www.tvmao.com/program/CCTV-CCTV6-w3.html']
#	nameList = ['CCTV 6']
	for i in range(len(urlList)):
		url = urlList[i]
		name = nameList[i]
		cctv3 = Cctv(url,name)
		print "Starting parse %s ......" % url
		cctv3.get_program_info()
		cctv3.close()
		print "Starting write to excel ......"
		cctv3.output_excel()
		print "parsing EPG OK!"
if __name__ == "__main__":
	main()


