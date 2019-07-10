from flask import request
from flask_restful import Resource
from models.Board import Board as BoardModel

# /board
class BoardApi(Resource):
    # C 입력한 정보로 새 Board를 만들어 DB 안에 삽입
    def post(self):
        try:
            get_title = request.args.get('title', None)
            get_comment = request.args.get('comment', None)
            if get_title is None or get_comment is None:
                return {'Exception': 'You should give us title and comment'}, 400
            board = BoardModel.create_board(title=get_title, comment=get_comment)
            return board, 200
        except Exception as e:
            return {'Exception': str(e)}, 409

    # R 주어진 title을 가진 Board를 가져오기
    def get(self):
        try:
            get_title = request.args.get('title', None)
            board = BoardModel.select_board(title=get_title)
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
            board = BoardModel.delete_board(title=get_title)
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
            board_list = BoardModel.select_board_list()
            return board_list, 200
        except Exception as e:
            return {'Exception': str(e)}, 409
