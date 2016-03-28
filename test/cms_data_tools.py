import myDb


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


def main():
    print "Providing following functions!"
    print "1 .change cms list url--"

    n = raw_input("Input number the function you want:")

    tool = Tools()

    if n == "1":
        host = raw_input("Input server host:")
        user = raw_input("Input server user:")
        passwd = raw_input("Input server password:")
        tool.change_cms_list_url(host, user, passwd)


if __name__ == "__main__":
    main()
