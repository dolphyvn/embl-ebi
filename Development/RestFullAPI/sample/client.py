import requests
import random
import json
import string
from random import randrange
from pymongo import MongoClient


# Generate random data for insert and update
first_name=('John','Andy','Joe','Bob','Adam')
last_name=('Johnson','Smith','Williams','Markham','Caleb')
favourite_colour=('red','green','blue','yellow','pink')
age = random.randint(15,99)
id_card = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
################################################
app_url = 'http://127.0.0.1:5000/api'
app_login_url = 'http://127.0.0.1:5000/login'
app_logout_url = 'http://127.0.0.1:5000/logout'
mongo_host = '127.0.0.1'
mongo_port = 27017

# Get random _id from mongodb for testing purpose
def get_random_id():
  client = MongoClient(mongo_host, mongo_port)
  db = client.person 
  collection = db.person 
  r = collection.find_one({})
  _id = (r.get('_id'))
  return str(_id)

# Prepare header for authentication after login with user and password
def get_header(auth_token):
	header = {'Authorization': 'Bearer ' + auth_token}
	return header

# Main functions
def insert(header):

	person_data = {
	        "first_name": random.choice(first_name),
	        "last_name": random.choice(last_name),
	        "age": age,
	        "favourite_colour": random.choice(favourite_colour),
	        "id_card": id_card
	    	}
	r = requests.post(app_url,json=person_data,headers=header)
	return json.loads(r.text)

def update(header):

	person_data = {
	        "first_name": random.choice(first_name),
	        "last_name": random.choice(last_name),
	        "age": age,
	        "favourite_colour": random.choice(favourite_colour),
	        "id_card": id_card,
	        "id": get_random_id()
	    	}
	r = requests.put(app_url,json=person_data,headers=header)
	return json.loads(r.text)

def delete(header):
	person_data = {
	        "id": get_random_id()
	    	}
	r = requests.delete(app_url,json=person_data,headers=header)
	return json.loads(r.text)

def get(header):
	r = requests.get(app_url,headers=header)
	return json.loads(r.text)

def login():
	data = {"username":"test","password":"test"}
	r = requests.post(app_login_url,json=data)
	data = json.loads(r.text)
	auth_token = data['access_token']
	return data['access_token']

def logout(header):

	r = requests.post(app_logout_url,headers=header)
	return (r.text)

if __name__ == "__main__":
	auth_token = login()
	header = get_header(auth_token)
	auth = get(header)
	insert(header)
	print(auth)
