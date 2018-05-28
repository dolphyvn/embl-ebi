from flask_restful import Api
from resources import Login, Logout, Person, FNameSearch, Index, app


api = Api(app)
api.add_resource(Index, "/")
api.add_resource(Person,"/api")
api.add_resource(Login,"/login")
api.add_resource(Logout,"/logout")
api.add_resource(FNameSearch,"/search/<string:name>")
api.add_resource(Person,"/api/<string:id>", endpoint="id")
api.add_resource(Person,"/api/<int:maximum>", endpoint="maximum")

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
