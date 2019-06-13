from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_bcrypt import check_password_hash
from userlogic import User

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.get_password
def get_password(username):
    try:
        password = User.select().where(User.id == username).get().password
        return password
    except User.DoesNotExist:
        return None


@basic_auth.verify_password
def verify_password(id, password):
    try:
        user = User.get(User.id == id)
        if not check_password_hash(user.password, password):
            return False
        g.user = user
        return True
    except User.DoesNotExist:
        return False


@token_auth.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if user is not None:
        g.user = user
        return True
    return False

