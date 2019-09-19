from flask import Flask
from flask_restful import Api
from werkzeug import exceptions

from resources import user, board, pin, common
from models.database import initialize

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
api = Api(app)


@app.errorhandler(exceptions.BadRequest)
def handle_400_error(error_message):
    response = {'Exception': error_message}
    return response, 400


@app.errorhandler(exceptions.MethodNotAllowed)
def handle_405_error(error_message):
    response = {'Exception': error_message}
    return response, 405


api.add_resource(common.Hello, '/hello')
api.add_resource(user.UserSignUpResource, '/signup')
api.add_resource(user.UserAuthResource, '/auth')
api.add_resource(pin.PinResource, '/pin')
api.add_resource(pin.PinListResource, '/pin-list')
api.add_resource(pin.PinItemResource, '/pin/<name>')
api.add_resource(board.BoardResource, '/board')
api.add_resource(board.BoardListResource, '/board-list')
api.add_resource(board.BoardItemResource, '/board/<title>')

if __name__ == '__main__':
    initialize()
    app.run(host='localhost', port=8000)