from flask import request
from flask_restful import Resource
from models.pin import Pin as PinModel
from models.board import Board as BoardModel


class PinResource(Resource):
    """
    Pin 테이블의 정보에 CRUD 형식으로 접근합니다.
    """
    def post(self):
        """
        입력한 정보로 새 Pin을 만들어 DB 안에 삽입
        :return:
        """
        try:
            name = request.args['name']
            img_url = request.args['img_url']
            description = request.args['description']
            board = request.args['board']
        except KeyError:
            return {'Exception': 'You should give us required value'}, 400

        pin = PinModel.create_pin(name=name, img_url=img_url, description=description, board=board)

        if pin.get('Exception'):
            return pin, 400
        return pin, 201

    def get(self):
        """
        주어진 name을 가진 Pin의 정보를 반환
        :return:
        """
        try:
            name = request.args['name']
        except KeyError:
            return {'Exception': 'You should give us name'}, 400

        pin = PinModel.select_pin(name=name)

        if pin.get('Exception'):
            return pin, 400
        return pin, 200

    def put(self):
        """
        입력한 정보로 주어진 name을 가진 Pin을 업데이트
        :return:
        """
        try:
            name = request.args['name']
            img_url = request.args['img_url']
            description = request.args['description']
            board = request.args['board']
        except KeyError:
            return {'Exception': 'You should give us data'}, 400

        if not BoardModel.select_board(board):
            return {'Exception': 'Your board does not exist in our Board title list'}, 400

        pin = PinModel.update_pin(name=name, img_url=img_url, description=description, board=board)

        if pin.get('Exception'):
            return pin, 400
        return pin, 200

    def delete(self):
        """
        입력한 name의 Pin 정보를 삭제
        :return:
        """
        try:
            name = request.args['name']
        except KeyError:
            return {'Exception': 'You should give us name'}, 400

        pin = PinModel.delete_pin(name=name)

        if pin.get('Exception'):
            return pin, 400
        return pin, 200


class PinListResource(Resource):
    """
    name에 해당하는 Pin 정보를 조회
    name이 list일 경우 DB 안의 모든 Pin 정보들을 조회
    """
    # 모든 Pin들을 가져오기
    def get(self, name):
        """
        DB 안의 모든 Pin 정보들을 조회
        :return:
        """
        if name == 'list':
            pin_list = PinModel.select_pin_list()
            return pin_list, 200

        pin = PinModel.select_pin(name=name)

        if pin.get('Exception'):
            return pin, 400
        return pin, 200
