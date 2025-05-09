from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data.users import User
from data import db_session

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('about', required=True)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('name', 'about', 'email'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'news': [item.to_dict(
            only=('name', 'about', 'email')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            name=args['name'],
            about=args['about'],
            email=args['email']
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})
