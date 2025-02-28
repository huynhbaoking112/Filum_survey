from fastapi import APIRouter
from controllers.admin_controller import admin_controller

router = APIRouter()

@router.get("/admin/bg")
def read_admin_root():
    return admin_controller.read_admin_controller()



