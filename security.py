from werkzeug.security import safe_str_cmp
from models.user import UserModel
from hashing import bcrypt


def authenticate(username, password):
    user = UserModel.findOne(username=username)
    if user and bcrypt.check_password_hash(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    print(user_id)
    return UserModel.findOne(id=user_id)
