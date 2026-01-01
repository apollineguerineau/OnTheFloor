from fastapi import FastAPI
from src.api.routes.user import router as users_router
from src.api.routes.session import router as session_router

app = FastAPI()

app.include_router(users_router)
app.include_router(session_router)
