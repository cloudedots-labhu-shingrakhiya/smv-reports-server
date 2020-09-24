from datetime import datetime, date
from fastapi import APIRouter, Request, Response
from typing import Optional
from helper.response import Response as Res, JSONEncoder
from controllers.sales.salesReports import salesReports
router = APIRouter()


@router.get("/sales-reports")
async def getSelesReports(req: Request, res: Response):
    try:
        report = await salesReports(req.query_params)
        if len(report) != 0:
            return Res(report).successRes()
        else:
            return Res(404).errorRes()
    except Exception as error:
        print('GET /sales-reports Error', error)
        return Res(500).errorRes()
