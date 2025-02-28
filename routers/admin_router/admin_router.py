from fastapi import APIRouter, Request
from controllers.admin_controller import admin_controller

router = APIRouter()


# all get router
@router.get("/filum/visual/{survey_id}")
async def get_visual(survey_id: str):
    return admin_controller.controller_get_visual(survey_id)


# all post router 
@router.post("/filum/survey")
async def create_survey(request: Request):
    body = await request.json()
    return admin_controller.controller_create_survey(body)
