#!/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import re

global_text = ""
server = None

class MainHandler(tornado.web.RequestHandler):

  def get(self):
    print("aaa")
    self.write("welcome to watashiko")
    

def args_to_dict(args):
  answer = {'id':'','tag':[]}
  work = re.split(',|=',args)
  i=0
  while(i<len(work)):
    if(work[i]=="id"):
      answer['id'] = work[i+1]
    if(work[i]=="tag"):
      answer['tag'].append(work[i+1])
    i+=2
  print(answer)
  return(answer)


  
class APIHandler(tornado.web.RequestHandler):

  def get(self,*args, **kwargs):
#    print("args")
#    print(args)
#    print("kwargs")
#    print(kwargs['args'])
    args_to_dict(kwargs['args'])
#    id=123,tag=123,tag=aaaみたいな感じ
#    work = kwargs['args'].split(',|=')
#    print(key_val_list_to_dict(work))
    
    self.write("printed")
#    tagはバイトコードとかにして受け取らないとバグるのでjsで変換してから受け取る?
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
  )
  application.listen(8889)
  print('Server launch')
  server = tornado.ioloop.IOLoop.instance()
  server.start()

if __name__ == "__main__":
  serve_forever()
