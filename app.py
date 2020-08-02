from flask import Flask
from flask_restful import Api
from werkzeug import exceptions

from db import db

from resources import board, pin
from config import DB_URL
# from resources import user, board, pin, common
# from models.database import initialize

app = Flask(__name__)
# app.config.from_pyfile('config.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.errorhandler(exceptions.BadRequest)
def handle_400_error(error_message):
    response = {'Exception': error_message}
    return response, 400


@app.errorhandler(exceptions.MethodNotAllowed)
def handle_405_error(error_message):
    response = {'Exception': error_message}
    return response, 405


# api.add_resource(common.Hello, '/hello')
# api.add_resource(user.UserSignUpResource, '/signup')
# api.add_resource(user.UserAuthResource, '/auth')
api.add_resource(pin.PinItemResource, '/pins/<id>')
api.add_resource(pin.PinListResource, '/pins')
api.add_resource(pin.PinBulkResource, '/pins/bulk')
api.add_resource(board.BoardItemResource, '/boards/<id>')
api.add_resource(board.BoardListResource, '/boards')
api.add_resource(board.BoardBulkResource, '/boards/bulk')
# api.add_resource(board.BoardListResource, '/board-list')
# api.add_resource(board.BoardItemResource, '/board/<title>')

if __name__ == '__main__':
    # initialize()
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='localhost', port=8000)
