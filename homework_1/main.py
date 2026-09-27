from fastapi import FastAPI

app = FastAPI(
    title = "ZloiZebr HomeWork №1",
    description = "Домашние работы по изучению FastAPI",
)

@app.get("/users/admin")
async def getAdmin() -> dict:
    return {"admin": "администратор не попадает в эндпоинт users"}

@app.get("/users/{user_id}")
async def getUserID(user_id: int) -> dict:
    return {"user_id": user_id}


# @app.get("/products/{product_name}")
# async def getProduct(product_name: str) -> dict:
#     return {"product": product_name}

@app.get("/products")
async def getProduct(category:str|None = None, min_price:int|None = None, max_price:int|None = None ) -> dict:
    return {"category": category, "min_price": min_price, "max_price": max_price}