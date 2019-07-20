import datetime
from peewee import Model, CharField

from . import DB


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
        if board == 1:
            return {'message': 'board created successfully'}
        else:
            return {'message': 'failed to create board'}

    # R read board
    @classmethod
    def select_board(cls, title):
        try:
            board = cls().select().where(cls.title == title).get()
            return {'title': board.title,
                    'comment': board.comment,
                    'created_at': board.created_at}
        except cls.DoesNotExist:
            return {'Exception': 'Your title does not exist in our Board title list'}

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
            return {'Exception': 'Your title does not exist in our Board title list'}

    # D delete board
    @classmethod
    def delete_board(cls, title):
        try:
            board = cls().get(cls.title == title)
            board.delete_instance()
            return {'status': 'success'}
        except cls.DoesNotExist:
            return {'Exception': 'Your title does not exist in our Board title list'}

    @classmethod
    def select_board_list(cls):
        result = []
        for board in cls.select():
            result.append({'title': board.title,
                           'comment': board.comment,
                           'created_at': board.created_at})
        return result
