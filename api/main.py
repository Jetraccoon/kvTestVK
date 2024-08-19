from fastapi import FastAPI, Depends, HTTPException, status
from datetime import timedelta

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from database import get_user_from_db
from auth import create_access_token, get_current_user
from models import Token, WriteData, ReadKeys, UserLogin
from crud import write_data, read_data

app = FastAPI()


@app.post("/api/login", response_model=Token)
def login(data: UserLogin):
    user = get_user_from_db(data.username)
    if not user or data.password != user[0][2]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token}


@app.post("/api/write")
def write_kv(data: WriteData, user: str = Depends(get_current_user)):
    write_data(data.data)
    return {"status": "success"}


@app.post("/api/read")
def read_kv(keys: ReadKeys, user: str = Depends(get_current_user)):
    data = read_data(keys.keys)
    return {"data": data}
