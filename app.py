from flask import Flask, g, jsonify
from flask_restful import Api

import model
import resource
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
api = Api(app)


api.add_resource(resource.AuthAndToken, '/token')
api.add_resource(resource.User, '/user')
api.add_resource(resource.Hello, '/hello')
api.add_resource(resource.Pin, '/pin')
api.add_resource(resource.Board, '/board')
api.add_resource(resource.PinList, '/pin/list')
api.add_resource(resource.BoardList, '/board/list')

if __name__ == '__main__':
    model.initialize()
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
