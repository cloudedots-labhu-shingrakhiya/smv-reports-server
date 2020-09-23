from datetime import datetime
from helper.db import get_connection
from helper.response import JSONEncoder, Response as Res
from helper.query import getSort, getSkip, getSearch, getLimit, getPage, getDate
from controllers.usersQuery import usersQuery
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

        dbQuery = await usersQuery(search, '', date, False, sort, skip, limit)

        allUser = json.loads(json.dumps(
            list(conn.users.aggregate(dbQuery)), cls=JSONEncoder))

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
        sort = getSort(queryObj)
        skip = getSkip(queryObj)
        search = getSearch(queryObj)
        limit = getLimit(queryObj)
        page = getPage(queryObj)
        date = getDate(queryObj)
        queryProject = {
            'salesOfficer.sessions': 0,
            'salesOfficer.password': 0,
        }
        conn = await get_connection()

        dbQuery = [
            {
                '$match': {
                    'status': 'active'
                }
            }, {
                '$lookup': {
                    'from': 'users',
                    'localField': 'salesOfficer',
                    'foreignField': '_id',
                    'as': 'salesOfficer'
                }
            },
            {
                '$unwind': '$salesOfficer'
            }, {
                '$project': queryProject
            }, {
                '$sort': sort
            },
            {
                '$skip': int(skip)
            },
            {
                '$limit':  int(limit)
            }
        ]

        allSales = json.loads(json.dumps(
            list(conn.sales.aggregate(dbQuery)), cls=JSONEncoder))

        return allSales
    except Exception as error:
        print('Error in Sales reports ', error)
        return Res(500).errorRes()
