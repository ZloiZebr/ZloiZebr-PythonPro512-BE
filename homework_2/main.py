from typing import Annotated
from fastapi import Body, FastAPI, HTTPException, Path, status
from pydantic import BaseModel

app = FastAPI(
    title = "ZloiZebr HomeWork №2",
    description = "Домашние работы по изучению FastAPI",
)

class ProductResponse(BaseModel):
    name: str
    price: int
    category: str

products_db = {
    1: {"name": "Laptop", "price": 1200, "category": "Electronics"},
    2: {"name": "Coffee Maker", "price": 150, "category": "Appliances"}
}

@app.get("/products")
async def getProduct(category:str|None = None) -> dict:
    filteredList = {}
    if category is not None:
        for id, product in products_db.items():
            if product['category'] == category:
                filteredList[id] = product
        return filteredList
    return products_db

@app.get("/products/{product_id}")
async def get_product(
    product_id: Annotated[int, Path(ge = 1)]
) -> ProductResponse:
    try:
        return products_db[product_id]
    except:
        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Product not found"
    )

@app.post("/products", status_code = status.HTTP_201_CREATED)
async def create_product(
    name: Annotated[str, Body(max_length = 50)],
    price: Annotated[int, Body(ge = 0)],
    category: Annotated[str, Body(max_length = 30)]
) -> ProductResponse: 
    new_id = max(products_db) + 1 if products_db else 1
    new_product = {"name": name, "price": price, "category": category}
    products_db[new_id] = new_product
    return new_product
