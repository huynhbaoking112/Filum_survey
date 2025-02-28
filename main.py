from fastapi import FastAPI
from routers.admin_router import admin_router
from routers.client_router import client_router


app = FastAPI()


app.include_router(admin_router.router)
app.include_router(client_router.router)
