# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from flask import jsonify, make_response, g, request
from auth import basic_auth
from model import Pin, Board
from userlogic import User


# /hello Server 작동 확인
class HelloApi(Resource):
    def get(self):
        try:
            return {'name': request.args.get('name', '')}, 200
        except Exception as e:
            return {'Exception': str(e)}, 409

    def post(self):
        return {'message': 'hello, World!'}, 200


# /token token 기반 인증 확인
class AuthAndTokenApi(Resource):
    @basic_auth.login_required
    def get(self):
        token = g.user.generate_auth_token()
        return {'token': token.decode('ascii')}, 200

    @basic_auth.login_required
    def post(self):
        return {'data': 'Hello, %s!' % g.user.id}, 200


# /user
class UserApi(Resource):
    # 입력한 정보로 유저 생성
    def post(self):
        try:
            get_id = request.args.get('id', None)
            get_email = request.args.get('email', 'default')
            get_password = request.args.get('password', None)
            if get_id is None or get_password is None:
                return {'Exception': 'You should give us id and password'}, 400
            user = User.create_user(id=get_id, email=get_email, password=get_password)
            User.generate_auth_token(User.get(id=get_id))
            return user, 201
        except Exception as e:
            return {'Exception': str(e)}, 409

    def get(self):
        try:
            get_id = request.args.get('id', None)
            get_password = request.args.get('password', None)
            if get_id is None or get_password is None:
                return {'Exception': 'You should give us id and password'}, 400
            user = User.select_user(id=get_id, password=get_password)
            return user, 200
        except Exception as e:
            return {'Exception': str(e)}, 409


# /pin
class PinApi(Resource):
    # C 입력한 정보로 새 Pin을 만들어 DB 안에 삽입
    def post(self):
        try:
            get_name = request.args.get('name', None)
            get_img_url = request.args.get('img_url', None)
            get_description = request.args.get('description', 'default')
            get_board = request.args.get('board', 'default')
            if get_name is None or get_img_url is None:
                return {'Exception': 'You should give us name and img_url'}, 400
            pin = Pin.create_pin(name=get_name, img_url=get_img_url, description=get_description, board=get_board)
            if pin is None:
                return {'Exception': 'Your board does not exist in our Board title list'}, 400
            return pin, 200
        except Exception as e:
            return {'Exception': str(e)}, 409

    # R 주어진 name을 가진 Pin을 가져오기
    def get(self):
        try:
            get_name = request.args.get('name', None)
            pin = Pin.select_pin(name=get_name)
            if pin is None:
                return {'Exception': 'Your name does not exist in our Pin name list'}, 400
            return pin, 200
        except Exception as e:
            return {'Exception': str(e)}, 409

    # U 주어진 name을 가진 Pin을 업데이트
    def put(self):
        try:
            get_name = request.args.get('name', None)
            get_img_url = request.args.get('img_url', None)
            get_description = request.args.get('description', 'default')
            get_board = request.args.get('board', 'default')
            if get_name is None or get_img_url is None:
                return {'Exception': 'You should give us name or img_url'}, 400
            pin = Pin.update_pin(name=get_name, img_url=get_img_url, description=get_description, board=get_board)
            if pin == 0:
                pin = {'Exception': 'Your board does not exist in our Board title list'}
            elif pin == 1:
                pin = {'Exception': 'Your name does not exist in our Pin name list'}
            return pin, 200
        except Exception as e:
            return {'Exception': str(e)}, 409

    # D 주어진 name을 가진 Pin을 삭제
    def delete(self):
        try:
            get_name = request.args.get('name', None)
            pin = Pin.delete_pin(name=get_name)
            if pin is None:
                return {'Exception': 'Your name does not exist in our Pin name list'}, 400
            return pin, 200
        except Exception as e:
            return {'Exception': str(e)}, 409


# /pin/list
class PinListApi(Resource):
    # 모든 Pin들을 가져오기
    def get(self):
        try:
            pin_list = Pin.select_pin_list()
            return pin_list, 200
        except Exception as e:
            return {'Exception': str(e)}, 409


# /board
class BoardApi(Resource):
    # C 입력한 정보로 새 Board를 만들어 DB 안에 삽입
    def post(self):
        try:
            get_title = request.args.get('title', None)
            get_comment = request.args.get('comment', None)
            if get_title is None or get_comment is None:
                return {'Exception': 'You should give us title and comment'}, 400
            board = Board.create_board(title=get_title, comment=get_comment)
            return board, 200
        except Exception as e:
            return {'Exception': str(e)}, 409

    # R 주어진 title을 가진 Board를 가져오기
    def get(self):
        try:
            get_title = request.args.get('title', None)
            board = Board.select_board(title=get_title)
            if board is None:
                return {'Exception': 'Your title does not exist in our Board title list'}, 400
            return board, 200
        except Exception as e:
            return {'Exception': str(e)}, 409

    # U 주어진 title을 가진 Board를 업데이트
    def put(self):
        try:
            get_title = request.args.get('title', None)
            get_comment = request.args.get('comment', None)
            if get_title is None or get_comment is None:
                return {'Exception': 'You should give us title and comment'}, 400
            board = Board.update_board(title=get_title, comment=get_comment)
            if board is None:
                return {'Exception': 'Your title does not exist in our Board title list'}, 400
            return board, 200
        except Exception as e:
            return {'Exception': str(e)}, 409

    # D 주어진 name을 가진 Board를 삭제
    def delete(self):
        try:
            get_title = request.args.get('title', None)
            board = Board.delete_board(title=get_title)
            if board == 0:
                return {'Exception': 'Your title does not exist in our Board title list'}, 400
            elif board == 1:
                return {'Exception': 'You cannot delete default board'}, 400
            return board, 200
        except Exception as e:
            return {'Exception': str(e)}, 409


# /board/list
class BoardListApi(Resource):
    # 모든 Board들을 가져오기
    def get(self):
        try:
            board_list = Board.select_board_list()
            return board_list, 200
        except Exception as e:
            return {'Exception': str(e)}, 409
