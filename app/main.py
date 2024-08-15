from fastapi import FastAPI
from routers.item_router import router as item_router
from routers.websocket_router import router as websocket_router

app = FastAPI()
app.include_router(item_router, 
    prefix="/item",
    tags=["Item"])
app.include_router(websocket_router)