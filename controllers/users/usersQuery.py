from datetime import datetime
from helper.response import JSONEncoder, Response as Res
from bson.objectid import ObjectId
import json


async def usersQuery(textSearch, searchProp, date, onlyTotal, sort, skip, limit):
    try:
        queryProject = {
            'name': {'$concat': ['$firstName', ' ', '$lastName']},
            'email': 1,
            'contact': 1,
            'address': 1,
            'avatar': 1
        }
        query = [
            {
                '$match': {
                    'status': 'active'
                }
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

        if len(textSearch) > 0 and not textSearch.isspace():
            query[0]['$match'].update(
                {'$text': {'$search': textSearch,  '$language': 'es',  '$caseSensitive': False, '$diacriticSensitive': True}})

            queryProject['score'] = {'$meta': 'textScore'
                                     }
            for key in dict(sort):
                sort.pop(key)

            sort['score'] = {'$meta': 'textScore'
                             }

        elif len(searchProp) > 0 and not searchProp.isspace():
            query.append({'$match': {
                'name': {'$regex': searchProp,
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

        print('user query.........', query)
        return query

    except Exception as error:
        print('Error in usersQuery function ', error)
        return Res(500).errorRes()
