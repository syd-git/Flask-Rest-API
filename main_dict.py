from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

names = {"tim": {"age": 19, "gender": "Male"},
         "joe": {"age": 20, "gender": "Female"}
         }

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("name", type=str, help="Input for name is missing", required=True)
user_put_args.add_argument("age", type=int, help="Input for age is missing", required=True)

users = {}

def cancel_if_user_does_not_exist(userid):
    if userid not in users:
        abort(404, message=f"User with ID {userid} does not exist")

def cancel_if_user_exist(userid):
    if userid in users:
        abort(409, message=f"User with ID {userid} already exists")

class User(Resource):
    def get(self, userid):
        cancel_if_user_does_not_exist(userid)
        return users[userid]

    def put(self, userid):
        cancel_if_user_exist(userid)
        args = user_put_args.parse_args()
        users[userid] = args
        return users[userid], 201

    def delete(self, userid):
        cancel_if_user_does_not_exist(userid)
        del users[userid]
        return "", 204



class HelloWorld(Resource):
    def get(self, name):
        return names[name]

    def post(self):
        return {'result': 'post method OK'}

api.add_resource(User, '/users/<int:userid>')
api.add_resource(HelloWorld, '/hello/<string:name>')

if __name__ == "__main__":
    app.run(debug=True)
