from flask_restful import Resource
from flask import request


# /hello Server 작동 확인
class Hello(Resource):
    def get(self):
        return {'name': request.args.get('name', '')}, 200

    def post(self):
        return {'message': 'hello, World!'}, 200

