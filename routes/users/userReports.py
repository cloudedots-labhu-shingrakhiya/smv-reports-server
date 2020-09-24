from datetime import datetime, date
from fastapi import APIRouter, Request, Response
from typing import Optional
from helper.response import Response as Res, JSONEncoder
from controllers.users.userReports import usersReports, userReport
router = APIRouter()


@router.get("/users-reports")
async def getUsersReports(req: Request, res: Response):
    try:
        report = await usersReports(req.query_params)
        if len(report) != 0:
            return Res(report).successRes()
        else:
            return Res(404).errorRes()
    except Exception as error:
        print('GET /users-reports Error', error)
        return Res(500).errorRes()


@router.get("/user-reports/{id}")
async def getUserReport(id: str, req: Request, res: Response):
    try:
        report = await userReport(id)
        if len(report) != 0:
            return Res(report).successRes()
        else:
            return Res(404).errorRes()
    except Exception as error:
        print('GET /user-reports Error', id, error)
        return Res(500).errorRes()
