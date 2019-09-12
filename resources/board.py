from flask import request, abort
from flask_restful import Resource
from models.board import Board as BoardModel
from peewee import IntegrityError


class BoardResource(Resource):
    """
    Board 테이블의 모든 정보에 접근합니다.
    """
    def get(self):
        """
        DB 안의 모든 Board 정보들을 조회
        :return: Board 정보들
        """
        board_list = BoardModel.select_board_list()
        return board_list, 200

    def post(self):
        """
        입력한 정보로 새 Board를 만들어 DB 안에 삽입
        :return:
        """
        data = request.json()
        status_code = 201

        if isinstance(data, list):
            # [] 형태로 여러 개의 Board Data를 전송할 때, 한꺼번에 POST가 가능하도록 처리
            response_payload = []
            for input_board_data in data:
                output_board_data = BoardModel.create_board(**input_board_data)
                if output_board_data.get('Exception'):
                    status_code = 400
                response_payload.append(output_board_data)
        else:
            try:
                response_payload= BoardModel.create_board(**data)
            except KeyError:
                return {'Exception': "You should give us required data"}, 400

            if response_payload.get('Exception'):
                status_code = 400

        return response_payload, status_code


class BoardItemResource(Resource):
    """
    Board 테이블의 정보에 CRUD 형식으로 접근합니다.
    """
    def post(self, title):
        """
        입력한 정보로 새 Board를 만들어 DB 안에 삽입
        :return:
        """
        comment = request.args.get('comment', title)
        try:
            board = BoardModel.create_board(title=title, comment=comment)
        except IntegrityError:
            abort(400, 'This title already exists in our list')

        if board.get('Exception'):
            abort(400, board['Exception'])
        return board, 201

    def get(self, title):
        """
        주어진 title을 가진 Board의 정보를 반환
        :return:
        """
        board = BoardModel.select_board(title=title)

        if board.get('Exception'):
            abort(400, board['Exception'])
        return board, 200

    def patch(self, title):
        """
        입력한 정보로 주어진 title을 가진 Board를 업데이트
        :return:
        """
        comment = request.args.get('comment', title)
        alter_title = request.args.get('title', title)

        board = BoardModel.update_board(title=title, alter_title=alter_title, comment=comment)

        if board.get('Exception'):
            abort(400, board['Exception'])
        return board, 200

    # D
    def delete(self, title):
        """
        입력한 title의 Board 정보를 삭제
        :return:
        """
        if title == 'default':
            return {'Exception': 'You cannot delete default board'}, 405

        board = BoardModel.delete_board(title=title)

        if board.get('Exception'):
            abort(400, board['Exception'])
        return board, 200

