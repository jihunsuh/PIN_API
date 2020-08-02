from flask import request, abort
from flask_restful import Resource
from models.board import BoardModel
from sqlalchemy import exc


class BoardItemResource(Resource):
    # GET /boards/<id>
    def get(self, id):
        try:
            board = BoardModel.findOne(id=id)
            if board is None:
                raise Exception("Board not found")
            return {"data": board.json()}, 200
        except Exception as e:
            return {'Exception': str(e)}, 500

    # PUT /boards/<id>
    def put(self, id):
        try:
            body = request.json

            board = BoardModel.findOne(id=id)
            if board is None:
                raise Exception("Board not found")

            board.update(**body)

            return {'message': "successfully updated"}, 200
        except Exception as e:
            return {'Exception': str(e)}, 500

    # DELETE /boards/<id>
    def delete(self, id):
        try:
            board = BoardModel.findOne(id=id)
            if board is None:
                raise Exception("Board not found")

            board.delete()

            return {'message': "successfully deleted"}, 200
        except exc.IntegrityError:
            return {'Exception': "There are connected Pins in this board"}
        except Exception as e:
            return {'Exception': str(e)}, 500


class BoardListResource(Resource):
    # GET /boards
    def get(self):
        try:
            boards = BoardModel.findAll()

            def getJson(model):
                return model.json()

            return {"data": list(map(getJson, boards))}, 200
        except Exception as e:
            return {'Exception': str(e)}, 500

    # POST /boards
    def post(self):
        try:
            body = request.json
            board = BoardModel(**body)
            board.create()

            return {'message': "successfully created"}, 200
        except Exception as e:
            return {'Exception': str(e)}, 500


class BoardBulkResource(Resource):
    # POST /boards/bulk
    def post(self):
        try:
            body = request.json

            if not isinstance(body, list):
                raise Exception("request body is not list type data")

            BoardModel.create_bulk(body)

            return {'message': "successfully created"}, 200
        except Exception as e:
            return {'Exception': str(e)}, 500
