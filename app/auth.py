import secrets
from typing import Annotated

from fastapi import Depends, Header, HTTPException

from app.config import API_READ_KEY


def get_api_key(x_api_key: Annotated[str | None, Header()] = None) -> str:
    if not x_api_key or not secrets.compare_digest(x_api_key, API_READ_KEY):
        raise HTTPException(status_code=401, detail="Clave de consulta incorrecta")
    return x_api_key


Auth = Annotated[str, Depends(get_api_key)]
