#!/bin/env python
# -*- coding: utf-8 -*-
from browser import window, alert,document
from browser import document as doc
from browser import ajax
#locat = window.location
json = window.JSON
jq = window.jQuery
b64 = window.Base64
req_num = 10
last_id = -1
content_index = 0
selected_tag = ["-1"]
api_address = "http://t0d0.jp:8889/api/"
now_hash = ""
def get_complete(req):
  global last_id
  global content_index
  global lacat
  if(req.text=="No_Data"):
    print("これ以上読み込めません")
  else:
    data = json.parse(str(req.text))
#    print(str(req.text))
#    print(len(data['item']))
    for i in range(0,len(data['item'])):
      add_html = "<li name = '"+str(data['item'][i].ID)+"' id = '"+ str(data['item'][i].ID) +"'>"
      add_html += "<h2>" + data['item'][i].main_comment + "</h2>"
      add_html += "<p>" + data['item'][i].url + "</p>"
      add_html += "<p>" + data['item'][i].sub_comment + "</p>"
      add_html += "<p class = 'shikoiine' id = '"+str(data['item'][i].ID)+"'>shikoiine:" + str(data['item'][i].shikoiine) + "</p>"
      add_html += "<p class = 'naerune' id = '"+str(data['item'][i].ID)+"'>naerune:" + str(data['item'][i].naerune) + "</p>"
      add_html += "<p class = 'guilty' id = '"+str(data['item'][i].ID)+"'>guilty:" + str(data['item'][i].guilty) + "</p>"
      add_html += "<p>ID:" + str(data['item'][i].ID) + "</p>"
      last_id = data['item'][i].ID
      for tag_index in range(0,len(data['item'][i].tag)):
        add_html += "<p class='tag'>" + data['item'][i].tag[tag_index] + "</p>"
      add_html += "</li>"
      doc["contents_list"].html += add_html
      jq(".shikoiine").on("click",shikoiine_click)
      jq(".naerune").on("click",naerune_click)
      jq(".guilty").on("click",guilty_click)
      jq(".tag").on("click",tag_select)
      content_index += 1
      
    pass
def shikoiine_click(ev):
  global now_hash
  now_hash = ev.target.id
  put(api_address + ev.target.id,{"action":"shikoiine"})
def naerune_click(ev):
  global now_hash
  now_hash = ev.target.id
  put(api_address + ev.target.id,{"action":"naerune"})
def guilty_click(ev):
  global now_hash
  now_hash = ev.target.id
  put(api_address + ev.target.id,{"action":"guilty"})
  
def post_complete(req):
#  print(req.text)
  doc.getElementById("close").click()
  reload_list()
  
def err_msg():
    doc["result"].html = "server didn't reply after %s seconds" %timeout

timeout = 4
def get(url,param={}):
    req = ajax.ajax()
    req.bind('complete',get_complete)
    req.set_timeout(timeout,err_msg)
    send_param = url
    for i in param.keys():
      if(isinstance(param[i],list)):
        for j in param[i]:
          send_param += i + "," + b64.encode(j) + ","
      else:
        send_param += i + "," + b64.encode(param[i]) + ","
#    print("send_param="+send_param)
    req.open('GET',send_param,True)
    req.send()

def put_callback(data,text_status):
#  reload_list()
  work = data['responseJSON']
#    print(i)
#  work = json.parse(str(data))
#  print("data="+data)
#  print("text_status"+text_status)
#  print("req="+req)
  i = 0
#  print(work['item'][i].main_comment)
  
  add_html = ""
#  print(now_hash)
  add_html += "<h2>" + work['item'][i].main_comment + "</h2>"
  add_html += "<p>" + work['item'][i].url + "</p>"
  add_html += "<p>" + work['item'][i].sub_comment + "</p>"
  add_html += "<p class = 'shikoiine' id = '"+str(work['item'][i].ID)+"'>shikoiine:" + str(work['item'][i].shikoiine) + "</p>"
  add_html += "<p class = 'naerune' id = '"+str(work['item'][i].ID)+"'>naerune:" + str(work['item'][i].naerune) + "</p>"
  add_html += "<p class = 'guilty' id = '"+str(work['item'][i].ID)+"'>guilty:" + str(work['item'][i].guilty) + "</p>"
  add_html += "<p>ID:" + str(work['item'][i].ID) + "</p>"
#  last_id = data['item'][i].ID
  for tag_index in range(0,len(work['item'][i].tag)):
    add_html += "<p class='tag'>" + work['item'][i].tag[tag_index] + "</p>"
  print(add_html)
  doc[now_hash].html = add_html
  jq(".shikoiine").on("click",shikoiine_click)
  jq(".naerune").on("click",naerune_click)
  jq(".guilty").on("click",guilty_click)
  jq(".tag").on("click",tag_select)

  


def put(url,param):
  jq.put(url, param,put_callback,(lambda request, text_status, error_thrown:print("session failed")))

#postメソッド自体は分離してjqコールバック内から関数だけ呼び出しのほうが健全かな。
def post(ev):
    url = api_address
    req = ajax.ajax()
    req.bind('complete',post_complete)
    req.set_timeout(timeout,err_msg)

    req.open('POST',url,True)
    req.set_header('content-type','application/x-www-form-urlencoded')

    req.send({
      'main_comment':b64.encode(doc['main_comment'].value),
      'sub_comment':b64.encode(doc['sub_comment'].value),
      'url':b64.encode(doc['url'].value),
      'tag':b64.encode(doc['tag'].value)
    })
    doc['main_comment'].value = ""
    doc['sub_comment'].value = ""
    doc['url'].value = ""
    doc['tag'].value = ""
#    print("ポストしたよ")
    return(0)
    
def reload_list():
  global content_index
  doc["contents_list"].html = ""
  index_memo = content_index
  content_index = 0
  get(api_address,{"id":-1,"tag":selected_tag,"num":index_memo})
  
def tag_select(ev):
  global selected_tag
  if selected_tag[0] == "-1":
    selected_tag = [ev.target.text]
  else:
    selected_tag.append(ev.target.text)
  reload_list()
#  print(selected_tag)

def inview_callback(event, isInView):
  global last_id
  global selected_tag
  global req_num
  if(isInView):
#    print("見えた")
    get(api_address,{"id":last_id,"tag":selected_tag,"num":int(req_num)})#-1でnone指定

  else:
#    print("消えた")
    pass

jq('#last').on('inview', inview_callback)
jq('.shikotta-button').on('click',post)