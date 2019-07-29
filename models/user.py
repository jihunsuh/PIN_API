from peewee import Model, CharField
from flask_bcrypt import check_password_hash, generate_password_hash

from . import DB


# 사용자를 정의하는 User 모델 정의
class User(Model):
    username = CharField(primary_key=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DB

    # 사용자 정보로 User 생성
    @classmethod
    def create_user(cls, username, email, password):
        email = email.lower()
        try:
            cls.select().where(
                (cls.email == email) | (cls.username == username)
            ).get()
        except cls.DoesNotExist:
            # 주어진 password를 bcrypt로 암호화
            user = cls.create(username=username, email=email, password=generate_password_hash(password).decode('utf-8'))
            return {'username': user.username,
                    'email': user.email}
        else:
            return {'Exception': 'this user already exists'}

    @classmethod
    def select_user(cls, username, password):
        try:
            user = cls().select().where(cls.username == username).get()
            # 주어진 password를 확인
            if check_password_hash(user.password, password):
                return {'username': user.username,
                        'email': user.email,
                        'password': password}
            else:
                return {'Exception': 'Your password does not match'}
        except cls.DoesNotExist:
            return {'Exception': 'Your id does not exist in our User Id list'}


