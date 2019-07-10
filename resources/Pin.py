from flask import request
from flask_restful import Resource
from models.Pin import Pin as PinModel

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
            pin = PinModel.create_pin(name=get_name, img_url=get_img_url, description=get_description, board=get_board)
            if pin is None:
                return {'Exception': 'Your board does not exist in our Board title list'}, 400
            return pin, 200
        except Exception as e:
            return {'Exception': str(e)}, 409

    # R 주어진 name을 가진 Pin을 가져오기
    def get(self):
        try:
            get_name = request.args.get('name', None)
            pin = PinModel.select_pin(name=get_name)
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
            pin = PinModel.update_pin(name=get_name, img_url=get_img_url, description=get_description, board=get_board)
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
            pin = PinModel.delete_pin(name=get_name)
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
            pin_list = PinModel.select_pin_list()
            return pin_list, 200
        except Exception as e:
            return {'Exception': str(e)}, 409