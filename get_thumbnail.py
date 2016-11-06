#!/bin/env python
# -*- coding: utf-8 -*-
import urllib
#from datetime import datetime
import hashlib
import os
import threading


class GetThumbnailThread(threading.Thread):

  def __init__(self):
    super(GetThumbnailThread, self).__init__()
#    self.path = path
#    self.url = url
    self.task = []
  
  def run(self):
    while(1):
      if(len(self.task)>=0):
        try:
          next_task = self.task.pop()
          os.system("mkdir " + next_task["path"])
          os.system("wget -O " + next_task["path"]+ "/" +next_task["name"] + " http://capture.heartrails.com/huge?" + next_task["url"])
        except:
          pass
  
  def append_task(self,path,file_name,url):
    self.task.append({"path":path,"name":file_name,"url":url})

#if __name__ == '__main__':
#    thumb = GetThumbnailThread()
#    thumb.start()
#    thumb.append_task("/var/www/tornado/test1.jpg","http://google.com")
#    thumb.append_task("/var/www/tornado/test2.jpg","http://google.com")
#    thumb.append_task("/var/www/tornado/test3.jpg","http://takumus.com")