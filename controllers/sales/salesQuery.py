from datetime import datetime
from helper.response import JSONEncoder, Response as Res
from bson.objectid import ObjectId
import json


async def salesQuery(textSearch, searchProp, date, onlyTotal, sort, skip, limit):
    try:
        sort = {'salesOfficer.name': -1}
        queryProject = {
            'salesOfficer.name': {'$concat': ['$salesOfficer.firstName', ' ', '$salesOfficer.lastName']},
            'salesOfficer.email': 1,
            'salesOfficer.contact': 1,
            'salesOfficer.address': 1,
            'salesOfficer.avatar': 1
            # 'salesOfficer.sessions': 0,
            # 'salesOfficer.password': 0
        }

        query = [
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
            }, {
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

# TODO....// No 'text' index in sales Schema so we can't use $text, $search in aggregate so, we use '$regex' for search...
        # if len(textSearch) > 0 and not textSearch.isspace():
        #     query[0]['$match'].update(
        #         {'$text': {'$search': textSearch,  '$language': 'es',  '$caseSensitive': False, '$diacriticSensitive': True}})

        #     queryProject['score'] = {'$meta': 'textScore'
        #                              }
        #     for key in dict(sort):
        #         sort.pop(key)

        #     sort['score'] = {'$meta': 'textScore'
        #                      }

        if (len(textSearch) > 0 and not textSearch.isspace()) or (len(searchProp) > 0 and not searchProp.isspace()):
            query.append({'$match': {
                'salesOfficer.name': {'$regex': textSearch or searchProp,
                                      '$options': 'i'
                                      }
            }
            })

        if date:
            query[0]['$match'].update({
                'createdAt': {'$gte': date['startDate'], '$lte': date['endDate']}
            })

        if onlyTotal == True:
            query.append({
                '$count': 'total'
            })

        print('sales query.........', query)
        return query

    except Exception as error:
        print('Error in salesQuery function ', error)
        return Res(500).errorRes()
