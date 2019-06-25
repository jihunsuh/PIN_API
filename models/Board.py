from peewee import Model, CharField
import datetime
from flask_restful import Resource
from flask import request
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
            if title == 'default':
                return 1
            board.delete_instance()
            return {'status': 'success'}
        except cls.DoesNotExist:
            return 0

    @classmethod
    def select_board_list(cls):
        result = []
        for board in cls.select():
            result.append({'title': board.title,
                           'comment': board.comment,
                           'created_at': board.created_at})
        return result

# /board
class BoardApi(Resource):
    # C 입력한 정보로 새 Board를 만들어 DB 안에 삽입
    def post(self):
        try:
            get_title = request.args.get('title', None)
            get_comment = request.args.get('comment', None)
            if get_title is None or get_comment is None:
                return {'Exception': 'You should give us title and comment'}, 400
            board = Board.create_board(title=get_title, comment=get_comment)
            return board, 200
        except Exception as e:
            return {'Exception': str(e)}, 409

    # R 주어진 title을 가진 Board를 가져오기
    def get(self):
        try:
            get_title = request.args.get('title', None)
            board = Board.select_board(title=get_title)
            if board is None:
                return {'Exception': 'Your title does not exist in our Board title list'}, 400
            return board, 200
        except Exception as e:
            return {'Exception': str(e)}, 409

    # U 주어진 title을 가진 Board를 업데이트
    def put(self):
        try:
            get_title = request.args.get('title', None)
            get_comment = request.args.get('comment', None)
            if get_title is None or get_comment is None:
                return {'Exception': 'You should give us title and comment'}, 400
            board = Board.update_board(title=get_title, comment=get_comment)
            if board is None:
                return {'Exception': 'Your title does not exist in our Board title list'}, 400
            return board, 200
        except Exception as e:
            return {'Exception': str(e)}, 409

    # D 주어진 name을 가진 Board를 삭제
    def delete(self):
        try:
            get_title = request.args.get('title', None)
            board = Board.delete_board(title=get_title)
            if board == 0:
                return {'Exception': 'Your title does not exist in our Board title list'}, 400
            elif board == 1:
                return {'Exception': 'You cannot delete default board'}, 400
            return board, 200
        except Exception as e:
            return {'Exception': str(e)}, 409


# /board/list
class BoardListApi(Resource):
    # 모든 Board들을 가져오기
    def get(self):
        try:
            board_list = Board.select_board_list()
            return board_list, 200
        except Exception as e:
            return {'Exception': str(e)}, 409