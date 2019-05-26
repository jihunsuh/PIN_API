from flask_restful import Resource, reqparse, marshal_with, fields
from flask import jsonify, make_response, g
from auth import basic_auth, token_auth
import model


# /hello Server 작동 확인
class Home(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', required=True, type=str, help='give us right name')
            args = parser.parse_args()
            return make_response(args['name'], 200)
        except Exception as e:
            return make_response(jsonify({'Exception': str(e)}), 409)

    def post(self):
        return make_response(jsonify({'message': 'hello, World!'}), 200)


# /token token 기반 인증 확인
class AuthAndToken(Resource):
    @basic_auth.login_required
    def get(self):
        token = g.user.generate_auth_token()
        return make_response(jsonify({'token': token.decode('ascii')}), 200)

    @basic_auth.login_required
    def post(self):
        return make_response(jsonify({'data': 'Hello, %s!' % g.user.id}), 200)


# /user
class User(Resource):
    # 입력한 정보로 유저 생성
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(
                'id',
                type=str
            )
            parser.add_argument(
                'email',
                type=str
            )
            parser.add_argument(
                'password',
                type=str
            )
            args = parser.parse_args()
            get_id = args['id']
            get_email = args['email']
            get_password = args['password']
            user = model.User.create_user(id=get_id, email=get_email, password=get_password)
            return make_response(jsonify(user), 201)
        except Exception as e:
            return make_response(jsonify({'Exception': str(e)}), 409)

    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(
                'id',
                type=str
            )
            parser.add_argument(
                'password',
                type=str
            )
            args = parser.parse_args()
            get_id = args['id']
            get_password = args['password']
            user = model.User.select_user(id=get_id, password=get_password)
            return make_response(jsonify(user), 200)
        except Exception as e:
            return make_response(jsonify({'Exception': str(e)}), 409)


# /pin
class Pin(Resource):
    # C 입력한 정보로 새 Pin을 만들어 DB 안에 삽입
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(
                'name',
                type=str,
                help='give me right name'
            )
            parser.add_argument(
                'img_url',
                type=str,
                help='give me right url'
            )
            parser.add_argument(
                'description',
                type=str,
                default='default',
                help='give me right description'
            )
            parser.add_argument(
                'board',
                type=str,
                help='give me right board',
                default='default'
            )
            args = parser.parse_args()
            get_name = args['name']
            get_img_url = args['img_url']
            get_description = args['description']
            get_board = args['board']
            pin = model.Pin.create_pin(name=get_name, img_url=get_img_url, description=get_description, board=get_board)
            if pin is None:
                return make_response(jsonify({'Exception': 'Your board does not exist in our Board title list'}), 400)
            return make_response(jsonify(pin), 200)
        except Exception as e:
            return make_response(jsonify({'Exception': str(e)}), 409)

    # R 주어진 name을 가진 Pin을 가져오기
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(
                'name',
                type=str,
                required=True,
                nullable=False,
                help='give me right name'
            )
            args = parser.parse_args()
            get_name = args['name']
            pin = model.Pin.select_pin(name=get_name)
            if pin is None:
                return make_response({'Exception': 'Your name does not exist in our Pin name list'}, 400)
            return make_response(jsonify(pin), 200)
        except Exception as e:
            return make_response(jsonify({'Exception': str(e)}), 409)

    # U 주어진 name을 가진 Pin을 업데이트
    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(
                'name',
                type=str,
                required=True,
                nullable=False,
                help='give me right name'
            )
            parser.add_argument(
                'img_url',
                type=str,
                required=False,
                default='default',
                help='give me right url'
            )
            parser.add_argument(
                'description',
                type=str,
                required=False,
                default='default',
                help='give me right url'
            )
            args = parser.parse_args()
            get_name = args['name']
            get_img_url = args['img_url']
            get_description = args['description']
            pin = model.Pin.update_pin(name=get_name, img_url=get_img_url, description=get_description)
            if pin is None:
                return make_response(jsonify({'Exception': 'Your name does not exist in our Pin name list'}), 400)
            return make_response(jsonify(pin), 200)
        except Exception as e:
            return make_response(jsonify({'Exception': str(e)}), 409)

    # D 주어진 name을 가진 Pin을 삭제
    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(
                'name',
                type=str,
                required=True,
                nullable=False,
                help='give me right name'
            )
            args = parser.parse_args()
            get_name = args['name']
            pin = model.Pin.delete_pin(name=get_name)
            if pin is None:
                return make_response(jsonify({'Exception': 'Your name does not exist in our Pin name list'}), 400)
            return make_response(jsonify(pin), status=200)
        except Exception as e:
            return make_response(jsonify({'Exception': str(e)}), status=409)


# /pin/list
class PinList(Resource):
    # 모든 Pin들을 가져오기
    def post(self):
        try:
            pin_list = model.Pin.select_pin_list()
            return make_response(jsonify(pin_list), 200)
        except Exception as e:
            return make_response(jsonify({'Exception': str(e)}), 409)


# /board
class Board(Resource):
    # C 입력한 정보로 새 Board를 만들어 DB 안에 삽입
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(
                'title',
                type=str,
                required=True,
                nullable=False,
                default='default',
                help='No title provided'
            )
            parser.add_argument(
                'comment',
                type=str,
                default='',
                help='No comment provided'
            )
            args = parser.parse_args()
            get_title = args['title']
            get_comment = args['comment']
            board = model.Board.create_board(title=get_title, comment=get_comment)
            return make_response(jsonify(board), 00)
        except Exception as e:
            return make_response(jsonify({'Exception': str(e)}), 409)

    # R 주어진 title을 가진 Board를 가져오기
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(
                'title',
                type=str,
                required=True,
                nullable=False,
                help='No title provided'
            )
            args = parser.parse_args()
            get_title = args['title']
            board = model.Board.select_board(title=get_title)
            if board is None:
                return make_response(jsonify({'Exception': 'Your title does not exist in our Board title list'}), 400)
            return make_response(jsonify(board), 200)
        except Exception as e:
            return make_response(jsonify({'Exception': str(e)}), 409)

    # U 주어진 title을 가진 Board를 업데이트
    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(
                'title',
                type=str,
                required=True,
                nullable=False,
                default='default',
                help='No title provided'
            )
            parser.add_argument(
                'comment',
                type=str,
                default='',
                help='No comment provided'
            )
            args = parser.parse_args()
            get_title = args['title']
            get_comment = args['comment']
            board = model.Board.update_board(title=get_title, comment=get_comment)
            if board is None:
                return make_response(jsonify({'Exception': 'Your title does not exist in our Board title list'}), 400)
            return make_response(jsonify(board), 200)
        except Exception as e:
            return make_response(jsonify({'Exception': str(e)}), 409)

    # D 주어진 name을 가진 Board를 삭제
    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(
                'title',
                type=str,
                required=True,
                nullable=False,
                default='default',
                help='No title provided'
            )
            args = parser.parse_args()
            get_title = args['title']
            board = model.Board.delete_board(title=get_title)
            if board is None:
                return make_response(jsonify({'Exception': 'Your title does not exist in our Board title list'}), 400)
            return make_response(jsonify(board), 200)
        except Exception as e:
            return make_response(jsonify({'Exception': str(e)}), 409)


# /board/list
class BoardList(Resource):
    # 모든 Board들을 가져오기
    def post(self):
        try:
            board_list = model.Board.select_board_list()
            return make_response(jsonify(board_list), 200)
        except Exception as e:
            return make_response(jsonify({'Exception': str(e)}), 409)