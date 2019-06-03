from peewee import *
import pymysql.cursors
from userlogic import User
import datetime

DB = SqliteDatabase('test_peewee.db')
# connection = pymysql.connect(host='127.0.0.1',
#                              user='root',
#                              password='root',
#                              db='test_mysql',
#                              charset='UTF-8',
#                              cursorclass=pymysql.cursors.DictCursor)

# 원본 board의 삭제를 감지해 자동으로 Pin의 board를 default로 업데이트해주는 함수
def title_confirm_board_null(pin):
    try:
        title = pin.board.title
    except Exception as e:
        Pin.update(board='default').where(Pin.name == pin.name).execute()
        return 'default'
    else:
        return title

# DB에 접속할 때 default Board를 자동으로 생성해주는 함수
def create_default():
    try:
        get_Board = Board.select().where(Board.title=='default').get()
    except Board.DoesNotExist:
        Board.create_board('default', 'default')
        return None
    else:
        return None


# Pin을 모아두는 Board 모델 정의
class Board(Model):
    title = CharField(max_length=20, primary_key=True)
    comment = CharField(max_length=200)
    created_at = CharField(default=str(datetime.datetime.now()))

    class Meta:
        database = DB

    # C create board
    @classmethod
    def create_board(cls, title, comment):
        board = cls.create(title=title, comment=comment)
        board = board.save()
        return {'save': board}
    
    # R read board
    @classmethod
    def select_board(cls, title):
        try:
            board = cls().select().where(cls.title == title).get()
            return {'title': board.title,
                    'comment': board.comment,
                    'created_at': board.created_at}
        except cls.DoesNotExist:
            return None

    # U update board
    @classmethod
    def update_board(cls, title, comment):
        try:
            board = cls().update(comment=comment).where(cls.title == title)
            board.execute()
            update_result = cls().get(cls.title == title)
            return {'name': update_result.title,
                    'comment': update_result.comment,
                    'created_at': update_result.created_at}
        except cls.DoesNotExist:
            return None

    # D delete board
    @classmethod
    def delete_board(cls, title):
        try:
            board = cls().get(cls.title == title)
        except cls.DoesNotExist:
            return 0
        else:
            if title == 'default':
                return 1
            board.delete_instance()
            return {'status': 'success'}

    @classmethod
    def select_board_list(cls):
        result = []
        for board in cls.select():
            result.append({'title': board.title,
                           'comment': board.comment,
                           'created_at': board.created_at})
        return result


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
            get_board = Board.select().where(Board.title == board).get()
        except Board.DoesNotExist:
            return None
        else:
            pin = cls.create(name=name, img_url=img_url, description=description, board=board)
            pin = pin.save()
            return {'save': pin}

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
            get_board = Board.select().where(Board.title == board).get()
            get_pin = Pin.get(cls.name == name)
        except Board.DoesNotExist:
            return 0
        except Pin.DoesNotExist:
            return 1
        else:
            # img_url의 입력값이 들어오지 않았을 때 img_url을 기존 값으로 설정
            if img_url is None:
                img_url = cls.get(cls.name == name).img_url
            # description의 입력값이 들어오지 않았을 때 description을 기존 값으로 설정
            if description is None:
                description = cls.get(cls.name == name).description
            pin = cls().update(img_url=img_url, description=description, board=board).where(cls.name == name)
            pin.execute()
            pin = get_pin
            return {'name': pin.name,
                    'img_url': pin.img_url,
                    'description': pin.description,
                    'board': title_confirm_board_null(pin)}


    # D delete pin
    @classmethod
    def delete_pin(cls, name):
        try:
            pin = cls().get(cls.name == name)
        except cls.DoesNotExist:
            return None
        else:
            pin.delete_instance()
            return {'status': 'success'}

    @classmethod
    def select_pin_list(cls):
        result = []
        for pin in cls.select():
            result.append({'name': pin.name,
                           'img_url': pin.img_url,
                           'description': pin.description,
                           'board': title_confirm_board_null(pin)})
        return result


def initialize():
    DB.connect()
    DB.create_tables([User, Board, Pin], safe=True)
    create_default()
    DB.close()
