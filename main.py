from fastapi import FastAPI
from initialize import db_config, redis_config
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# initialize config package
db_config.connection_mongodb()
redis_config.initialize_redis_cache()

from routers.admin_router import admin_router
from routers.client_router import client_router

app.include_router(admin_router.router)
app.include_router(client_router.router)
