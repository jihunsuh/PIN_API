from peewee import *
import datetime

DB = SqliteDatabase('test_peewee.db')


# 원본 board의 삭제를 감지해 자동으로 Pin의 board를 default로 업데이트해주는 함수
def title_confirm_board_null(pin):
    try:
        title = pin.board.title
    except Exception as e:
        Pin.update(board='default').where(Pin.name == pin.name).execute()
        return 'default'
    else:
        return title


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
            return {'exception': 'Your title does not exist in our Board title list'}

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
            return {'exception': 'Your title does not exist in our Board title list'}

    # D delete board
    @classmethod
    def delete_board(cls, title):
        try:
            board = cls().get(cls.title == title)
            board.delete_instance()
            return {'status': 'success'}
        except cls.DoesNotExist:
            return {'exception': 'Your title does not exist in our Board title list'}

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
        boardlist = Board.select()
        if 'default' not in [board.title for board in boardlist]:
            Board.create_board(title='default', comment='default')
        if board in [board.title for board in boardlist]:
            pin = cls.create(name=name, img_url=img_url, description=description, board=board)
            pin = pin.save()
            return {'save': pin}
        else:
            return {'Exception': 'Your title does not exist in our board list'}

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
            return {'exception': 'Your name does not exist in our Pin name list'}

    # U update pin
    @classmethod
    def update_pin(cls, name, img_url, description):
        # img_url의 입력값이 들어오지 않았을 때 img_url을 기존 값으로 설정
        if img_url == 'default':
            img_url = cls.get(cls.name == name).img_url
        # description의 입력값이 들어오지 않았을 때 description을 기존 값으로 설정
        if description == 'default':
            description = cls.get(cls.name == name).description

        try:
            pin = cls().update(img_url=img_url, description=description).where(cls.name == name)
            pin.execute()
            pin = cls.get(cls.name == name)
            return {'name': pin.name,
                    'img_url': pin.img_url,
                    'description': pin.description,
                    'board': title_confirm_board_null(pin)}
        except cls.DoesNotExist:
            return {'exception': 'Your name does not exist in our Pin name list'}

    # D delete pin
    @classmethod
    def delete_pin(cls, name):
        try:
            pin = cls().get(cls.name == name)
            pin.delete_instance()
            return {'status': 'success'}
        except cls.DoesNotExist:
            return {'exception': 'Your name does not exist in our Pin name list'}

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
    DB.close()
