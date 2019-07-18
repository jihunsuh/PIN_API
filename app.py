from flask import Flask
from flask_restful import Api

from resources import user, board, pin, common
from models.database import initialize

from config import SETTING, SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY
api = Api(app)

api.add_resource(common.Hello, '/hello')
api.add_resource(user.UserResource, '/user')
api.add_resource(pin.PinResource, '/pin')
api.add_resource(pin.PinListResource, '/pin/list')
api.add_resource(board.BoardResource, '/board')
api.add_resource(board.BoardListResource, '/board/list')

if __name__ == '__main__':
    initialize()
    app.run(**SETTING)
