from flask import request, abort
from flask_restful import Resource
from models.pin import PinModel
from sqlalchemy import exc
from flask_jwt import jwt_required


def validate_body(body):
    try:
        img_url = body['img_url']
        description = body['description']
        board_id = body['board_id']
    except KeyError:
        raise Exception("Request data is wrong!")
    return {'img_url': img_url, 'description': description, 'board_id': board_id}


class PinItemResource(Resource):
    # GET /pins/<id>
    def get(self, id):
        try:
            pin = PinModel.findOne(id=id)

            if pin is None:
                raise Exception("Pin not found")

            return {"data": pin.json()}, 200
        except Exception as e:
            return {'Exception': str(e)}, 500

    # PUT /pins/<id>
    @jwt_required()
    def put(self, id):
        try:
            body = request.json

            pin = PinModel.findOne(id=id)
            if pin is None:
                raise Exception("Pin not found")

            pin.update(**body)

            return {'message': "successfully updated"}, 200
        except exc.IntegrityError:
            return {'Exception': "Unknown board_id in your body"}
        except Exception as e:
            return {'Exception': str(e)}, 500

    # DELETE /pins/<id>
    @jwt_required()
    def delete(self, id):
        try:
            pin = PinModel.findOne(id=id)
            if pin is None:
                raise Exception("Pin not found")

            pin.delete()

            return {'message': "successfully deleted"}, 200
        except Exception as e:
            return {'Exception': str(e)}, 500


class PinListResource(Resource):
    # GET /pins
    def get(self):
        try:
            pins = PinModel.findAll()

            def getJson(model):
                return model.json()

            return {"data": list(map(getJson, pins))}, 200
        except Exception as e:
            return {'Exception': str(e)}, 500

    # POST /pins
    @jwt_required()
    def post(self):
        try:
            body = request.json
            body = validate_body(body)
            pin = PinModel(**body)
            pin.create()

            return {'message': "successfully created"}, 200
        except exc.IntegrityError:
            return {'Exception': "Unknown board_id in your body"}
        except Exception as e:
            return {'Exception': str(e)}, 500


class PinBulkResource(Resource):
    # POST /pins/bulk
    @jwt_required()
    def post(self):
        try:
            body = request.json

            if not isinstance(body, list):
                raise Exception("request body is not list type data")

            body = map(validate_body, body)

            PinModel.create_bulk(body)

            return {'message': "successfully created"}, 200
        except Exception as e:
            return {'Exception': str(e)}, 500
