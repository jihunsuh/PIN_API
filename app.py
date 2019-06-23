from flask import Flask
from flask_restful import Api

import model
import resource
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
api = Api(app)


api.add_resource(resource.AuthAndTokenApi, '/token')
api.add_resource(resource.UserApi, '/user')
api.add_resource(resource.HelloApi, '/hello')
api.add_resource(resource.PinApi, '/pin')
api.add_resource(resource.BoardApi, '/board')
api.add_resource(resource.PinListApi, '/pin/list')
api.add_resource(resource.BoardListApi, '/board/list')