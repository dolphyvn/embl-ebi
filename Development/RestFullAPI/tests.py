import unittest
import run as restfullapi
import requests
import json
import sys
import string
from random import randrange
from flask_pymongo import ObjectId
from pymongo import MongoClient
import random
# class TestFlaskApiUsingRequests(unittest.TestCase):
#     def test_hello_world(self):
#         response = requests.get('http://localhost:5000')
#         self.assertEqual(response.json(), {'msg':'api'})
data = {"username":"test","password":"test"}
first_name=('John','Andy','Joe','Bob','Adam')
last_name=('Johnson','Smith','Williams','Markham','Caleb')
favourite_colour=('red','green','blue','yellow','pink')
age = random.randint(15,99)
app_url = 'http://localhost:5000/api'
app_login_url = 'http://localhost:5000/login'
app_logout_url = 'http://localhost:5000/logout'
id_card = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))


class TestFlaskApi(unittest.TestCase):

    
    def setUp(self):

      self.app = restfullapi.app.test_client()
      self.mongo_host = restfullapi.app.config['MONGO_HOST']
      self.mongo_port = restfullapi.app.config['MONGO_PORT']
      self.mongo_dbname = restfullapi.app.config["MONGO_DBNAME"]
      # self.mongo = PyMongo(self.app)

    def get_header(self,auth_token):

      header = {'Authorization': 'Bearer ' + auth_token}
      return header

    def get_access_token(self):

      r = self.app.post('/login',json=data)
      resp = json.loads(r.get_data().decode(sys.getdefaultencoding()))
      access_token = (resp['access_token'])
      return access_token,resp

    def get_random_id(self):
      client = MongoClient(self.mongo_host, self.mongo_port)
      db = client.person 
      collection = db.person 
      r = collection.find_one({})
      _id = (r.get('_id'))
      return str(_id)

      
      #data = resources.mongo.db.person.find({})
      # r = self.mongo.db.person.find({})
      # for i in r:
      #   users.add(i.get('_id'))

      # return random.choice(users)

    def test_index(self):
      r = self.app.get('/')
      resp = json.loads(r.get_data().decode(sys.getdefaultencoding()))
      self.assertEqual(resp, {'msg':'api'})

    def test_login(self):

      access_token,resp = self.get_access_token()
      self.assertEqual(resp,{'msg':'Successfully logged in','access_token':access_token})

    def test_logout(self):

      access_token,resp = self.get_access_token()
      header = self.get_header(access_token)
      r = self.app.post('/logout',headers=header)
      resp = json.loads(r.get_data().decode(sys.getdefaultencoding()))
      self.assertEqual(resp,{"msg": "Successfully logged out"})
    def test_insert(self):

      access_token = self.get_access_token()[0]
      header = self.get_header(access_token)

      person_data = {
              "first_name": random.choice(first_name),
              "last_name": random.choice(last_name),
              "age": age,
              "favourite_colour": random.choice(favourite_colour),
              "id_card": id_card
            }
      r = self.app.post('/api',json=person_data,headers=header)
      resp = json.loads(r.get_data().decode(sys.getdefaultencoding()))
      self.assertEqual(resp,{'status': 'Insert Successfully'})

    def test_update_existing_acc(self):

      access_token = self.get_access_token()[0]
      header = self.get_header(access_token)

      person_data = {
              "first_name": random.choice(first_name),
              "last_name": random.choice(last_name),
              "age": age,
              "favourite_colour": random.choice(favourite_colour),
              "id_card": id_card,
              "id": self.get_random_id()
            }
      r = self.app.put('/api',json=person_data,headers=header)
      resp = json.loads(r.get_data().decode(sys.getdefaultencoding()))
      self.assertEqual(resp,{'status': 'Update Successfully'})

    def test_update_non_existing_acc(self):

      access_token = self.get_access_token()[0]
      header = self.get_header(access_token)

      person_data = {
              "first_name": random.choice(first_name),
              "last_name": random.choice(last_name),
              "age": age,
              "favourite_colour": random.choice(favourite_colour),
              "id_card": id_card,
              "id": "5afe433e0a721629d7dc4fbb"
            }
      r = self.app.put('/api',json=person_data,headers=header)
      resp = json.loads(r.get_data().decode(sys.getdefaultencoding()))
      self.assertEqual(resp,{'status': 'Update Successfully'})

    def test_delete_existing_acc(self):

      access_token = self.get_access_token()[0]
      header = self.get_header(access_token)

      person_data = {
              "id": self.get_random_id()
            }
      r = self.app.delete('/api',json=person_data,headers=header)
      resp = json.loads(r.get_data().decode(sys.getdefaultencoding()))
      #self.assertEqual(resp,{'status':'Delete Successfully'})
      self.assertEqual(resp,{'status':'Delete Successfully'})

    def test_delete_non_existing_acc(self):

      access_token = self.get_access_token()[0]
      header = self.get_header(access_token)

      person_data = {
              "id": "5afe433e0a721629d7dc4fbb"
            }
      r = self.app.delete('/api',json=person_data,headers=header)
      resp = json.loads(r.get_data().decode(sys.getdefaultencoding()))
      #self.assertEqual(resp,{'status':'Delete Successfully'})
      self.assertEqual(resp,{'status':'Id not exist'})


if __name__ == "__main__":
    unittest.main()
