# -*-coding:utf8-*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.common.keys import Keys
import time
import thread
import sys

def getipInfo(ip):
    browser = webdriver.Firefox() # Get local session of firefox
    browser.get("http://112.91.81.84:2000/main.do") # Load page
    elem = browser.find_element_by_id("search_search") # Find the query box
    elem.send_keys(ip + Keys.RETURN)
    print(time.time())
    browser.implicitly_wait(5)
    print(time.time())
    browser.find_element_by_id('tab_whois').click()
    ip = browser.find_element_by_tag_name("pre")
    print(ip.text)
    time.sleep(5) # Let the page load, will be added to the API
    browser.close()
	
def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    browser = webdriver.Firefox()
    browser.get("http://112.91.81.84:2000/main.do")
    elem = browser.find_element_by_id("userName")
    elem.send_keys("马文意".decode())
    elem = browser.find_element_by_id("userPassword")
    elem.send_keys("930513")
    browser.find_element_by_id("loginBtn").click()
    browser.implicitly_wait(5)
    #browser.find_element_by_xpath("//span[@mid='483f77b4-b479-4312-bb48-d7c9b7b90360']/a[@class='rdm-link-a']").click()
    #browser.find_element_by_xpath("//li[@mid='6bc02755-db7c-44e9-bf74-b9d5d0faaaaa']/div[@class='rdm-home-li-div']").click()
    browser.find_element_by_xpath("//div[@id='rdmHome']/img[@class='rdm-home']").click()
    browser.find_element_by_xpath("//span[@id='eb0e597a-5bbe-4489-8466-594d1babc867']").click()
    browser.switch_to_frame('main')
    browser.switch_to_frame('undefined_frame')
    time.sleep(1)
    tr= browser.find_element_by_xpath("//div[@id='bodyPanel']/table[1]/tbody/tr[1]/td/div")
    #ActionChains(browser).move_to_element(tr).perform()
    ActionChains(browser).context_click(tr).perform()
    manage = browser.find_element_by_xpath("//div[@id='manageMenu']/div[@class='text']")
    ActionChains(browser).move_to_element(manage).perform()
    browser.find_element_by_xpath('//div[@id="editMenu"]/div[@class="text"]').click()
    #browser.find_element_by_xpath("//div[@id='bodyPanel']/table[2]/tbody/tr/td[2]/a[@id='pagination_nextPage']").click()
    browser.switch_to_default_content()
    browser.switch_to_frame('main')
    browser.switch_to_frame('undefined_frame')
    browser.switch_to_frame('createFrame')
    browser.find_element_by_xpath("//li[@field='Fld_S_00005']/div[2]/div").click()
    lis = browser.find_element_by_xpath("//li[@field='Fld_S_00005']/div[2]/div/ul/li")
    for li  in lis:
        print li.text
    
    
    
    
    #browser.find_element_by_xpath("//a[@id='pagination_nextPage']").click()
    
    


if __name__ == "__main__":
    main()
