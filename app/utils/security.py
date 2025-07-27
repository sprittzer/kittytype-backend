from passlib.context import CryptContext

from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.core.settings import env, log

# hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password) -> str:
    return pwd_context.hash(password)

# jwt
def create_access_token(
    data: dict,
    expires_delta: timedelta = timedelta(minutes=env.ACCESS_TOKEN_EXPIRE_MINUTES),
) -> str:
    to_encode = data.copy()
    
    expire = datetime.utcnow() + expires_delta
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, env.ACCESS_TOKEN_SECRET_KEY, algorithm=env.ACCESS_TOKEN_ALGORITHM
    )
    return encoded_jwt

def decode_username(token) -> str | None:
    try:
        return jwt.decode(
            token, env.ACCESS_TOKEN_SECRET_KEY, env.ACCESS_TOKEN_ALGORITHM
        ).get("sub")
    except JWTError as e:
        log.error(f"An error has occurred while decoding JWT token: {e}")