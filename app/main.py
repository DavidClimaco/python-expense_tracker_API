from fastapi import FastAPI

from .config.db import create_db_and_tables
from .routers import auth_router, expenses_router, user_router

app = FastAPI(lifespan=create_db_and_tables)
app.include_router(expenses_router.router)
app.include_router(auth_router.router)
app.include_router(user_router.router)


@app.get("/")
async def root():
    return {"Hello World!"}
