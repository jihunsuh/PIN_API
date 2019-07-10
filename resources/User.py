from flask import request
from flask_restful import Resource

from models.User import User as UserModel


# /user
class UserResource(Resource):
    # 입력한 정보로 유저 생성
    def post(self):
        try:
            get_id = request.args.get('id', None)
            get_email = request.args.get('email', 'default')
            get_password = request.args.get('password', None)
            if get_id is None or get_password is None:
                return {'Exception': 'You should give us id and password'}, 400
            user = UserModel.create_user(id=get_id, email=get_email, password=get_password)
            UserModel.generate_auth_token(user)
            return user, 201
        except Exception as e:
            return {'Exception': str(e)}, 409

    def get(self):
        get_id = request.args.get('id', None)
        get_password = request.args.get('password', None)
        if get_id is None or get_password is None:
            return {'Exception': 'You should give us id and password'}, 400
        user = UserModel.select_user(id=get_id, password=get_password)
        if user['exception'] is not None:
            return user, 404
        return user, 200
