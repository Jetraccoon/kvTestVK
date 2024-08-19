from pydantic import BaseModel
from typing import Dict, List, Any


class Token(BaseModel):
    access_token: str


class UserLogin(BaseModel):
    username: str
    password: str


class WriteData(BaseModel):
    data: Dict[Any, Any]


class ReadKeys(BaseModel):
    keys: List[Any]
