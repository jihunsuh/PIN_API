from flask import request
from flask_restful import Resource
from models.User import User as UserModel


# /user
class UserResource(Resource):
    # 입력한 정보로 유저 생성
    def post(self):
        try:
            get_username = request.args['username']
            get_email = request.args['email']
            get_password = request.args['password']
        except KeyError:
            return {'Exception': 'You should give us username or password'}, 400

        user = UserModel.create_user(username=get_username, email=get_email, password=get_password)
        return user, 201

    def get(self):
        try:
            get_username = request.args['username']
            get_password = request.args['password']
        except KeyError:
            return {'Exception': 'You should give us username or password'}, 400

        user = UserModel.select_user(username=get_username, password=get_password)

        if user['exception']:
            return user, 400
        return user, 200

