from flask import request
from flask_restful import Resource
from models.board import Board as BoardModel


class BoardResource(Resource):
    """
    Board 테이블의 정보에 CRUD 형식으로 접근합니다.
    """
    def post(self, title):
        """
        입력한 정보로 새 Board를 만들어 DB 안에 삽입
        :return:
        """
        comment = request.args.get('comment', title)

        board = BoardModel.create_board(title=title, comment=comment)

        if board.get('Exception'):
            return board, 400
        return board, 201

    def get(self, title):
        """
        주어진 title을 가진 Board의 정보를 반환
        :return:
        """
        board = BoardModel.select_board(title=title)

        if board.get('Exception'):
            return board, 400
        return board, 200

    def put(self, title):
        """
        입력한 정보로 주어진 title을 가진 Board를 업데이트
        :return:
        """
        comment = request.args.get('comment', title)
        alter_title = request.args.get('title', title)

        board = BoardModel.update_board(title=title, alter_title=alter_title, comment=comment)

        if board.get('Exception'):
            return board, 400
        return board, 200

    # D
    def delete(self, title):
        """
        입력한 title의 Board 정보를 삭제
        :return:
        """
        if title == 'default':
            return {'Exception': 'You cannot delete default board'}, 400

        board = BoardModel.delete_board(title=title)

        if board.get('Exception'):
            return board, 400
        return board, 200


class BoardListResource(Resource):
    """
    Board 테이블의 모든 정보에 접근합니다.
    """
    def get(self, title):
        """
        DB 안의 모든 Board 정보들을 조회
        :return: Board 정보들
        """
        board_list = BoardModel.select_board_list()
        return board_list, 200
