from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"User (id = {self.id}, name = {self.name}, age = {self.age})"

app.app_context().push()
#db.create_all()

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("name", type=str, help="Input for name is missing", required=True)
user_post_args.add_argument("age", type=int, help="Input for age is missing", required=True)

user_patch_args = reqparse.RequestParser()
user_patch_args.add_argument("name", type=str)
user_patch_args.add_argument("age", type=int)


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'age': fields.Integer
}

class Users(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result = UserModel.query.all()
        return result

    @marshal_with(resource_fields)
    def post(self):
        args = user_post_args.parse_args()
        # result = UserModel.query.filter_by(id=userid).first()
        # if result:
        #     abort(409, message="User already exists")

        user = UserModel(name=args['name'], age=args['age'])
        db.session.add(user)
        db.session.commit()
        return user, 201

class User(Resource):
    @marshal_with(resource_fields)
    def get(self, userid):
        result = UserModel.query.filter_by(id=userid).first()
        if not result:
            abort(404, message="User not found")
        return result

    @marshal_with(resource_fields)
    def patch(self, userid):
        args = user_patch_args.parse_args()
        result = UserModel.query.filter_by(id=userid).first()
        if not result:
            abort(404, message="User not found: can't update")

        if args['name']:
            result.name = args['name']
        if args['age']:
            result.age = args['age']

        db.session.commit()
        return result, 200

    @marshal_with(resource_fields)
    def delete(self, userid):
        result = UserModel.query.filter_by(id=userid).first()
        if not result:
            abort(404, message="User not found: can't delete")
        db.session.delete(result)
        db.session.commit()
        return " ", 204


api.add_resource(Users, '/users', methods=['GET', 'POST'])
api.add_resource(User, '/users/<int:userid>', methods=['GET', 'DELETE', 'PATCH'])


if __name__ == "__main__":
    app.run(debug=True)
