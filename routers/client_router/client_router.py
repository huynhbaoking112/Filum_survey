from fastapi import APIRouter
from controllers.client_controller import client_controller

router = APIRouter()

@router.get("/client/bg")
def read_client_root():
    return client_controller.read_client_controller()