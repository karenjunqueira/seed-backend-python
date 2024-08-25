from fastapi import FastAPI
from routers.token_router import router as token_router
from routers.item_router import router as item_router
from routers.user_router import router as user_router

app = FastAPI()
app.include_router(item_router)
app.include_router(user_router)
app.include_router(token_router)

