from fastapi import FastAPI

from app.apps.categories.router import router as categories_router
from app.apps.products.router import router as products_router


# Создаём приложение FastAPI
app = FastAPI(
  title="CryShopa Интернет-магазин",
  version="0.1.0",
)

# Подключаем маршруты категорий и товаров
app.include_router(categories_router)
app.include_router(products_router)


# Корневой эндпоинт для проверки
@app.get("/")
async def root():
  """
  Корневой маршрут, подтверждающий, что API работает.
  """
  return {"message": "Добро пожаловать в API интернет-магазина!"}
