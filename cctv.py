
#coding=utf-8
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re

class Cctv:
	def __init__(self,homeUrl):
		self.homeUrl = homeUrl
		self.browser = webdriver.Firefox()
		self.epgInfo = []
	def __del__(self):
		self.browser.close()
		
	def getProgramInfo(self):
		self.browser.get(self.homeUrl)
		pageText = self.browser.page_source
		self.epgInfo.append(self.getEpgInfo(pageText))
	
	def getEpgInfo(self,html):
		soup = BeautifulSoup(html,'lxml')
		data = soup.find_all('div',class_='epg mt10 mb10')
		print data

def main():
	url = 'http://www.tvmao.com/program/CCTV-CCTV3-w3.html'
	cctv = Cctv(url)
	cctv.getProgramInfo()

if __name__ == "__main__":
	main()


