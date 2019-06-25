# -*- coding: utf-8 -*-
from peewee import Model, CharField
from flask import g, request
from flask_restful import Resource
from flask_bcrypt import check_password_hash, generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

import config
from . import DB


# 사용자를 정의하는 User 모델 정의
class User(Model):
    id = CharField(primary_key=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DB

    # 사용자 정보로 User 생성
    @classmethod
    def create_user(cls, id, email, password):
        email = email.lower()
        try:
            cls.select().where(
                (cls.email == email) | (cls.id == id)
            ).get()
        except cls.DoesNotExist:
            # 주어진 password를 bcrypt로 암호화
            user = cls.create(id=id, email=email, password=generate_password_hash(password).decode('utf-8'))
            user.save()
            g.user = user
            return {'id': user.id,
                    'email': user.email,
                    'password': user.password}
        else:
            return {'exception': 'this user already exists'}

    @classmethod
    def select_user(cls, id, password):
        try:
            user = cls().select().where(cls.id == id).get()
        except cls.DoesNotExist:
            return {'Exception': 'Your id does not exist in our User Id list'}
        else:
            # 주어진 password를 확인
            if check_password_hash(user.password, password):
                return {'id': user.id,
                        'email': user.email,
                        'password': user.password}
            else:
                return {'Exception': 'Your password does not match'}

    # 인증에 쓰이는 Token을 발급
    def generate_auth_token(self, expires=3600):
        serializer = Serializer(config.SECRET_KEY, expires_in=expires)
        return serializer.dumps({'id': self.id})

    # Token 확인
    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(config.SECRET_KEY)
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.select().where(User.id == data['id']).get()
        return user

# /user
class UserApi(Resource):
    # 입력한 정보로 유저 생성
    def post(self):
        try:
            get_id = request.args.get('id', None)
            get_email = request.args.get('email', 'default')
            get_password = request.args.get('password', None)
            if get_id is None or get_password is None:
                return {'Exception': 'You should give us id and password'}, 400
            user = User.create_user(id=get_id, email=get_email, password=get_password)
            User.generate_auth_token(user)
            return user, 201
        except Exception as e:
            return {'Exception': str(e)}, 409

    def get(self):
        get_id = request.args.get('id', None)
        get_password = request.args.get('password', None)
        if get_id is None or get_password is None:
            return {'Exception': 'You should give us id and password'}, 400
        user = User.select_user(id=get_id, password=get_password)
        if user['exception'] is not None:
            return user, 404
        return user, 200
