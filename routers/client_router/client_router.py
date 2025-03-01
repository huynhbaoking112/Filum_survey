from fastapi import APIRouter, Request
from controllers.client_controller import client_controller

router = APIRouter()


# all get router
@router.get("/filum/s/{survey_id}")
async def read_client_survey(survey_id: str):
    return client_controller.read_client_survey_controller(survey_id) 

@router.get("/filum/{survey_id}/lan/{lan}")
async def read_client_survey(survey_id: str, lan: str):
    return client_controller.read_client_survey_lan(survey_id, lan) 


# all post router 
@router.post("/filum/s/{survey_id}")
async def create_client_survey(survey_id: str, req: Request):
    data = await req.json()
    return client_controller.create_client_survey_controller(survey_id, data)