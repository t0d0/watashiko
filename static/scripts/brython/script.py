from browser import window,document, alert
from browser import document as doc
from browser import ajax
#import base64
from javascript import JSConstructor
jq = window.jQuery
b64 = window.Base64
#print(b64.encode("あああ"))

def on_complete(req):
#  print(req.text)
#      for i in range(0,15):
  doc["contents_list"].html += "<li>" + (req.text) + "</li>"

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

#def fake_qs():
#    return '?foo=%s' %time.time()

def get(url,param={}):
    req = ajax.ajax()
    req.bind('complete',on_complete)
    req.set_timeout(timeout,err_msg)
    send_param = url
    for i in param.keys():
      if(isinstance(param[i],list)):
        for j in param[i]:
#          print(type(j))
#          work = base64.urlsafe_b64encode("iii")
          send_param += i + "," + b64.encode(j) + ","
      else:
#        print(param[i].encode('utf-8'))
        send_param += i + "," + b64.encode(param[i]) + ","
    print(send_param)
    req.open('GET',send_param,True)
    req.send()
#    print(req.text)
#      print(i)



def callback(event, isInView):
  if(isInView):
    print("見えた")
#    print( base64.b64encode("見えた"))
    get("http://t0d0.jp:8889/api/",{"id":"-1","tag":["-1"]})#-1でnone指定
#    contents_list.appendChild()
#    for i in range(0,15):
#      doc["contents_list"].html += "<li>test</li>"
  else:
    print("消えた")

jq('#last').on('inview', callback)
