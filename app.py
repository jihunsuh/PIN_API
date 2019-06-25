from flask import Flask
from flask_restful import Api

from models import User, Board, Pin, Common
from models.Database import initialize

import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
api = Api(app)


api.add_resource(Common.HelloApi, '/hello')
api.add_resource(Common.AuthAndTokenApi, '/token')
api.add_resource(User.UserApi, '/user')
api.add_resource(Pin.PinApi, '/pin')
api.add_resource(Pin.PinListApi, '/pin/list')
api.add_resource(Board.BoardApi, '/board')
api.add_resource(Board.BoardListApi, '/board/list')

# if __name__=='__main__':
#     initialize()
#     app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)