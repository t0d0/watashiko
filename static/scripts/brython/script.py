from browser import window,document, alert
from browser import document as doc
from browser import ajax

json = window.JSON
jq = window.jQuery
b64 = window.Base64
last_id = -1;
def on_complete(req):
  global last_id
  data = json.parse(str(req.text))
  print(len(data['item']))
  for i in range(0,len(data['item'])-1):
    add_html = "<li>"
    add_html += "<h2>" + data['item'][i].main_comment + "</h2>"
    add_html += "<p>" + data['item'][i].url + "</p>"
    add_html += "<p>" + data['item'][i].sub_comment + "</p>"
    add_html += "<p>shikoiine:" + str(data['item'][i].shikoiine) + "</p>"
    add_html += "<p>naerune:" + str(data['item'][i].naerune) + "</p>"
    add_html += "<p>guilty:" + str(data['item'][i].guilty) + "</p>"
    add_html += "<p>ID:" + str(data['item'][i].ID) + "</p>"
    last_id = data['item'][i].ID
    for tag_index in range(0,len(data['item'][i].tag)):
      add_html += "<p>" + data['item'][i].tag[tag_index] + "</p>"
    add_html += "</li>"
    doc["contents_list"].html += add_html

#    if req.status==200 or req.status==0:
#        doc["result"].html = req.text
#        print("aaaaa"+req.text)
#    else:
#        doc["result"].html = "error "+req.text
#        print(req.text)
  pass

def err_msg():
    doc["result"].html = "server didn't reply after %s seconds" %timeout

timeout = 4


def get(url,param={}):
    req = ajax.ajax()
    req.bind('complete',on_complete)
    req.set_timeout(timeout,err_msg)
    send_param = url
    for i in param.keys():
      if(isinstance(param[i],list)):
        for j in param[i]:
          send_param += i + "," + b64.encode(j) + ","
      else:
        send_param += i + "," + b64.encode(param[i]) + ","
    print(send_param)
    req.open('GET',send_param,True)
    req.send()

def callback(event, isInView):
  global last_id
  if(isInView):
    print("見えた")
    get("http://t0d0.jp:8889/api/",{"id":last_id,"tag":["-1"]})#-1でnone指定

  else:
    print("消えた")

jq('#last').on('inview', callback)
