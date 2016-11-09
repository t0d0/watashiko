#!/bin/env python
# -*- coding: utf-8 -*-
import urllib
from struct import *
#from datetime import datetime
import hashlib
import os
import threading
import time
NG_hash = ["72d8ecec1defbfc3acb50c67dea9eb88",]#後で変える。
#"4dd229433629e6ca32967e09a7027ff2"]



class GetThumbnailThread(threading.Thread):

  def __init__(self):
    super(GetThumbnailThread, self).__init__()
#    self.path = path
#    self.url = url
    self.task = []
  
  def run(self):
    while(1):

      if(len(self.task)>0):
        try:
          next_task = self.task.pop()
          os.system("mkdir " + next_task["path"])
          if(next_task["url"][-1:]=="/"):
            next_task["url"] = next_task["url"][:-1]
          print(next_task["url"] + next_task["name"])
          os.system("wget -O " + next_task["path"]+ "/" +next_task["name"] + " http://api.thumbalizr.com/?api_key=7qgx1dhQtqQJPiRjZYHGHARxKivN&quality=90&width=250&encoding=png&delay=8&mode=screen&bwidth=1280&bheight=1024&url=?" + next_task["url"])
          next_task["path"]+ "/" +next_task["name"]
#          if(check_NG(next_task["path"]+ "/" +next_task["name"])):
#            print("img_ok")
#            pass
#          else:
#            print("img_ng")
#            self.task.append(next_task)

        except:
          print("コマンド実行エラー")
          pass
        finally:
          if(self.check_NG(next_task["path"]+ "/" +next_task["name"])):
            print("img_ok")
            pass
          else:
            print("img_ng")
            self.task.append(next_task)

          
      time.sleep(10)
  
  def append_task(self,path,file_name,url):
    self.task.append({"path":path,"name":file_name,"url":url})
  
  def check_NG(self,path):
    print("img_checking...")
    bin_data = open(path,'rb')
    string = ""
    while(1) :
        b = bin_data.read(1)
        if b == "" :
            break
        try:
          string+=str(unpack('c',b))
        except:
          break
#    print(hashlib.md5(string.encode('utf-8')).hexdigest())
    for i in NG_hash:
      if(hashlib.md5(string.encode('utf-8')).hexdigest() == i):
        return False

    return True
#thumb = GetThumbnailThread()
#thumb.start()
##thumb = GetThumbnailThread()
#thumb.check_NG("/var/www/tornado/watashiko/static/img/201611/c47d4c0b8b8967f4b9fb5377717b826b.jpg")
