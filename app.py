from flask import Flask
from flask_restful import Api

from resources import User, Board, Pin, Common
from models.Database import initialize

from config import SETTING, SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY
api = Api(app)


api.add_resource(Common.Hello, '/hello')
api.add_resource(User.UserResource, '/user')
api.add_resource(Pin.PinResource, '/pin')
api.add_resource(Pin.PinListResource, '/pin/list')
api.add_resource(Board.BoardResource, '/board')
api.add_resource(Board.BoardListResource, '/board/list')

if __name__ == '__main__':
    initialize()
    app.run(**SETTING)
