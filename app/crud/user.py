from typing import List, Optional
from app.models.user import User

async def create_user(
    username: str,
    email: str,
    hashed_password: str
) -> User:
    user = await User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    return user


async def get_user_by_id(user_id: int) -> Optional[User]:
    return await User.get_or_none(id=user_id)

async def get_user_by_username(username: int) -> Optional[User]:
    return await User.get_or_none(username=username)

async def get_user_by_email(email: int) -> Optional[User]:
    return await User.get_or_none(email=email)

async def get_users(skip: int = 0, limit: Optional[int] = None) -> List[User]:
    query = User.all().offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return await query


async def update_user(user_id: int, **kwargs) -> Optional[User]:
    user = await User.get_or_none(id=user_id)
    for key, value in kwargs.items():
        setattr(user, key, value)
    await user.save()
    return user