from flask import request
from flask_restful import Resource
from models.Pin import Pin as PinModel
from models.Board import Board as BoardModel


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
            get_name = request.args['name']
            get_img_url = request.args['img_url']
            get_description = request.args['description']
            get_board = request.args['board']
        except KeyError:
            return {'Exception': 'You should give us name and img_url'}, 400

        if PinModel.select_pin(get_name):
            return {"Exception": 'This title already exists in our list'}, 400

        pin = PinModel.create_pin(name=get_name, img_url=get_img_url, description=get_description, board=get_board)

        if pin['Exception']:
            return pin, 400
        return pin, 200

    def get(self):
        """
        주어진 name을 가진 Pin의 정보를 반환
        :return:
        """
        try:
            get_name = request.args['name']
        except KeyError:
            return {'Exception': 'You should give us name'}, 400

        pin = PinModel.select_pin(name=get_name)

        if pin['Exception']:
            return pin, 400
        return pin, 200

    def put(self):
        """
        입력한 정보로 주어진 name을 가진 Pin을 업데이트
        :return:
        """
        try:
            get_name = request.args['name']
            get_img_url = request.args['img_url']
            get_description = request.args['description']
            get_board = request.args['board']
        except KeyError:
            return {'Exception': 'You should give us data'}, 400

        if not BoardModel.select_board(get_board):
            return {'Exception': 'Your board does not exist in our Board title list'}, 400

        pin = PinModel.update_pin(name=get_name, img_url=get_img_url, description=get_description, board=get_board)

        if pin['Exception']:
            return pin, 400
        return pin, 200

    def delete(self):
        """
        입력한 name의 Pin 정보를 삭제
        :return:
        """
        try:
            get_name = request.args['name']
        except KeyError:
            return {'Exception': 'You should give us name'}, 400

        pin = PinModel.delete_pin(name=get_name)

        if pin['Exception']:
            return pin, 400
        return pin, 200


# /pin/list
class PinListResource(Resource):
    """
    Pin 테이블의 모든 정보에 접근합니다.
    """
    # 모든 Pin들을 가져오기
    def get(self):
        """
        DB 안의 모든 Pin 정보들을 조회
        :return:
        """
        pin_list = PinModel.select_pin_list()
        return pin_list, 200
