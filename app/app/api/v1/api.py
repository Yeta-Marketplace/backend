from fastapi import APIRouter

from app.api.v1.endpoints import login, users, yardsales, feedback, event_types

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(yardsales.router, prefix="/yardsales", tags=["yardsales"])
api_router.include_router(event_types.router, prefix="/events/categories", tags=["events"])
api_router.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
