from flask import jsonify, make_response, request, Blueprint

from . import db_session
from .__all_models import User

blueprint = Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict()
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'user': user.to_dict()
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'hashed_password']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    user = User()
    user.surname = request.json['surname'],
    user.name = request.json['name'],
    user.age = request.json['age'],
    user.position = request.json['position'],
    user.speciality = request.json['speciality'],
    user.address = request.json['address'],
    user.email = request.json['email'],
    user.hashed_password = request.json['hashed_password']
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'id': user.id})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id).first()
    if not user:
        return make_response(jsonify({'error': 'Not Found'}), 404)
    user.surname = request.json['surname'] if 'surname' in request.json.keys() else user.surname
    user.name = request.json['name'] if 'name' in request.json.keys() else user.name
    user.age = request.json['age'] if 'age' in request.json.keys() else user.age
    user.position = request.json['position'] if 'position' in request.json.keys() else user.position
    user.speciality = request.json['speciality'] if 'speciality' in request.json.keys() else user.speciality
    user.address = request.json['address'] if 'address' in request.json.keys() else user.address
    user.email = request.json['email'] if 'email' in request.json.keys() else user.email
    user.hashed_password = request.json['hashed_password'] if 'hashed_password' in request.json.keys() else user.hashed_password
    db_sess.commit()
    return jsonify({'id': user.id})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})
