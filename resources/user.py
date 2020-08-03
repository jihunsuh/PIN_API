from flask import request, abort
from flask_restful import Resource
from models.user import UserModel
from flask_jwt import jwt_required
from hashing import bcrypt


class SignUpResource(Resource):
    # POST /signup
    def post(self):
        try:
            body = request.json

            hashed_password = bcrypt.generate_password_hash(body['password'])

            body['password'] = hashed_password

            user = UserModel(**body)
            user.create()

            return {'message': "Welcome to PIN_API"}, 200
        except Exception as e:
            return {'Exception': str(e)}, 500


# class LoginResource(Resource):
#     # POST /login
#     def post(self):
#         try:
#             body = request.json
#             if not body['password']:
#                 raise Exception("Password Not Found")

#             user = UserModel.findOne(**body)

#             if not user:
#                 raise Exception("User Not Found")

#             return {'message': "successfully logined", 'data': user.json()}, 200
#         except Exception as e:
#             return {'Exception': str(e)}, 500
