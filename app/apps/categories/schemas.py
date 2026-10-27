from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict


class CategoryResponse(BaseModel):
  """
  Модель для ответа с данными категории.
  Используется в GET-запросах.
  """
  id: Annotated[int, Field(description="Уникальный идентификатор категории")]
  name: Annotated[str, Field(description="Название категории")]
  parent_id: Annotated[int | None, Field(description="ID родительской категории, если есть")] = None
  is_active: Annotated[bool, Field(description="Активность категории")] # для "мягкого" удаления категории

  model_config = ConfigDict(from_attributes=True)
  # Мы планируем работать с базами данных через ORM
  # По умолчанию Pydantic умеет создавать объекты только из словарей
  # Но объекты из базы данных — это не словари, а сложные объекты классов.
  # Что делает этот флаг: Он разрешает Pydantic читать данные не только по ключам data["name"], но и через точку: data.name.

  # Почему указали только для GET (Сериализация): Данные текут из Базы Данных -> в Pydantic -> в JSON
  # POST/PUT (Десериализация): Данные текут из JSON -> в Pydantic -> в БД. Здесь Pydantic получает обычный JSON (который легко превращается в словарь).

  # Пример:
  # Представим, что у нас есть объект категории из базы данных SQLAlchemy:
  # db_category = DBCategory(id=1, name="Электроника", is_active=True) # Объект из БД
  # Без from_attributes=True:
  # Category.model_validate(db_category)  ->  ВЫДАСТ ОШИБКУ! (ожидался словарь)
  # С from_attributes=True:
  # category = Category.model_validate(db_category)  # РАБОТАЕТ!


class CategoryCreate(BaseModel):
  """
  Модель для создания и обновления категории.
  Используется в POST и PUT запросах.
  """
  name: Annotated[str, Field(
    min_length=3,
    max_length=50,
    description="Название категории (3-50 символов)"
  )]
  parent_id: Annotated[int | None, Field(description="ID родительской категории, если есть")] = None


CategoryFullUpdate = CategoryCreate
