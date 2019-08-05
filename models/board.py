import datetime
from peewee import Model, CharField, IntegrityError, DateTimeField

from . import DB


# Pin을 모아두는 Board 모델 정의
class Board(Model):
    title = CharField(max_length=20, primary_key=True)
    comment = CharField(max_length=200)
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = DB

    # C create board
    @classmethod
    def create_board(cls, title, comment):
        try:
            board = cls.create(title=title, comment=comment)
            return {'message': 'board created successfully'}
        except IntegrityError:
            return {'Exception': 'This title already exists in our list'}

    # R read board
    @classmethod
    def select_board(cls, title):
        if cls.check_exist_with_title(title):
            board = cls().select().where(cls.title == title).get()
            return {'title': board.title,
                    'comment': board.comment,
                    'created_at': board.created_at}
        else:
            return {'Exception': 'Given title does not exist in our Board title list'}

    # U update board
    @classmethod
    def update_board(cls, title, alter_title, comment):
        if cls.check_exist_with_title(title):
            # 만약 title을 변경할 예정인데, 변경할 title을 가진 board가 이미 있다면 exception 리턴
            if title != alter_title and cls.check_exist_with_title(alter_title):
                return {'Exception': 'Given altered title already exists in our Board title list'}

            board = cls().update(title=alter_title, comment=comment).where(cls.title == title)
            board.execute()
            return {'message': 'pin updated successfully'}
        else:
            return {'Exception': 'Given title does not exist in our Board title list'}

    # D delete board
    @classmethod
    def delete_board(cls, title):
        try:
            board = cls().get(cls.title == title)
            board.delete_instance()
            return {'message': 'board deleted successfully'}
        except cls.DoesNotExist:
            return {'Exception': 'Given title does not exist in our Board title list'}

    @classmethod
    def select_board_list(cls):
        result = []
        for board in cls.select():
            result.append({'title': board.title,
                           'comment': board.comment,
                           'created_at': board.created_at})
        return result

    @classmethod
    def check_exist_with_title(cls, title):
        try:
            if_board_exists = cls().get(cls.title == title)
            return True
        except cls.DoesNotExist:
            return False
