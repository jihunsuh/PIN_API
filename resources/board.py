from flask import request, abort
from flask_restful import Resource
from models.board import Board as BoardModel


class BoardResource(Resource):
    """
    /board
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
        입력한 정보로 새 Board를 만들어 Board 테이블에 저장
        :return:
        """
        data = request.json

        try:
            response_payload = BoardModel.create_board(**data)
        except KeyError:
            abort(400, "You should give us required data")

        return response_payload, 201


class BoardListResource(Resource):
    """
    /board-list
    Board 테이블에 데이터 리스트를 넣습니다.
    """
    def post(self):
        """
        입력한 리스트들을 모두 Board 테이블에 저장
        :return:
        """
        data = request.json

        if isinstance(data, list):
            # [] 형태로 여러 개의 Board Data를 전송할 때, 한꺼번에 POST가 가능하도록 처리
            response_payload = []
            for input_board_data in data:
                output_board_data = BoardModel.create_board(**input_board_data)
                response_payload.append(output_board_data)
        else:
            abort(400, "You should give us 'list' of data")

        return response_payload, 201


class BoardItemResource(Resource):
    """
    /board/<item>
    Board 테이블의 정보에 CRUD 형식으로 접근합니다.
    """
    def get(self, title):
        """
        주어진 title을 가진 Board의 정보를 반환
        :return:
        """
        board = BoardModel.select_board(title=title)
        return board, 200

    def patch(self, title):
        """
        입력한 정보로 주어진 name을 가진 Pin을 업데이트
        :return:
        """
        try:
            data = request.json
            if data['title']:
                data['alter_title'] = data.pop('title')

            if not BoardModel.select_board(data['board']):
                abort(400, 'Given board does not exist in our Board title list')

            board = BoardModel.update_board(title=title, **data)

        except KeyError:
            abort(400, 'You should give us required data')

        return board, 200

    # D
    def delete(self, title):
        """
        입력한 title의 Board 정보를 삭제
        :return:
        """
        if title == 'default':
            abort(405, 'You cannot delete default board')

        board = BoardModel.delete_board(title=title)
        return board, 200

