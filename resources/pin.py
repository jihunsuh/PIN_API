from flask import request
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
        return pin_list, 200

    def post(self):
        """
        입력한 정보로 새 Pin을 만들어 DB 안에 삽입
        :return:
        """
        data = request.get_json()
        status_code = 201

        if isinstance(data, list):
            # [] 형태로 여러 개의 Pin Data를 전송할 때, 한꺼번에 POST가 가능하도록 처리
            pin = []
            for input_pin_data in data:
                output_pin_data = PinModel.create_pin(**input_pin_data)
                if output_pin_data.get('Exception'):
                    status_code = 400
                pin.append(output_pin_data)
        else:
            try:
                pin = PinModel.create_pin(**data)
            except KeyError:
                return {'Exception': "You should give us required data"}, 400

            if pin.get('Exception'):
                status_code = 400

        return pin, status_code


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

        if pin.get('Exception'):
            return pin, 400
        return pin, 200

    def patch(self, name):
        """
        입력한 정보로 주어진 name을 가진 Pin을 업데이트
        :return:
        """
        try:
            data = request.get_json()
            if data['name']:
                data['alter_name'] = data.pop('name')
        except KeyError:
            return {'Exception': 'You should give us data'}, 400

        if not BoardModel.select_board(data['board']):
            return {'Exception': 'Given board does not exist in our Board title list'}, 400

        pin = PinModel.update_pin(name=name, **data)

        if pin.get('Exception'):
            return pin, 400
        return pin, 200

    def delete(self, name):
        """
        입력한 name의 Pin 정보를 삭제
        :return:
        """
        pin = PinModel.delete_pin(name=name)

        if pin.get('Exception'):
            return pin, 400
        return pin, 200

