from typing import List, Optional, Dict, Any
from app.models.game import Game
from app.models.user import User
from app.models.text import Text
from tortoise.exceptions import DoesNotExist

async def create_game(
    user: User,
    text: Text,
    wpm: float,
    raw_wpm: float,
    accuracy: float,
    errors: int,
    duration: int,
    performance_data: Optional[List[Dict[str, Any]]] = None
) -> Game:
    game = Game(
        user=user,
        text=text,
        wpm=wpm,
        raw_wpm=raw_wpm,
        accuracy=accuracy,
        errors=errors,
        duration=duration,
        performance_data=performance_data
    )
    await game.save()
    return game

async def get_game_by_id(game_id: int) -> Optional[Game]:
    return await Game.get_or_none(id=game_id)

async def get_game_by_id_with_performance(game_id: int) -> Optional[Game]:
    """Получение игры с посекундными данными"""
    return await Game.get_or_none(id=game_id).prefetch_related('user', 'text')

async def get_games_by_user(user_id: int) -> List[Game]:
    return await Game.filter(user_id=user_id).order_by('-timestamp')

async def get_recent_games_by_user(user_id: int, limit: int = 10) -> List[Game]:
    return await Game.filter(user_id=user_id).order_by('-timestamp').limit(limit)

async def get_games_by_date_range(user_id: int, start_date, end_date) -> List[Game]:
    return await Game.filter(
        user_id=user_id,
        timestamp__gte=start_date,
        timestamp__lte=end_date
    ).order_by('-timestamp')

async def get_user_best_scores(user_id: int) -> dict:
    best_wpm = await Game.filter(user_id=user_id).order_by('-wpm').first()
    best_accuracy = await Game.filter(user_id=user_id).order_by('-accuracy').first()
    
    return {
        "best_wpm": best_wpm.wpm if best_wpm else 0,
        "best_accuracy": best_accuracy.accuracy if best_accuracy else 0
    }

async def get_user_stats(user_id: int) -> dict:
    games = await Game.filter(user_id=user_id)
    if not games:
        return {}
    
    total_games = len(games)
    avg_wpm = sum(game.wpm for game in games) / total_games
    avg_accuracy = sum(game.accuracy for game in games) / total_games
    
    return {
        "total_games": total_games,
        "average_wpm": round(avg_wpm, 2),
        "average_accuracy": round(avg_accuracy, 2)
    }

async def get_game_performance_data(game_id: int) -> Optional[List[Dict[str, Any]]]:
    game = await Game.get_or_none(id=game_id)
    if game and game.performance_data:
        return game.performance_data
    return None

async def get_games_with_performance_by_user(user_id: int, limit: int = 10) -> List[Game]:
    return await Game.filter(user_id=user_id).order_by('-timestamp').limit(limit)

async def update_game(game_id: int, **kwargs) -> Optional[Game]:
    game = await Game.get_or_none(id=game_id)
    if game:
        for key, value in kwargs.items():
            setattr(game, key, value)
        await game.save()
    return game

async def delete_game(game_id: int) -> bool:
    try:
        game = await Game.get(id=game_id)
        await game.delete()
        return True
    except DoesNotExist:
        return False