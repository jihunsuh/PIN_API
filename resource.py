from flask_restful import Resource, reqparse
from flask import jsonify, make_response, g, request
from auth import basic_auth
import auth
import model


# /hello Server 작동 확인
class Hello(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', required=True, type=str, help='give us right name')
            args = parser.parse_args()
            return make_response(jsonify({'name': args['name']}), 200)
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
            args = request.args.to_dict()
            get_id = args.get('id', None)
            get_email = args.get('email', 'default')
            get_password = args['password']
            if get_id is None or get_password is None:
                return make_response(jsonify({'Exception': 'You should give us id and password'}), 400)
            user = model.User.create_user(id=get_id, email=get_email, password=get_password)
            model.User.generate_auth_token(user)
            return make_response(jsonify(user), 201)
        except Exception as e:
            return make_response(jsonify({'Exception': str(e)}), 409)

    def get(self):
        try:
            args = request.args.to_dict()
            get_id = args.get('id', default=None)
            get_password = args('password', default=None)
            if get_id is None or get_password is None:
                return make_response(jsonify({'Exception': 'You should give us id and password'}), 400)
            user = model.User.select_user(id=get_id, password=get_password)
            return make_response(jsonify(user), 200)
        except Exception as e:
            return make_response(jsonify({'Exception': str(e)}), 409)


# /pin
class Pin(Resource):
    # C 입력한 정보로 새 Pin을 만들어 DB 안에 삽입
    def post(self):
        try:
            args = request.args.to_dict()
            get_name = args.get('name', None)
            get_img_url = args.get('img_url', None)
            get_description = args.get('description', 'default')
            get_board = args.get('board', 'default')
            if get_name is None or get_img_url is None:
                return make_response(jsonify({'Exception': 'You should give us name and img_url'}), 400)
            pin = model.Pin.create_pin(name=get_name, img_url=get_img_url, description=get_description, board=get_board)
            if pin is None:
                return make_response(jsonify({'Exception': 'Your board does not exist in our Board title list'}), 400)
            return make_response(jsonify(pin), 200)
        except Exception as e:
            return make_response(jsonify({'Exception': str(e)}), 409)

    # R 주어진 name을 가진 Pin을 가져오기
    def get(self):
        try:
            args = request.args.to_dict()
            get_name = args.get('name', None)
            pin = model.Pin.select_pin(name=get_name)
            if pin is None:
                return make_response(jsonify({'Exception': 'Your name does not exist in our Pin name list'}), 400)
            return make_response(jsonify(pin), 200)
        except Exception as e:
            return make_response(jsonify({'Exception': str(e)}), 409)

    # U 주어진 name을 가진 Pin을 업데이트
    def put(self):
        try:
            args = request.args.to_dict()
            get_name = args.get('name', None)
            get_img_url = args.get('img_url', None)
            get_description = args.get('description', 'default')
            get_board = args.get('board', 'default')
            if get_name is None or get_img_url is None:
                return make_response(jsonify({'Exception': 'You should give us name or img_url'}), 400)
            pin = model.Pin.update_pin(name=get_name, img_url=get_img_url, description=get_description, board=get_board)
            if pin == 0:
                pin = {'Exception': 'Your board does not exist in our Board title list'}
            elif pin == 1:
                pin = {'Exception': 'Your name does not exist in our Pin name list'}
            return make_response(jsonify(pin), 200)
        except Exception as e:
            return make_response(jsonify({'Exception': str(e)}), 409)

    # D 주어진 name을 가진 Pin을 삭제
    def delete(self):
        try:
            args = request.args.to_dict()
            get_name = args.get('name', None)
            pin = model.Pin.delete_pin(name=get_name)
            if pin is None:
                return make_response(jsonify({'Exception': 'Your name does not exist in our Pin name list'}), 400)
            return make_response(jsonify(pin), 200)
        except Exception as e:
            return make_response(jsonify({'Exception': str(e)}), 409)


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
            args = request.args.to_dict()
            get_title = args.get('title', None)
            get_comment = args.get('comment', None)
            if get_title is None or get_comment is None:
                return make_response(jsonify({'Exception': 'You should give us title and comment'}), 400)
            board = model.Board.create_board(title=get_title, comment=get_comment)
            return make_response(jsonify(board), 200)
        except Exception as e:
            return make_response(jsonify({'Exception': str(e)}), 409)

    # R 주어진 title을 가진 Board를 가져오기
    def get(self):
        try:
            args = request.args.to_dict()
            get_title = args.get('title', None)
            board = model.Board.select_board(title=get_title)
            if board is None:
                return make_response(jsonify({'Exception': 'Your title does not exist in our Board title list'}), 400)
            return make_response(jsonify(board), 200)
        except Exception as e:
            return make_response(jsonify({'Exception': str(e)}), 409)

    # U 주어진 title을 가진 Board를 업데이트
    def put(self):
        try:
            args = request.args.to_dict()
            get_title = args.get('title', None)
            get_comment = args.get('comment', None)
            if get_title is None or get_comment is None:
                return make_response(jsonify({'Exception': 'You should give us title and comment'}), 400)
            board = model.Board.update_board(title=get_title, comment=get_comment)
            if board is None:
                return make_response(jsonify({'Exception': 'Your title does not exist in our Board title list'}), 400)
            return make_response(jsonify(board), 200)
        except Exception as e:
            return make_response(jsonify({'Exception': str(e)}), 409)

    # D 주어진 name을 가진 Board를 삭제
    def delete(self):
        try:
            args = request.args.to_dict()
            get_title = args.get('title', None)
            board = model.Board.delete_board(title=get_title)
            if board == 0:
                return make_response(jsonify({'Exception': 'Your title does not exist in our Board title list'}), 400)
            elif board == 1:
                return make_response(jsonify({'Exception': 'You cannot delete default board'}), 400)
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