from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
import userlogic

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

def get_users():
    query = userlogic.User.select()
    result = {}
    for user in query:
        result[user.id] = user.password
    return result


@basic_auth.get_password
def get_pw(username):
    if username in get_users():
        return userlogic.User.get(userlogic.User.id == username)
    return None


@basic_auth.verify_password
def verify_password(id, password):
    try:
        user = userlogic.User.get(userlogic.User.id == id)
        if not userlogic.verify_password(user.password, password):
            return False
    except userlogic.User.DoesNotExist:
        return False
    else:
        g.user = user
        return True


@token_auth.verify_token
def verify_token(token):
    user = userlogic.User.verify_auth_token(token)
    if user is not None:
        g.user = user
        return True
    return False


