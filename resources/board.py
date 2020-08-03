from flask import request, abort
from flask_restful import Resource
from models.board import BoardModel
from sqlalchemy import exc
from flask_jwt import jwt_required


def validate_body(body):
    try:
        title = body['title']
        comment = body['comment']
    except KeyError:
        raise Exception("Request data is wrong!")
    return {'title': title, 'comment': comment}


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
    @jwt_required()
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
    @jwt_required()
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
    @jwt_required()
    def post(self):
        try:
            body = request.json
            body = validate_body(body)
            board = BoardModel(**body)
            board.create()

            return {'message': "successfully created"}, 200
        except Exception as e:
            return {'Exception': str(e)}, 500


class BoardBulkResource(Resource):
    # POST /boards/bulk
    @jwt_required()
    def post(self):
        try:
            body = request.json

            if not isinstance(body, list):
                raise Exception("request body is not list type data")

            body = map(validate_body, body)

            BoardModel.create_bulk(body)

            return {'message': "successfully created"}, 200
        except Exception as e:
            return {'Exception': str(e)}, 500
