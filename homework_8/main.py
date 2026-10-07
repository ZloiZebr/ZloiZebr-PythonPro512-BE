
from fastapi import FastAPI,status
from pydantic import BaseModel
from decimal import Decimal

app = FastAPI()

class User(BaseModel):
    name: str
    age: int

class UserResponse(BaseModel):
    name: str
    age: int
    is_adult: bool

@app.get("/square/{number}")
async def get_square(number:Decimal|int) -> Decimal:
    return number**2

@app.get("/fullname")
async def get_fullname(name:str, surname:str) -> str:
    return name.capitalize() + " " + surname.capitalize()

@app.post("/user",status_code = status.HTTP_201_CREATED)
async def get_user_info(user:User) -> UserResponse:
    is_adult = False
    if user.age >= 18:
        is_adult = True
    return UserResponse(
        name = user.name,
        age = user.age,
        is_adult = is_adult
    )

@app.get("/reverse/{text}")
async def get_reverse_text(text:str) -> str:
    return text[::-1]