#!/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from db_access import DB_Access
from get_thumbnail import GetThumbnailThread
from datetime import datetime
import hashlib

import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import re
import base64
import sys


db = DB_Access()
img_root_path = "/var/www/tornado/watashiko/static/img"
img_root_url = "http://images.watashi.co"
global_text = ""
server = None
thumb = None
class MainHandler(tornado.web.RequestHandler):

  def get(self):
    self.render("index.html")

class NewContentHandler(tornado.web.RequestHandler):

  def get(self):
    self.render("new_content.html")

def args_to_dict(args):
  answer = {'id':'','tag':[]}
  work = re.split(',',args)
  i=0
  while(i<len(work)):
    if(work[i]=="num"):
      answer['num'] =int(base64.decodestring(work[i+1].encode("ascii")).decode("utf8"))
    if(work[i]=="id"):
      answer['id'] = base64.decodestring(work[i+1].encode("ascii")).decode("utf8")
    if(work[i]=="tag"):
      answer['tag'].append(base64.decodestring(work[i+1].encode("ascii")).decode("utf8"))
    i+=2
  print(answer)
  return(answer)
  
class APIHandler(tornado.web.RequestHandler):

  @tornado.web.asynchronous
  def get(self,*args, **kwargs):

    convert_data = args_to_dict(kwargs['args'])
    None_flag = False
    write_text = '{"item":['
    for i in db.get_list(ID = int(convert_data['id']),tag = convert_data['tag'],num = convert_data["num"]):
#      print(i)
      None_flag = True
      write_text += (str(i).replace("\'","\"")+",")
    write_text = write_text[:-1]#最後のカンマを除去
    write_text += ']}'
    if(None_flag):
      self.write(write_text)
    else:
      self.write("No_Data")
    self.finish()
    
  @tornado.web.asynchronous
  def post(self, *args, **kwargs):
#    global thumb
    data = {
      "main_comment":base64.decodestring(self.get_argument('main_comment').encode("ascii")).decode("utf-8"),
      "sub_comment":base64.decodestring(self.get_argument('sub_comment').encode("ascii")).decode("utf-8"),
      "url":base64.decodestring(self.get_argument('url').encode("ascii")).decode("utf-8"),
      "tag":re.split(',',base64.decodestring(self.get_argument('tag').encode("ascii")).decode("utf-8"))
           }
    
    data["main_comment"] = re.sub(r',|\\|<|>|\"|\'|[|]', '', data["main_comment"])
    data["sub_comment"] = re.sub(r',|\\|<|>|\"|\'|[|]', '', data["sub_comment"])
    data["url"] = re.sub(r',|\\|<|>|\"|\'|[|]', '', data["url"])
    target_path = img_root_path + "/" + datetime.now().strftime('%Y%m')
    print("target_path = " + target_path)
    file_name = hashlib.md5((datetime.now().strftime('%s') + str(db.get_max_ID()) + data["main_comment"]).encode('utf-8')).hexdigest() + ".jpg"
    if(not thumb.isAlive()):
      thumb.start()
    thumb.append_task(target_path,file_name,data["url"])
#    print(data["url"])
    data["path"] = img_root_url + "/" +datetime.now().strftime('%Y%m')+ "/" + file_name
    for tag in range(0,len(data["tag"])):
      data["tag"][tag] = re.sub(r',|\\|<|>|\?|\"|\'|[|]|\/', '', data["tag"][tag])

#    print(data)
    
    db.set_data(data)
    self.finish()
    
  @tornado.web.asynchronous
  def put(self, *args, **kwargs):
    ID = kwargs['args']
    action = self.get_argument('action', None)
    print(action)
    if(action == "shikoiine"):
      db.update_shikoiine(int(ID))
      
    if(action == "naerune"):
      db.update_naerune(int(ID))
      
    if(action == "guilty"):
      db.update_guilty(int(ID))
    
#    ans = ""
    write_text = '{"item":['
    for i in db.get_data(int(ID)):
      write_text += str(i)
    print(write_text)
    
    None_flag = False
    write_text = '{"item":['
    for i in db.get_data(int(ID)):
#      print(i)
      None_flag = True
      write_text += (str(i).replace("\'","\"")+",")
    write_text = write_text[:-1]#最後のカンマを除去
    write_text += ']}'
    print(write_text)
    self.write(write_text)
    self.finish()
    
#実行用関数
def serve_forever():
  global server
  global thumb
  thumb = GetThumbnailThread()
  thumb.start()
  application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/api/(?P<args>.+)", APIHandler),
    (r"/api", APIHandler),
    (r"/api/?(.*)", APIHandler),
    
    (r"/new_content", NewContentHandler),
      ],
    template_path=os.path.join(os.getcwd(),  "templates"),
    static_path=os.path.join(os.getcwd(),  "static"),
  )
  application.listen(8889)
  print=('サーバー起動')
  server = tornado.ioloop.IOLoop.instance()
  server.start()

if __name__ == "__main__":
  serve_forever()
