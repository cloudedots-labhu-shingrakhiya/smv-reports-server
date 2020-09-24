from datetime import datetime
from helper.db import get_connection
from helper.response import JSONEncoder, Response as Res
from helper.query import getSort, getSkip, getSearch, getLimit, getPage, getDate
from controllers.sales.salesQuery import salesQuery
from bson.objectid import ObjectId
import json


async def salesReports(queryObj):
    try:
        conn = await get_connection()

        sort = getSort(queryObj)
        skip = getSkip(queryObj)
        search = getSearch(queryObj)
        limit = getLimit(queryObj)
        date = getDate(queryObj)

        query = await salesQuery(search, '', date, False, sort, skip, limit)

        allSales = json.loads(json.dumps(
            list(conn.sales.aggregate(query)), cls=JSONEncoder))

        return allSales
    except Exception as error:
        print('Error in salesReports function ', error)
        return Res(500).errorRes()
