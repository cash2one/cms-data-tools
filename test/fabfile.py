# encoding: utf-8

from fabric.api import *
from time import  *

env.roledefs = {'test': ["root@192.168.7.74"],
                'real': ["root@104.243.42.10:22"]}

#env.hosts = ["root@104.243.42.10:22"]
#env.password = "mocean@2016^"
env.password = "mktech2015"

def deploy():

    filePath = "C:\Users\Administrator\Desktop\cms\cms.war"

    if put(filePath, "/home/nobody/cms.war").failed:
        abort("file input failed!")

    run("rm -rf /home/nobody/backup.war")

    with cd("/opt/starview/boss/cms/tomcat/webapps"):
        run("cp cms.war /home/nobody/backup.war")
        with cd("../../bin"):
            run("./shutdown.sh")

        run("rm -rf cms*")
        run("mv /home/nobody/cms.war .")

        with cd("../../bin"):
            run("./startup.sh")

def uploadTemp(filePath):

    if put(filePath, "/opt/starview/CTMSData/upload/uploadImage/template").failed:
        abort("Template upload failed!")

@roles('test')
def test():

    env.shell = "/bin/bash -c"

    with cd("/opt/starview/boss/cms/tomcat/webapps"):

#        with cd("../../bin"):
#            run("ls")
#            with show('debug'):
#                run("./shutdown.sh")

        with cd("../../bin"):
            run("pwd")
            run("./startup.sh")
            run("ps aux | grep startup")





