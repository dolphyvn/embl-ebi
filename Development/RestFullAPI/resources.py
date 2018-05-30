from flask_restful import Resource
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, ObjectId
#from flask_jwt import JWT, jwt_required, current_identity
#from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity,get_raw_jwt
)
import json



app = Flask(__name__)
app.config["MONGO_DBNAME"] = "person"
app.config['MONGO_PORT'] = 27017
app.config['MONGO_HOST'] = 'mongodb'
mongo = PyMongo(app)
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
jwt = JWTManager(app)
blacklist = set()


class Login(Resource):
  def post(self):
      if not request.is_json:
          return jsonify({"msg": "Missing JSON in request"})

      username = request.json.get('username', None)
      password = request.json.get('password', None)
      if not username:
          return jsonify({"msg": "Missing username parameter"})
      if not password:
          return jsonify({"msg": "Missing password parameter"})

      if username != 'test' or password != 'test':
          return jsonify({"msg": "Bad username or password"})
      
      access_token = create_access_token(identity=username)
      return jsonify(msg='Successfully logged in',access_token=access_token)

class Logout(Resource):

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
      jti = decrypted_token['jti']
      return jti in blacklist

    @jwt_required
    def post(self):
      username = get_raw_jwt()['identity']
      jti = get_raw_jwt()['jti']
      blacklist.add(jti)
      return jsonify({'msg': 'Successfully logged out'})

class Person(Resource):
  @jwt_required
  def get(self,id=None,maximum=None):
    data = []
    if id:
      result = mongo.db.person.find_one({"_id": ObjectId(id)}, {"_id": 0,"id_card": 0})
      return jsonify({'Person':result})
    elif maximum:
      result = mongo.db.person.find({},{"_id": 0,"id_card": 0}).limit(maximum)
      for res in result:
        data.append(res)
      return jsonify({'Person':data})
    else:
      result = mongo.db.person.find({},{"_id": 0,"id_card": 0})
      for res in result:
        data.append(res)
      return jsonify({'Person':data})

  @jwt_required
  def post(self):
    data = request.get_json()
    if not data:
      return {"status": "Insert Error"}
    else:
      if data.get('id_card'):
        if mongo.db.person.find_one({'id_card':data.get('id_card')}):
          return jsonify({"status":"Person existing"})
        else:
          p_id = mongo.db.person.insert_one(data).inserted_id
          if p_id:
            return jsonify({"status": "Insert Successfully"})
      else:
        p_id = mongo.db.person.insert_one(data).inserted_id
        if p_id:
          return jsonify({"status": "Insert Successfully"})

  @jwt_required
  def put(self):
    data = request.get_json()
    id = data.get('id')
    data.pop('id')
    p_up = mongo.db.person.update_one({"_id":ObjectId(id)},{'$set': data})
    if p_up:
      return jsonify({"status": "Update Successfully"})
    else:
      return jsonify({"status": "Update Error"})

  @jwt_required
  def delete(self):
    data = request.get_json()
    id = data.get('id')
    if id:
      count = mongo.db.person.delete_one({'_id':ObjectId(id)}).deleted_count
      if count:
        return {'status':'Delete Successfully'}
      else:
        return {'status':'Id not exist'}

class FNameSearch(Resource):
  def get(self,name=None):
    data = []
    if name:
      result = mongo.db.person.find({"first_name":name})
      for res in result:
        data.append(res)
      return jsonify({'Person':'ok'})

class LNameSearch(Resource):
  def get(self,name=None):
    data = []
    if name:
      result = mongo.db.person.find({"last_name":name},{"_id": 0})
      for res in result:
        data.append(res)
      return jsonify({'Person':data})

class Index(Resource):
  def get(self):
    return {'msg':'api'}
