from browser import window,document, alert
from browser import document as doc
from browser import ajax


jq = window.jQuery


def on_complete(req):
    if req.status==200 or req.status==0:
        doc["result"].html = req.text
    else:
        doc["result"].html = "error "+req.text

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
          send_param += i + "=" + j + ","
      else:
        send_param += i + "=" +param[i] + ","
    print(send_param)  
    req.open('GET',send_param,True)
    req.send()


def callback(event, isInView):
  if(isInView):
    print("見えた")
    get("http://t0d0.jp:8889/api/",{"id":"123","tag":["tag1","tag2"]})
#    contents_list.appendChild()
    for i in range(0,15):
      doc["contents_list"].html += "<li>test</li>"
  else:
    print("消えた")

jq('#last').on('inview', callback)
