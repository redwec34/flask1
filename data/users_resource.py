from flask import jsonify
from flask_restful import abort, Resource

from . import db_session
from .users import User
from .user_parser import parser


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('name', 'surname', 'age', 'address',
                  'email', 'position', 'speciality', 'hashed_password'))})

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
        user = session.query(User).all()
        return jsonify({'user': [item.to_dict(
            only=('name', 'surname', 'age', 'address',
                  'email', 'position', 'speciality', 'hashed_password')) for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
            address=args['address'],
            email=args['email'],
            position=args['position'],
            speciality=args['speciality']
        )
        user.set_password(args['hashed_password'])
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})