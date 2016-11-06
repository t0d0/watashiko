import pymongo
from functools import singledispatch
from datetime import datetime

class DB_Access:
  def __init__(self):
    self.client = pymongo.MongoClient('localhost', 27017)
    self.db = self.client.watashiko_db
    self.co = self.db.watshiko_collection
    self.tag_co = self.db.watshiko_tag_collection
  
  def set_data(self,data):
    self.work = data
    data['ID'] = (self.get_max_ID() + 1)
    data['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['shikoiine'] = 0
    data['naerune'] = 0
    data['guilty'] = 0
    for i in data['tag']:
      if(not(self.tag_check(i))):
        self.set_tag(data['tag'])
    self.co.insert_one(data)

  def get_data(self,ID):
    return(self.co.find({'ID':ID},{"_id":0}))

  def erase_data(self,ID):
    self.co.remove({'ID':ID})

  def get_tag_list(self):
    tags=[]
    for tag in self.tag_co.find():
      tags.extend(tag['tag'])
    return(list(set(tags)))

  def set_tag(self,tag):
    self.tag_co.insert_one({'tag':tag})

  def get_list(self,ID = '',tag = '',num = 10):
    if(ID == '' or ID == -1):
      ID = self.get_max_ID()+1;
    if(tag == '' or tag[0] == "-1"):
      print("tag is none")
      return(self.co.find({'ID':{'$lt': ID}},{"_id":0}).sort('ID',-1).limit(num))
    else:
      return(self.co.find({'ID':{'$lt': ID},'tag':{'$in':tag}},{"_id":0}).sort('ID',-1).limit(num))

  def update_shikoiine(self,ID):
    self.co.update({'ID':ID}, {'$inc':{'shikoiine':1}})

  def update_naerune(self,ID):
    self.co.update({'ID':ID}, {'$inc':{'naerune':1}})

  def update_guilty(self,ID):
    self.co.update({'ID':ID}, {'$inc':{'guilty':1}})

  def get_max_ID(self):
    for i in self.co.find().sort('ID',-1).limit(1):
      return(i['ID'])

  def tag_check(self,tag):
    for i in self.tag_co.find({'tag':tag}):
      return(True)
    return(False)
  
db = DB_Access()
#db.erase_data(35)
#db.erase_data(34)
for i in range(0,98):
  db.erase_data(i)
#for i in db.get_list():
#  print(i)