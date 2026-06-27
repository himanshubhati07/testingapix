<<<<<<< HEAD
# Authentication dependencies for protected routes.
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .security import ALGORITHM, SECRET_KEY
from ..database import get_db
from ..models import User
=======
# Authentication dependencies for JWT validation
import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

load_dotenv('.env_d3b2dbc6-eb80-47a1-8fc6-6d72dad7f2f6', override=True)

from app.database import get_db
from app.models import User
from app.core.security import SECRET_KEY, ALGORITHM
>>>>>>> origin/main

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
<<<<<<< HEAD
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
=======
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
>>>>>>> origin/main
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
<<<<<<< HEAD
        payload = jwt_decode(token)
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
=======
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc
>>>>>>> origin/main
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise credentials_exception
    return user
<<<<<<< HEAD


def jwt_decode(token: str) -> dict:
    from jose import jwt

    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
=======
>>>>>>> origin/main
