# -*-coding:utf8-*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.common.keys import Keys
import time
import thread
import sys
import codecs

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

    #browser.find_element_by_xpath("//span[@mid='483f77b4-b479-4312-bb48-d7c9b7b90360']/a[@class='rdm-link-a']").click()
    #browser.find_element_by_xpath("//li[@mid='6bc02755-db7c-44e9-bf74-b9d5d0faaaaa']/div[@class='rdm-home-li-div']").click()
    browser = webdriver.Firefox()
    browser.get("http://192.168.0.247:2000")
    elem = browser.find_element_by_id("userName")
    elem.send_keys("马文意".decode())
    elem = browser.find_element_by_id("userPassword")
    elem.send_keys("930513")
    browser.find_element_by_id("loginBtn").click()
    browser.implicitly_wait(5)
    browser.find_element_by_xpath("//div[@id='rdmHome']/img[@class='rdm-home']").click()
    browser.find_element_by_xpath("//span[@id='eb0e597a-5bbe-4489-8466-594d1babc867']").click()


    while True:
        time.sleep(3)
        for i in range(50):
            browser.switch_to.default_content()
            browser.switch_to.frame('main')
            browser.switch_to.frame('undefined_frame')
            try:
                tr = browser.find_element_by_xpath("//div[@id='bodyPanel']/table[1]/tbody/tr[%d]/td[2]/div" % (i+1))
    #ActionChains(browser).move_to_element(tr).perform()
                ActionChains(browser).context_click(tr).perform()
                manage = browser.find_element_by_xpath("//div[@id='manageMenu']/div[@class='text']")
            except Exception as e:
                print e
                error_log(tr.text)
                continue
            try:
                ActionChains(browser).move_to_element(manage).perform()
                browser.find_element_by_xpath('//div[@id="editMenu"]/div[@class="text"]').click()
            except ElementNotVisibleException:
                manage.click()
                browser.find_element_by_xpath('//div[@id="editMenu"]/div[@class="text"]').click()
            except Exception as e:
                print e
                error_log(tr.text)
                continue
    #browser.find_element_by_xpath("//div[@id='bodyPanel']/table[2]/tbody/tr/td[2]/a[@id='pagination_nextPage']").click()
            browser.switch_to.default_content()
            browser.switch_to.frame('main')
            browser.switch_to.frame('undefined_frame')
            browser.switch_to.frame('createFrame')

            pid = browser.find_element_by_xpath("//textarea[@id='Fld_T_00009']").text
            div = browser.find_element_by_xpath("//li[@field='Fld_S_00005']/div[2]/div")
            div.click()
            #div.click()
            title = browser.find_element_by_xpath("//li[@field='Fld_S_00005']/div[2]/div/span[1]")
            text = title.text
        #title.send_keys(text)

            if title:
                try:
                    print text
                    lis = browser.find_element_by_xpath("//li[@field='Fld_S_00005']/div[2]/div/ul/li[contains(text(),'%s')]" % text)
                    lis.click()
                    # lis = browser.find_elements_by_xpath("//li[@field='Fld_S_00005']/div[2]/div/ul/li")
                    # for li in lis:
                    #     print li.text
                    #
                    # exit()
                # except NoSuchElementException:
                #     print "No such Element"
                #     error_log("%s\t%s" % (pid, text))
                #     pass
                except ElementNotVisibleException:
                    print "error:" + text
                    error_log("%s\t%s" % (pid, text))

            browser.find_element_by_xpath('//div[@id="operateDiv"]/input[2]').click()

        try:
            browser.switch_to.default_content()
            browser.switch_to.frame('main')
            browser.switch_to.frame('undefined_frame')
            browser.find_element_by_xpath("//a[@id='pagination_nextPage']").click()
        except Exception as e:
            print e
            break

def error_log(strlog):
    f = codecs.open("rdm_error_log", 'a',encoding="utf-8")
    f.write(strlog + "\n")
    f.close()

if __name__ == "__main__":
    main()
