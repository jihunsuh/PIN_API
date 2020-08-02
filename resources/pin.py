from flask import request, abort
from flask_restful import Resource
from models.pin import PinModel
from sqlalchemy import exc


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
            raise Exception(e)
            return {'Exception': str(e)}, 500

    # DELETE /pins/<id>
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
            raise Exception(e)
            return {'Exception': str(e)}, 500

    # POST /pins
    def post(self):
        try:
            body = request.json
            pin = PinModel(**body)
            pin.create()

            return {'message': "successfully created"}, 200
        except exc.IntegrityError:
            return {'Exception': "Unknown board_id in your body"}
        except Exception as e:
            return {'Exception': str(e)}, 500


class PinBulkResource(Resource):
    # POST /pins/bulk
    def post(self):
        try:
            body = request.json

            if not isinstance(body, list):
                raise Exception("request body is not list type data")

            PinModel.create_bulk(body)

            return {'message': "successfully created"}, 200
        except Exception as e:
            return {'Exception': str(e)}, 500
