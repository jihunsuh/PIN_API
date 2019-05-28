from peewee import Model, CharField, SqliteDatabase
from flask import g, Flask
from flask_bcrypt import Bcrypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

import config

app = Flask(__name__)
bcrypt = Bcrypt(app)
DB = SqliteDatabase('test_peewee.db')


# 사용자를 정의하는 User 모델 정의
class User(Model):
    id = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DB

    # 사용자 정보로 User 생성
    @classmethod
    def create_user(cls, id, email, password, **kwargs):
        email = email.lower()
        try:
            cls.select().where(
                (cls.email == email) | (cls.id == id)
            ).get()
        except cls.DoesNotExist:
            # 주어진 password를 bcrypt로 암호화
            user = cls.create(id=id, email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'))
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
            if bcrypt.check_password_hash(user.password, password):
                g.user = user
                return {'id': user.id,
                        'email': user.email,
                        'password': password}
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
