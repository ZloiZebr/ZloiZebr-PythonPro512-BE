from fastapi import FastAPI

from users.router import router as users_router

# Создаём приложение FastAPI
app = FastAPI(
    title="Homework №7 part №2",
)

# Подключаем маршруты категорий и товаров
app.include_router(users_router)


# Корневой эндпоинт для проверки
@app.get("/")
async def root():
    """
    Корневой маршрут, подтверждающий, что API работает.
    """
    return {"message": "Добро пожаловать в API интернет-магазина!"}
