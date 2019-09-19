from flask import request, abort
from flask_restful import Resource
from models.pin import Pin as PinModel
from models.board import Board as BoardModel


class PinResource(Resource):
    """
    name에 해당하는 Pin 정보를 조회
    name이 list일 경우 DB 안의 모든 Pin 정보들을 조회
    """

    def get(self):
        """
        DB 안의 모든 Pin 정보들을 조회
        :return:
        """
        pin_list = PinModel.select_pin_list()
        if not pin_list:
            abort(400, "There's no pin in here")
        return pin_list, 200

    def post(self):
        """
        입력한 정보로 새 Pin을 만들어 DB 안에 삽입
        :return:
        """
        data = request.json

        try:
            pin = PinModel.create_pin(**data)
        except KeyError:
            abort(400, "You should give us required data")

        return pin, 201


class PinListResource(Resource):
    """
    /pin-list
    Pin 테이블에 데이터 리스트를 넣습니다.
    """
    def post(self):
        """
        입력한 리스트들을 모두 Pin 테이블에 저장
        :return:
        """
        data = request.json

        if isinstance(data, list):
            # [] 형태로 여러 개의 Board Data를 전송할 때, 한꺼번에 POST가 가능하도록 처리
            response_payload = []
            for input_board_data in data:
                output_board_data = PinModel.create_pin(**input_board_data)
                response_payload.append(output_board_data)
        else:
            abort(400, "You should give us 'list' of data")

        return response_payload, 201


class PinItemResource(Resource):
    """
    Pin 테이블의 정보에 CRUD 형식으로 접근합니다.
    """

    def get(self, name):
        """
        주어진 name을 가진 Pin의 정보를 반환
        :return:
        """
        pin = PinModel.select_pin(name=name)
        return pin, 200

    def patch(self, name):
        """
        입력한 정보로 주어진 name을 가진 Pin을 업데이트
        :return:
        """
        try:
            data = request.json
            if data['name']:
                data['alter_name'] = data.pop('name')

            if not BoardModel.select_board(data['board']):
                abort(400, 'Given board does not exist in our Board title list')

            pin = PinModel.update_pin(name=name, **data)

        except KeyError:
            abort(400, 'You should give us required data')

        return pin, 200

    def delete(self, name):
        """
        입력한 name의 Pin 정보를 삭제
        :return:
        """
        pin = PinModel.delete_pin(name=name)
        return pin, 200

