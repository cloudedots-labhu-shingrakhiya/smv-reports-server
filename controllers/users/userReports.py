from datetime import datetime
from helper.db import get_connection
from helper.response import JSONEncoder, Response as Res
from helper.query import getSort, getSkip, getSearch, getLimit, getPage, getDate
from controllers.users.usersQuery import usersQuery
from bson.objectid import ObjectId
import json


async def usersReports(queryObj):
    try:
        conn = await get_connection()

        sort = getSort(queryObj)
        skip = getSkip(queryObj)
        search = getSearch(queryObj)
        limit = getLimit(queryObj)
        date = getDate(queryObj)

        query = await usersQuery(search, '', date, False, sort, skip, limit)

        allUser = json.loads(json.dumps(
            list(conn.users.aggregate(query)), cls=JSONEncoder))

        return allUser
    except Exception as error:
        print('Error in usersReports function ', error)
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
                    'name': {'$concat': ['$firstName', ' ', '$lastName']},
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
        print('Error in userReport function ', id, error)
        return Res(500).errorRes()
