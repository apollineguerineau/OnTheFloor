from fastapi import FastAPI
from src.api.routes.user import router as users_router
from src.api.routes.session import router as session_router
from src.api.routes.location import router as location_router
from src.api.routes.block import router as block_router
from src.api.routes.exercise import router as exercise_router

app = FastAPI()

app.include_router(users_router)
app.include_router(session_router)
app.include_router(location_router)
app.include_router(block_router)
app.include_router(exercise_router)
