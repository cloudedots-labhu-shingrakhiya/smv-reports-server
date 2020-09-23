from datetime import datetime
from helper.db import get_connection
from helper.response import JSONEncoder, Response as Res
from bson.objectid import ObjectId
import json


def getSort(queryObj):
    try:
        sort = queryObj['sort'] if 'sort' in queryObj else 'firstName'
        order = queryObj['order'] if 'order' in queryObj else 'asc'
        return {
            sort:  1 if (order == 'asc' or order == 1) else -1
        }
    except Exception as error:
        print('Error in getSort function ', error)
        return Res(500).errorRes()


def getSkip(queryObj):
    try:
        limit = getLimit(queryObj)
        page = getPage(queryObj)
        return (limit*(int(page) - 1)) if limit else 0
    except Exception as error:
        print('Error in getSkip function ', error)
        return Res(500).errorRes()


def getPage(queryObj):
    try:
        page = queryObj['page'] if 'page' in queryObj else 1
        return page
    except Exception as error:
        print('Error in getPage function ', error)
        return Res(500).errorRes()


def getLimit(queryObj):
    try:
        return queryObj['limit'] if 'limit' in queryObj and int(queryObj['limit']) >= 0 else 15
    except Exception as error:
        print('Error in getLimit function ', error)
        return Res(500).errorRes()


def getSearch(queryObj):
    try:
        return queryObj['search'] if 'search' in queryObj else ''
    except Exception as error:
        print('Error in getSearch function ', error)
        return Res(500).errorRes()


def getDate(queryObj):
    try:
        if(queryObj and ('startDate' in queryObj or 'endDate' in queryObj)):
            if 'startDate' in queryObj and len(queryObj['startDate']) > 0 and not queryObj['startDate'].isspace():
                startDate = datetime.strptime(
                    queryObj['startDate'], "%d/%m/%Y")
                print('startDate..', startDate, type(startDate))

            if 'endDate' in queryObj and len(queryObj['endDate']) > 0 and not queryObj['endDate'].isspace():
                endDate = datetime.combine(datetime.strptime(
                    queryObj['endDate'], "%d/%m/%Y"), datetime.max.time())
                print('endDate with max...', endDate,  type(endDate))

            return {
                'startDate': startDate or '',
                'endDate': endDate or ''
            }
        else:
            return
    except Exception as error:
        print('Error in getDate function ', error)
        return Res(500).errorRes()
