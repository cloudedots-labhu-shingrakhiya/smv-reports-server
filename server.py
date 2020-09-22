import requests
import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routes.index import router as allRouter
from config import NODE_SERVER_URL
from helper.response import Response as Res

app = FastAPI(title="FastAPI_Structure")
app.include_router(allRouter)


@app.middleware("http")
async def checkHeaders(request: Request, call_next):
    try:
        global NODE_SERVER_URL
        if (not NODE_SERVER_URL.isspace()):

            if ('branch' in request.headers and len(request.headers['branch']) >= 0 and not request.headers['branch'].isspace()):
                NODE_SERVER_URL = 'http://localhost:3399/api/gateway/auth/branch'
            else:
                NODE_SERVER_URL = 'http://localhost:3399/api/gateway/auth/admin'

        print('url...', NODE_SERVER_URL)

        apiRes = requests.post(NODE_SERVER_URL, data={},
                               headers=request.headers, params=request.query_params)

        if apiRes.status_code == 200:
            return await call_next(request)
        else:
            res = JSONResponse(content=apiRes.json(),
                               status_code=apiRes.status_code, headers=dict(apiRes.headers))
            return res
    except Exception as error:
        print('Error in checkHeaders middleware in server.py ', error)
        return Res(500).errorRes()
