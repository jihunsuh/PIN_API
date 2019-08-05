from peewee import Model, CharField, ForeignKeyField, TextField, DateTimeField, IntegrityError
import datetime
from . import DB
from .board import Board as BoardModel


# Pin 모델 정의
class Pin(Model):
    name = CharField(max_length=20, primary_key=True)
    # 외래 키 정의
    board = ForeignKeyField(BoardModel, backref='board')
    img_url = CharField(unique=True)
    description = TextField(default="")
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = DB

    # C create pin
    @classmethod
    def create_pin(cls, name, img_url, description, board):
        try:
            # 입력된 board가 DB 안의 board 안에 있는지 확인
            if_board_exists = BoardModel.get(BoardModel.title == board)

            pin = cls.create(name=name, img_url=img_url, description=description, board=board)
            return {'message': 'pin created successfully'}
        except BoardModel.DoesNotExist:
            return {'Exception': 'Given board does not exist in our Board title list'}
        except IntegrityError:
            return {'Exception': 'This name already exists in our list'}

    # R read pin
    @classmethod
    def select_pin(cls, name):
        try:
            pin = cls().select().where(cls.name == name).get()
            return {'name': pin.name,
                    'img_url': pin.img_url,
                    'description': pin.description,
                    'board': title_confirm_board_null(pin)}
        except cls.DoesNotExist:
            return {'Exception': 'Given name does not exist in our Pin name list'}

    # U update pin
    @classmethod
    def update_pin(cls, name, alter_name, img_url, description, board):
        try:
            # 입력된 board가 존재하는지, 입력된 name을 가진 pin이 존재하는지 확인
            if_pin_exists = cls.get(cls.name == name)
            if_board_exists = BoardModel.get(BoardModel.title == board)

            # 만약 name을 변경할 예정인데, 변경할 name을 가진 pin이 이미 있다면 exception 리턴
            if name != alter_name and cls.check_exist_with_name(alter_name):
                return {'Exception': 'Given name already exists in our Pin name list'}

            pin = cls().update(name=alter_name, img_url=img_url, description=description, board=board).where(
                cls.name == name)
            pin.execute()
            return {'message': 'pin updated successfully'}
        except cls.DoesNotExist:
            return {'Exception': 'Given name does not exist in our Pin name list'}
        except BoardModel.DoesNotExist:
            return {'Exception': 'Given board does not exist in our Board title list'}

    # D delete pin
    @classmethod
    def delete_pin(cls, name):
        try:
            pin = cls().get(cls.name == name)
            pin.delete_instance()
            return {'message': 'pin deleted successfully'}
        except cls.DoesNotExist:
            return {'Exception': 'Given name does not exist in our Pin name list'}

    @classmethod
    def select_pin_list(cls):
        result = []
        for pin in cls.select():
            result.append({'name': pin.name,
                           'img_url': pin.img_url,
                           'description': pin.description,
                           'board': title_confirm_board_null(pin)})
        return result

    @classmethod
    def check_exist_with_name(cls, name):
        try:
            if_pin_exists = cls().get(cls.name == name)
            return True
        except cls.DoesNotExist:
            return False


# 원본 board의 삭제를 감지해 자동으로 Pin의 board를 default로 업데이트해주는 함수
def title_confirm_board_null(pin):
    try:
        title = pin.board.title
        return title
    except BoardModel.DoesNotExist:
        Pin.update(board='default').where(Pin.name == pin.name).execute()
        return 'default'