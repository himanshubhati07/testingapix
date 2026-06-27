<<<<<<< HEAD
# Security helpers for password hashing and JWT tokens.
=======
# Security utilities for password hashing and JWT handling
>>>>>>> origin/main
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext

<<<<<<< HEAD
load_dotenv('.env_c517696b-c1ad-4fbe-ac2d-9f27763c2096', override=True)

SECRET_KEY = os.getenv("SECRET_KEY", "change-me-secret")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
=======
load_dotenv('.env_d3b2dbc6-eb80-47a1-8fc6-6d72dad7f2f6', override=True)

SECRET_KEY = os.getenv("SECRET_KEY", "change_this_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
>>>>>>> origin/main
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


<<<<<<< HEAD
def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"sub": subject, "exp": expire}
=======
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
>>>>>>> origin/main
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
