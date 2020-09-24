from datetime import datetime
from helper.db import get_connection
from helper.response import JSONEncoder, Response as Res
from helper.query import getSort, getSkip, getSearch, getLimit, getPage, getDate
# from controllers.sacustomersles.customersQuery import customersQuery
from bson.objectid import ObjectId
import json


async def customersReports(queryObj):
    try:
        conn = await get_connection()

        sort = getSort(queryObj)
        skip = getSkip(queryObj)
        search = getSearch(queryObj)
        limit = getLimit(queryObj)
        date = getDate(queryObj)

        # query = await customersQuery(search, '', date, False, sort, skip, limit)
        query = [
            {
                '$match': {
                    'status': 'active'
                }
            }
        ]

        allSales = json.loads(json.dumps(
            list(conn.sales.aggregate(query)), cls=JSONEncoder))

        return allSales
    except Exception as error:
        print('Error in salesReports function ', error)
        return Res(500).errorRes()
