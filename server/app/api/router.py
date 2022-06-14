from fastapi import APIRouter

from .endpoints import comments, competitions, login, teams, users, excellents

api_router = APIRouter()
api_router.include_router(comments.router, prefix="/comments")
api_router.include_router(competitions.router, prefix="/competitions")
api_router.include_router(login.router, prefix="/login")
api_router.include_router(teams.router, prefix="/teams")
api_router.include_router(users.router, prefix="/users")
api_router.include_router(excellents.router, prefix="/excellents")
