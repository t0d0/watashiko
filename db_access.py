import pymongo
from functools import singledispatch


class DB_Access:
  def __init__(self):
    self.client = pymongo.MongoClient('localhost', 27017)
    self.db = self.client.watashiko_db
    self.co = self.db.watshiko_collection
    self.tag_co = self.db.watshiko_tag_collection
  
  def set_data(self,data):
    self.work = data
    data['ID'] = (self.get_max_ID() + 1)
    for i in data['tag']:
      if(not(self.tag_check(i))):
        self.set_tag(data['tag'])
    self.co.insert_one(data)
  
  def get_data(self,ID):
    return(self.co.find({'ID':ID}))


  def erase_data(self,ID):
    self.co.remove({'ID':ID})
  
  def get_tag_list(self):
    tags=[]
    for tag in self.tag_co.find():
      tags.extend(tag['tag'])
    return(list(set(tags)))
    
  def set_tag(self,tag):
    self.tag_co.insert_one({'tag':tag})

  def get_list(self,ID = '',tag = '',num = 10):#ID:
    if(ID == ''):
      ID = self.get_max_ID();
    if(tag == ''):
      return(self.co.find({'ID':{'$lt': ID}}).sort('ID',-1).limit(num))
    else:
      return(self.co.find({'ID':{'$lt': ID},'tag':tag}).sort('ID',-1).limit(num))

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