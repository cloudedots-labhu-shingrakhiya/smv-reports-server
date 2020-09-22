from datetime import datetime
from helper.db import get_connection
from helper.response import JSONEncoder, Response as Res
from middlewares.query import getLimit
from bson.objectid import ObjectId
import json


async def usersReports():
    try:
        conn = await get_connection()
        allUser = json.loads(json.dumps(
            list(conn.users.find({'status': 'active'},
                                 {'firstName': 1, 'lastName': 1, 'email': 1, 'contact': 1, 'address': 1, 'avatar': 1})), cls=JSONEncoder))
        return allUser
    except Exception as error:
        print('Error in Users reports ', error)
        return Res(500).errorRes()


async def userReport(id):
    try:
        conn = await get_connection()
        pipeline = [
            {
                '$match': {
                    'status': 'active',
                    '_id': ObjectId(id)
                }},
            {
                '$project': {
                    'firstName': 1,
                    'lastName': 1,
                    'email': 1,
                    'contact': 1,
                    'address': 1,
                    'avatar': 1
                }}
        ]
        user = json.loads(json.dumps(
            list(conn.users.aggregate(pipeline)), cls=JSONEncoder))
        return user
    except Exception as error:
        print('Error in User report ', id, error)
        return Res(500).errorRes()


async def salesReports(queryObj):
    try:
        limit = getLimit(queryObj)
        print('limit.....', type(limit))
        conn = await get_connection()
        pipeline = [
            {
                '$match': {
                    'status': 'active'
                }}
        ]

        # if startDate and endDate:
        #     pipeline[0]['$match']['createdAt'] = {
        #         '$gte': startDate,
        #         '$lte': endDate
        #     }
        # elif startDate and not endDate:
        #     pipeline[0]['$match']['createdAt'] = {
        #         '$gte': startDate
        #     }
        # elif not startDate and endDate:
        #     pipeline[0]['$match']['createdAt'] = {
        #         '$lte': endDate
        #     }
        print('pipeline..',  pipeline)
        allSales = json.loads(json.dumps(
            list(conn.sales.aggregate(pipeline)), cls=JSONEncoder))

        return allSales
    except Exception as error:
        print('Error in Sales reports ', error)
        return Res(500).errorRes()
