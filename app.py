from flask import Flask
from flask_restful import Api

from resources import user, board, pin, common
from models.database import initialize

import config

app = Flask(__name__)
app.config.from_object('config.DefaultConfig')
api = Api(app)

api.add_resource(common.Hello, '/hello')
api.add_resource(user.UserResource, '/user')
api.add_resource(pin.PinResource, '/pin')
api.add_resource(pin.PinListResource, '/pin/<name>')
api.add_resource(board.BoardResource, '/board')
api.add_resource(board.BoardListResource, '/board/<title>')

if __name__ == '__main__':
    initialize()
    app.run(host=config.HOST, port=config.PORT)