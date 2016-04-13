from bs4 import BeautifulSoup
import urllib2
import re

url = 'http://www.tvmao.com/movie/LmEnLSM='
desc = ''
header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
		'Host':'www.tvmao.com'}
request = urllib2.Request(url,headers = header)
html = urllib2.urlopen(request).read().decode("utf-8").encode("utf-8")
reg = re.compile(r'<div class="clear more_c".*?style="display: none;">.*?<p>(.*?)</p>',re.S)
r = reg.search(html)
if r:
	desc = r.group(1)
        print desc
else:     
    
	print "NO"
