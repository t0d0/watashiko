#!/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import re
from db_access import DB_Access
import base64

db = DB_Access()

global_text = ""
server = None


class MainHandler(tornado.web.RequestHandler):

  def get(self):
    self.render("index.html")

def args_to_dict(args):
  answer = {'id':'','tag':[]}
  work = re.split(',',args)
  i=0
  while(i<len(work)):
    if(work[i]=="id"):
      answer['id'] = base64.decodestring(work[i+1].encode("ascii")).decode("utf8")
    if(work[i]=="tag"):
      answer['tag'].append(base64.decodestring(work[i+1].encode("ascii")).decode("utf8"))
    i+=2
#  print(answer)
  return(answer)


  
class APIHandler(tornado.web.RequestHandler):

  def get(self,*args, **kwargs):

    convert_data = args_to_dict(kwargs['args'])
#    print(convert_data['id'])
    write_text = '{"item":['
    for i in db.get_list(ID = int(convert_data['id']),tag = convert_data['tag']):
      print(i)
      write_text += (str(i).replace("\'","\"")+",")
    write_text = write_text[:-1]
    write_text += ']}'
    self.write(write_text)
  def post(self):
    self.get_argument('main_comment')
    self.get_argument('sub_comment')
    self.get_argument('url')
    self.get_argument('tag')#→カンマ区切りなので分割する
    self.get_argument('time_stamp')

#実行用関数
def serve_forever():
  global server
  application = tornado.web.Application([
    (r"/", MainHandler),
      (r"/api/(?P<args>.+)", APIHandler)
      ],
    template_path=os.path.join(os.getcwd(),  "templates"),
    static_path=os.path.join(os.getcwd(),  "static"),
    
  )
  application.listen(8889)
  print('Server launch')
  server = tornado.ioloop.IOLoop.instance()
  server.start()

if __name__ == "__main__":
  serve_forever()
