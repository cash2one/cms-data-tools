#! /usr/lib/env python
# -*- coding: utf-8 -*-

import MySQLdb
import time
from warnings import filterwarnings
filterwarnings('error', category = MySQLdb.Warning)

class DB:
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.cid = 0  #customer
        self.mid = 21    #硬件id
        
    def connect(self):
        try:
            self.conn = MySQLdb.connect(host = self.host,
                                        user = self.user,
                                        passwd = self.password,
                                        db = self.db,
                                        charset = 'utf8')
            self.cursor = self.conn.cursor()
        except MySQLdb.Error,e:
            print("Mysql error %d : %s" % (e.args[0], e.args[1]))
            
    def __del__(self):
        self.cursor.close()
        self.conn.close()
        
    def execute(self,sql):
        try:
            self.cursor.execute(sql);
            self.conn.commit();
        except MySQLdb.Error,e:
            print(sql)
            print("Mysql error %d : %s" % (e.args[0], e.args[1]))
            self.conn.rollback();
            return False
        except MySQLdb.Warning,w:
            print(sql);
            print("Warnings %s" % str(w))
        return True
            
    def get_where(self, table='', where='', select='*'):
        sql = "select " + select + " from " + table + " where 1=1 and " + where
        self.cursor.execute(sql)
        return self.cursor.fetchall();
    def get(self, table=''):
        sql = "select * from " + table
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def insert(self, table='', item={}):
        key = " ("
        value = "("
        for i in item:
            if item[i] or item[i] == 0:
                key += i + ","
                if isinstance(item[i],unicode):
                    value += '"' + item[i].replace('"','\'') + '",'
                elif isinstance(item[i],str):
                    value += '"' + item[i].replace('"','\'') + '",'
                else:
                    value += str(item[i]) + ','
        key = key[:-1] + ") "
        value = value[:-1] + ") "
        sql = "insert into " + table + key + " values" + value
        return self.execute(sql)
    
    def update(self,table,key,value,where = ''):
        sql = "update " + table + " set " + key + "=" + value + " " +where
        return self.execute(sql)
    
    def getIdentiryId(self):
        self.cursor.execute("select @@IDENTITY")
        return self.cursor.fetchone()[0]
    
    def getNow(self):
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

class oleDB:
    def __init__(self):
        self.db = DB("221.4.223.112", "cmsread", "mktech$2015", "gvod")
        self.db.connect()
        
    def get_categoryId(self):
        table = "iptv_customer_category_map"
        where = "cid=%d and mid=%d" % (self.db.cid, self.db.mid)
        category_id_array = self.db.get_where(table, where, "category_id")
        for category_id in category_id_array:
            programs = self.get_programs(category_id[0])
            
    def get_category(self):
        table = "iptv_customer_category_map"
        where = "cid=%d and mid=%d and type='%s'" % (self.db.cid, self.db.mid,"GVOD")
        return self.db.get_where(table, where, "category_id,category_name")
        
    def get_programs(self, category_id):
        table = "iptv_customer_prog"
        where = "cid=%d and mid=%d and multimedia_category=%d" % (self.db.cid, self.db.mid, category_id)
        return self.db.get_where(table,where,"multimedia_name,multimedia_url,issue_year,multimedia_thumbnail_url,multimedia_description,language,multimedia_duration,multimedia_area")

    def get_language(self,language):
        l = self.db.get_where("iptv_customer_support_language", "lang='%s'" % language, "language")
        if l:
            return l[0][0]
        return ""
    
    def get_region(self,region):
        r = self.db.get_where("iptv_customer_support_region","reg='%s'" % region, "region")
        if r:
            return r[0][0]
        return ""
    
    
    def get_series(self):
        return self.db.get_where("tv_series", "cid=0 and mid=21", "name, media_id, season, episodes, description, region,issue_year")
    
    def get_series_detail(self,media_id):
        return self.db.get_where("iptv_customer_prog", "media_id = '%s'" %media_id ,"multimedia_name,multimedia_url,issue_year,multimedia_thumbnail_url,multimedia_description,language,multimedia_duration,multimedia_area,episode")
class cmsDB:
    def __init__(self):
        self.db = DB("127.0.0.1", "root", "root", "cms")
        self.db.connect()
        self.ole = oleDB()
        self.cpspid = self.get_cpspid()
        
    def get_cpspid(self):
        if self.db.cid == 0:
            cpspid = self.db.get_where("cpsp", "code=1000000", "id")
        else:
            cpspid = self.db.get_where("cpsp", "code=%d" % self.db.cid, "id")
        return cpspid[0][0]
        
    def get_Mytube_Gvod(self):
        mytube_id = self.db.get_where("category","name='NG_list' and cpspid=%d and parentid=0" % self.cpspid, "id")[0][0]
        item = {}
        if not mytube_id:
            item["name"] = "NG_list"
            item["cpspid"] = self.cpspid
            item["parentid"] = 1
            item["type"] = 4
            self.db.insert("category",item)
            mytube_id = self.db.getIdentiryId()
            
        vod_id = self.db.get_where("category", "name='G-VOD' and parentid=%d" % mytube_id, "id")
        if not vod_id:
            item["name"] = "G-VOD"
            item["parentid"] = mytube_id
            self.db.insert("category", item)
            vod_id = self.db.getIdentiryId()
        else:
            vod_id = vod_id[0][0]
            
        return vod_id
        
    def add_category(self):
        vod_id = self.get_Mytube_Gvod()
        categorys = self.ole.get_category()
        if categorys:
            item = {}
            item["cpspid"] = self.cpspid
            item["type"] = 4
            item["sequence"] = 0
            for category in categorys:
                if category[1] == "Movie":
                    print("Begin adding category %s" % category[1])
                    #item["name"] = category[1]
                   # item["parentid"] = 105
                    #self.db.insert("category", item)
                    #category_id = self.db.getIdentiryId()
                    category_id = 117
                    self.add_program(category_id,category[0])
                elif category[1] == "Series":
                    print("Begin adding category %s" % category[1])
                    category_id = 118
                    self.add_series(category_id,category[0])
    
    def add_picture(self, programid, programtype, fileurl):
        item = {}
        item["name"] = fileurl[fileurl.rfind("/")+1:]
        item["newname"] = fileurl[fileurl.rfind("/")+1:]
        item["fileurl"] = fileurl
        item["programid"] = programid
        item["programtype"] = programtype
        item["type"] = 1
        self.db.insert("picture", item)
        item["type"] = 0
        self.db.insert("picture", item)
        
    def add_category_program(self, programid, categoryid, programtype):
        cp = {}
        cp["programid"] = programid
        cp["categoryid"] = categoryid
        cp["programtype"] = programtype
        self.db.insert("category_program",cp)
        
    def replace_url(self,url):
        return url.replace("xm","http")
    
    def add_program(self, category_id,ole_category_id):
        programs = self.ole.get_programs(ole_category_id)
        if programs:
            for program in programs:
                print("begin adding program %s in the category %d." % (program[0],ole_category_id))
                item = {}
                item["name"] = program[0]
                item["originalname"] = program[0]
                item["sortname"] = program[0]
                item["releaseyear"] = program[2]
                item["releasetime"] = self.db.getNow()
                item["description"] = program[4]
                item["viewpoint"] = program[4]
                item["language"] = self.ole.get_language(program[5])
                item["length"] = program[6]
                item["originalcountry"] = program[7]
                item["seriesflag"] = 0
                item["supporttype"] = 127
                item["status"] = 1
                item["releasestatus"] = 1
                item["cpspid"] = self.cpspid
                item["programtype"] = 0
                item["starlevel"] = 6
                item["contentprovider"] = "GVOD"
                self.db.insert("program", item)
                program_id = self.db.getIdentiryId()
                
                mcItem = {}
                mcItem["broadcasttype"] = 6
                mcItem["playurl"] = self.replace_url(program[1])
                mcItem["fileurl"] = self.replace_url(program[1])
                mcItem["programtype"] = 1
                mcItem["programid"] = program_id
                mcItem["source"] = "0:1:0"
                mcItem["name"] = program[0]
                mcItem["type"] = 1
                mcItem["status"] = 0
                self.db.insert("mediacontent",mcItem)
                
                self.add_picture(program_id, 1,program[3])
                self.add_category_program(program_id, category_id, 2)
    
    def add_series(self,category_id, ole_category_id):
        series = self.ole.get_series()
        for se in series:
            print "adding series %s" % se[0]
            item = {}
            item["name"] = se[0]
            item["description"] = se[4]
            item["releaseyear"] = se[6]
            item["originalcountry"] = se[5]
            item["releasestatus"] = 1
            item["status"] = 1
            item["cpspid"] = self.cpspid
            item["supporttype"] = 127
            item["seriessupporttype"] = 127
            item["starlevel"] = 3
            item["volumncount"] = se[3]
            
            self.db.insert("series", item)
            series_id = self.db.getIdentiryId()
            s = self.ole.get_series_detail(se[1])
            
            for sitcom in s:
                print "\tadd %s" % sitcom[0]
                ser = {}
                ser["supporttype"] = 127
                ser["status"] = 1
                ser["releasestatus"] =1
                ser["name"] = sitcom[0]
                ser["originalname"] = sitcom[0]
                ser["sortname"] = sitcom[0]
                ser["releaseyear"] = sitcom[2]
                ser["description"] =sitcom[4]
                ser["originalcountry"] = self.ole.get_region(sitcom[7])
                ser["seriesflag"] = 1
                ser["cpspid"] = self.cpspid
                ser["programtype"] = 0
                ser["starlevel"] = 6
                ser["length"] = sitcom[6]
                ser["contentprovider"] = "GVOD"
                self.db.insert("program", ser)
                program_id = self.db.getIdentiryId()
                
                mcItem = {}
                mcItem["broadcasttype"] = 6
                mcItem["playurl"] = self.replace_url(sitcom[1])
                mcItem["fileurl"] = self.replace_url(sitcom[1])
                mcItem["programtype"] = 1
                mcItem["programid"] = program_id
                mcItem["source"] = "0:1:0"
                mcItem["name"] = sitcom[0]
                mcItem["type"] = 1
                mcItem["status"] = 0
                self.db.insert("mediacontent",mcItem)
            
                self.add_picture(program_id, 0,sitcom[3])
                self.add_program_series(series_id, program_id,sitcom[8])
                if sitcom[8] == 0:
                    series_picture = sitcom[3]
            self.add_category_program(series_id, category_id, 1)
            self.add_picture(series_id, 0, series_picture)
        
    def add_program_series(self,seriesid,programid,sequence):
        ps = {}
        ps["sequence"] = sequence
        ps["seriesid"] = seriesid
        ps["programid"] = programid
        self.db.insert("program_series", ps)
        id = self.db.getIdentiryId()
        ps["cpcontentid"] = "'VOD%0.19d@SV'" % id
        self.db.update("program_series","cpcontentid",ps["cpcontentid"])
        
def main():
    print("Starting.......")
    cms = cmsDB()
    cms.add_category()
    print("Ending......")
    
    
if __name__=="__main__":
    main()