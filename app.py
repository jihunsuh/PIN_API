from flask import Flask, g, jsonify
from flask_restful import Api
from auth import basic_auth, token_auth
import model
import resource
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
api = Api(app)


@app.route('/home', methods=['POST'])
def index():
    return 'hey, {}!'.format(basic_auth.id())


@app.route('/token', methods=['GET'])
@basic_auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@app.route('/api/resource', methods=['GET'])
@basic_auth.login_required
def get_resource():
    return {'data': 'Hello, %s!' % g.user.username}


api.add_resource(resource.User, '/user')
api.add_resource(resource.Home, '/hello')
api.add_resource(resource.Pin, '/pin')
api.add_resource(resource.Board, '/board')
api.add_resource(resource.PinList, '/pin/list')
api.add_resource(resource.BoardList, '/board/list')

if __name__ == '__main__':
    model.initialize()
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
