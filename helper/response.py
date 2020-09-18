from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from datetime import datetime
import json


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


class Response:
    def __init__(self, data):
        self.data = data

    def successRes(self):
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder(
                {"status": "SUCCESS",
                 "data": self.data}))

    def errorRes(self):
        if self.data == 400:
            return JSONResponse(
                status_code=400,
                content=jsonable_encoder(
                    {"error": "Bad Request",
                     "errorCode": "BAD_REQUEST"}))
        elif self.data == 401:
            return JSONResponse(
                status_code=401,
                content=jsonable_encoder(
                    {"error": "Authorization Failed",
                     "errorCode": "NOT_AUTHORIZED"}))
        elif self.data == 404:
            return JSONResponse(
                status_code=404,
                content=jsonable_encoder(
                    {"error": "Not Found",
                     "errorCode": "NOT_FOUND"}))
        elif self.data == 500:
            return JSONResponse(
                status_code=500,
                content=jsonable_encoder(
                    {"error": "Server Error",
                     "errorCode": "SERVER_ERROR"}))
        elif self.data == 503:
            return JSONResponse(
                status_code=503,
                content=jsonable_encoder(
                    {"error": "Service Unavailable",
                     "errorCode": "SERVICE_UNAVAILABLE"}))

    def customRes(self, code, err, errCode):
        return JSONResponse(
            status_code=code,
            content=jsonable_encoder(
                {"error": err,
                 "errorCode": errCode}))
