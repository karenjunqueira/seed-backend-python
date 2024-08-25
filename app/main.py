from fastapi import FastAPI
from routers.item_router import router as item_router
from routers.user_router import router as user_router

app = FastAPI()
app.include_router(item_router, 
    prefix="/items",
    tags=["Item"])
app.include_router(user_router, 
    prefix="/users",
    tags=["User"])
