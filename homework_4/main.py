from typing import Annotated

from fastapi import FastAPI,HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel,Field

app = FastAPI(
    title = "ZloiZebr HomeWork №4",
    description = "Домашние работы по изучению FastAPI",
)
app.mount("/static", StaticFiles(directory="static"))
templates = Jinja2Templates(directory="templates")

class ProductResponse(BaseModel):
    id: Annotated[int, Field(ge = 1)]
    name: Annotated[str, Field(max_length = 50)]
    price: Annotated[int, Field(ge = 0)]
    category: Annotated[str, Field(max_length = 50)]

products_db: list[ProductResponse] = [
    ProductResponse(id=1, name="Laptop Pro 15", price=1200, category="Electronics"),
    ProductResponse(id=2, name="Wireless Mouse", price=35, category="Electronics"),
    ProductResponse(id=3, name="Mechanical Keyboard", price=89, category="Electronics"),
    ProductResponse(id=4, name="USB-C Hub", price=45, category="Accessories"),
    ProductResponse(id=5, name="Noise-Canceling Headphones", price=150, category="Audio"),
    ProductResponse(id=6, name="Smartwatch X", price=220, category="Wearables"),
]

@app.get("/web/products", name="products")
async def get_products(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html", {"products": products_db})


@app.get("/web/products/{product_id}")
async def get_product_detail(request: Request, product_id: int) -> HTMLResponse:
    for product in products_db:
        if product.id == product_id:
            return templates.TemplateResponse(request, "detail.html", {"product": product})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден")
