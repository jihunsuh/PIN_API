from flask import Flask
from flask_restful import Api
from werkzeug import exceptions
from flask_jwt import JWT

from db import db
from hashing import bcrypt
from security import authenticate, identity
from resources import board, pin, user

import config


app = Flask(__name__)
app.config.from_object('config.CONFIG')
api = Api(app)


@app.errorhandler(exceptions.BadRequest)
def handle_400_error(error_message):
    response = {'Exception': str(error_message)}
    return response, 400


@app.errorhandler(exceptions.MethodNotAllowed)
def handle_405_error(error_message):
    response = {'Exception': str(error_message)}
    return response, 405


jwt = JWT(app, authenticate, identity)

# api.add_resource(user.LoginResource, '/login')
api.add_resource(user.SignUpResource, '/signup')
api.add_resource(pin.PinItemResource, '/pins/<id>')
api.add_resource(pin.PinListResource, '/pins')
api.add_resource(pin.PinBulkResource, '/pins/bulk')
api.add_resource(board.BoardItemResource, '/boards/<id>')
api.add_resource(board.BoardListResource, '/boards')
api.add_resource(board.BoardBulkResource, '/boards/bulk')

if __name__ == '__main__':
    # initialize()
    db.init_app(app)
    bcrypt.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='localhost', port=8000)
