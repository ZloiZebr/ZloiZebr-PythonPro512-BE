from typing import Annotated
from datetime import datetime
import uvicorn
from fastapi import FastAPI, Depends,HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class Time(BaseModel):
    time: datetime

class User(BaseModel):
    role: str = "guest"

async def require_admin(role: str) -> User:
    if role == "admin":
        return User(role = "admin")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@app.get("/admin/dashboard")
async def is_admin(user_role: Annotated[User, Depends(require_admin)]) -> User:
    return user_role



if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host="127.0.0.1",
        port=8000,
        reload=True
    )