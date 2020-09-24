from datetime import datetime, date
from fastapi import APIRouter, Request, Response
from typing import Optional
from helper.response import Response as Res, JSONEncoder
from controllers.customers.customers import customersReports
router = APIRouter()


@router.get("/customers-reports")
async def getCustomersReports(req: Request, res: Response):
    try:
        report = await customersReports(req.query_params)
        if len(report) != 0:
            return Res(report).successRes()
        else:
            return Res(404).errorRes()
    except Exception as error:
        print('GET /customers-reports Error', error)
        return Res(500).errorRes()
