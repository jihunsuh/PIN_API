from flask_restful import Resource
from flask import g, request
from auth import basic_auth


# /hello Server 작동 확인
class HelloApi(Resource):
    def get(self):
        return {'name': request.args.get('name', '')}, 200

    def post(self):
        return {'message': 'hello, World!'}, 200


# /token token 기반 인증 확인
class AuthAndTokenApi(Resource):
    @basic_auth.login_required
    def get(self):
        token = g.user.generate_auth_token()
        return {'token': token.decode('ascii')}, 200

    @basic_auth.login_required
    def post(self):
        return {'data': 'Hello, %s!' % g.user.id}, 200
