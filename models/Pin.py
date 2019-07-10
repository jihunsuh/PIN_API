from peewee import Model, CharField, ForeignKeyField, TextField, DateTimeField
import datetime
from . import DB
from .Board import Board


# Pin 모델 정의
class Pin(Model):
    name = CharField(max_length=20, primary_key=True)
    # 외래 키 정의
    board = ForeignKeyField(Board, backref='board')
    img_url = CharField(unique=True)
    description = TextField(default="")
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = DB

    # C create pin
    @classmethod
    def create_pin(cls, name, img_url, description, board):
        # 입력된 board가 DB 안의 board 안에 있는지 확인
        try:
            if_board_exists = Board.select().where(Board.title == board).get()
            pin = cls.create(name=name, img_url=img_url, description=description, board=board)
            pin = pin.save()
            return {'save': pin}
        except Board.DoesNotExist:
            return None

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
            return None

    # U update pin
    @classmethod
    def update_pin(cls, name, img_url, description, board):
        # 입력된 board가 존재하는지, 입력된 name을 가진 pin이 존재하는지 확인
        try:
            if_board_exists = Board.select().where(Board.title == board).get()
            if_pin_exists = cls.get(cls.name == name)
        except Board.DoesNotExist:
            return 0
        except Pin.DoesNotExist:
            return 1
        else:
            # img_url의 입력값이 들어오지 않았을 때 img_url을 기존 값으로 설정
            if img_url == 'default' or img_url is None:
                img_url = cls.get(cls.name == name).img_url
            # description의 입력값이 들어오지 않았을 때 description을 기존 값으로 설정
            if description == 'default' or description is None:
                description = cls.get(cls.name == name).description
            pin = cls().update(img_url=img_url, description=description, board=board).where(cls.name == name)
            pin.execute()
            pin = cls.get(cls.name == name)
            return {'name': pin.name,
                    'img_url': pin.img_url,
                    'description': pin.description,
                    'board': title_confirm_board_null(pin)}

    # D delete pin
    @classmethod
    def delete_pin(cls, name):
        try:
            pin = cls().get(cls.name == name)
            pin.delete_instance()
            return {'status': 'success'}
        except cls.DoesNotExist:
            return None

    @classmethod
    def select_pin_list(cls):
        result = []
        for pin in cls.select():
            result.append({'name': pin.name,
                           'img_url': pin.img_url,
                           'description': pin.description,
                           'board': title_confirm_board_null(pin)})
        return result


# 원본 board의 삭제를 감지해 자동으로 Pin의 board를 default로 업데이트해주는 함수
def title_confirm_board_null(pin):
    try:
        title = pin.board.title
        return title
    except Exception as e:
        Pin.update(board='default').where(Pin.name == pin.name).execute()
        return 'default'
