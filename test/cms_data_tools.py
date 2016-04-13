import myDb
import telnetlib
import os


class CmsDb:
    def __init__(self, host, user, passwd):
        self.cmsdb = myDb.DB(host, user, passwd, 'cms')
        self.cmsdb.connect()

    def update_url(self, oUrl, nUrl):
        sql = 'update mediacontent set playurl=replace(playurl,"%s","%s")' % (oUrl, nUrl)
        self.cmsdb.execute(sql)
        print 'update VOD url success!'

        sql = 'update physicalchannel set channelurl=replace(channelurl,"%s","%s")' % (oUrl, nUrl)
        self.cmsdb.execute(sql)
        print 'update IPTV url success!'


class Tools:
    def __init__(self):
        pass

    def change_cms_list_url(self, host, user, passwd):
        cms = CmsDb(host, user, passwd)
        print 'Database connect success!'
        oldUrl = raw_input('Input old url:')
        newUrl = raw_input('Input new url:')
        cms.update_url(oldUrl, newUrl);

    def flush_all(self):
        host = "104.243.42.10"
        username = "root"
        password = 'mocean@2016^'
        finish = "[zb@bogon ~]$ "

        tn = telnetlib.Telnet(host=host,port=12000)

        tn.set_debuglevel(2)

        tn.read_until("login: ")
        tn.write(username + '\n')
        tn.read_until("Password: ")
        tn.write(password + '\n')


        #tn.read_until(finish)
        tn.write("flush_all\n")

        tn.read_until("ok")
        tn.write("quit\n")

        tn.close()

    def deploy(self):
        path = raw_input("Input cms war path :")
        os.system("fab main:%s" % path)



def main():
    print "Providing following functions!"
    print "1 .change cms list url--"
#    print "2 .flush cache--"
    print "2 .auto deploy cms war--"

    n = raw_input("Input number the function you want:")

    tool = Tools()

    host = "104.243.42.10"
    user = "root"
    passwd = "mocean@2016^"

    if n == "1":
        tool.change_cms_list_url(host, user, passwd)
    elif n == "2":
        tool.deploy()



if __name__ == "__main__":
    main()
