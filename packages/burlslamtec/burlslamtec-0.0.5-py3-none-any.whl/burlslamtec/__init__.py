#!/usr/bin/env python
import os
import subprocess
import platform
import threading
import sys

class apollo():
    def __init__(self):
        self.__ip=""
        self.__path="sdk\\"
        self.__burl_path="burl"
        self.__file_path=__file__.replace("__init__.py","")
        #os.system("cd "+self.__path)
        if(str(platform.system())=="Windows"):
            self.platform="windows"
        else:
            self.platform="linux"
            self.__path="sdk/"
            self.__file_path=self.__file_path[self.__file_path.find(".local"):]

    def config_ip(self,ip):
        self.__ip=ip

    def terminal(self,command):
        _temp=("" if(platform.system()=="Windows") else "wine ")+self.__file_path+self.__path+command[0]
        command.pop(0)
        command.insert(0,_temp)
        ans=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
        _result=str(ans.communicate()[0]).strip()
        if _result=="time out":
            raise Exception("robot not connect")
        #os.system(command.join(" "))

    def goto(self,x,y):
        if self.__ip != "":
            _temp=[self.__burl_path,self.__ip,"move",str(x),str(y)]
            robot=threading.Thread(target=self.terminal(_temp))
            robot.start()

    def home(self):
        if self.__ip != "":
            _temp=[self.__burl_path,self.__ip,"home"]
            robot=threading.Thread(target=self.terminal(_temp))
            robot.start()

    def rotation(self,degree):
        if self.__ip != "":
            degree=str(10 if degree>10 else 0 if degree<0 else degree)
            _temp=[self.__burl_path,self.__ip,"rotation",degree]
            robot=threading.Thread(target=self.terminal(_temp))
            robot.start()

    def cancel(self):
        if self.__ip != "":
            _temp=[self.__burl_path,self.__ip,"cancel"]
            robot=threading.Thread(target=self.terminal(_temp))
            robot.start()
    #command get value data from robot
    def __getValue(self,command):
        if self.__ip != "":
            _temp=("" if(platform.system()=="Windows") else "wine ")+self.__file_path+self.__path+command[0]
            command.pop(0)
            command.insert(0,_temp)
            ans=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
            _result=str(ans.communicate()[0]).strip()
            if _result=="time out":
                raise Exception("robot not connect")
            return _result
        else:
            return None

    def sensor(self,number):
        command=[self.__burl_path,self.__ip,"sensor",str(number)]
        if number>6 or number<1:
            return "-1"
        return self.__getValue(command)

    def status(self):
        command=[self.__burl_path,self.__ip,"status"]
        return self.__getValue(command)

    def battery(self):
        command=[self.__burl_path,self.__ip,"battery"]
        return self.__getValue(command)
