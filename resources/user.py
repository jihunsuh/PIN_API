from flask import request
from flask_restful import Resource
from models.user import User as UserModel


# /signup
class UserSignUpResource(Resource):
    """
    입력한 정보로 유저를 생성합니다.
    """
    def post(self):
        data = request.get_json()
        try:
            user = UserModel.create_user(**data)
        except KeyError:
            return {'Exception': 'You should give us username or password'}, 400

        return user, 201


# /auth
class UserAuthResource(Resource):
    def get(self):
        """
        입력한 정보가 유저 테이블 안에 있는지를 확인하고 그 결과를 리턴합니다.
        :return:
        """
        data = request.get_json()
        try:
            user = UserModel.select_user(**data)
        except KeyError:
            return {'Exception': 'You should give us username or password'}, 400

        if user.get('Exception'):
            return user, 401
        return user, 200
