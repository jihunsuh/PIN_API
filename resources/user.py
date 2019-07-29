from flask import request
from flask_restful import Resource
from models.user import User as UserModel


# /user
class UserResource(Resource):
    # 입력한 정보로 유저 생성
    def post(self):
        try:
            username = request.args['username']
            email = request.args['email']
            password = request.args['password']
        except KeyError:
            return {'Exception': 'You should give us username or password'}, 400

        user = UserModel.create_user(username=username, email=email, password=password)
        return user, 201

    def get(self):
        try:
            username = request.args['username']
            password = request.args['password']
        except KeyError:
            return {'Exception': 'You should give us username or password'}, 400

        user = UserModel.select_user(username=username, password=password)

        if user.get('Exception'):
            return user, 401
        return user, 200
