from typing import Annotated
from datetime import datetime
import uvicorn
from fastapi import FastAPI, Depends,HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class Time(BaseModel):
    time: datetime

class Token(BaseModel):
    token_auth: bool = False

async def get_current_time() -> Time:
    return Time(time=datetime.now())

async def get_token_or_401(token: str | None = None) -> bool:
    if token is not None:
        return Token(token_auth=True)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.get("/protected")
async def get_token(token: Annotated[Token, Depends(get_token_or_401)]) -> Token:
    return token

@app.get("/time")
async def get_time(current_time: Annotated[Time, Depends(get_current_time)]) -> Time:
    return current_time



if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host="127.0.0.1",
        port=8000,
        reload=True
    )