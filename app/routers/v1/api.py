from fastapi import APIRouter

from app.routers.v1.endpoints import auth, games, leaderboard, performance_logs, sessions, texts, users

router = APIRouter()
router.include_router(auth.router, tags=['User'])
router.include_router(users.router, prefix="/users/", tags=['User'])
router.include_router(games.router, prefix="/games/", tags=['Game'])
router.include_router(leaderboard.router, prefix="/leaderboards/", tags=['Leaderboard'])
router.include_router(performance_logs.router, prefix="/logs/", tags=['Performance Log'])
router.include_router(texts.router, prefix="/texts/", tags=['Texts'])


