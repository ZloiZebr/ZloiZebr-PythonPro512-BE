from fastapi import APIRouter

# Создаём маршрутизатор с префиксом и тегом
router = APIRouter(
  prefix="/users",
  tags=["users"],
)

@router.get("")
async def get_all_users():
  """
  Возвращает список всех пользователей
  """
  return {"Users": "Список всех пользователей (заглушка)"}

@router.get("{user_id}")
async def get_user(user_id):
  """
  Возвращает возвращает пользователя по ID
  """
  return {"User_ID": user_id}



