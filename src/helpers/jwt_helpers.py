import os
from fastapi import HTTPException, Request
from jose import JWTError, jwt
from environs import Env

env = Env()

env.read_env(path=".env")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORTIHM = os.getenv("ALGORITHM")


def extract_token_data(request: Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORTIHM])
        user_id: int = payload.get("user_id")
        role: int = payload.get("role")

        return {
            "user_id": user_id,
            "role": role,
        }

    except JWTError as error:
        raise HTTPException(status_code=404, detail=str(error))
