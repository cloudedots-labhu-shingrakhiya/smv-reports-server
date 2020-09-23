from datetime import datetime
from helper.response import JSONEncoder, Response as Res
from bson.objectid import ObjectId
import json


async def usersQuery(textSearch, search, date, onlyTotal, sort, skip, limit):
    try:
        queryProject = {
            'firstName': 1,
            'lastName': 1,
            'email': 1,
            'contact': 1,
            'address': 1,
            'avatar': 1
        }
        if len(textSearch) > 0 and not textSearch.isspace():
            queryProject['score'] = {'$meta': 'textScore'
                                     }
            for key in dict(sort):
                sort.pop(key)

            sort['score'] = {'$meta': 'textScore'
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
            query[0]['$match'].update({'$text': {'$search': textSearch}})

        if len(search) > 0 and not search.isspace():
            query.append({'$match': {
                'name': {'$regex': search,
                         '$options': 'i'
                         }
            }
            })
        
        if date:
            print('date.......', dict(date))

        print('query.........', query)
        return query

    except Exception as error:
        print('Error in usersQuery function ', error)
        return Res(500).errorRes()
