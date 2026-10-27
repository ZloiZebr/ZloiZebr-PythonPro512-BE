from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Annotated


class ProductResponse(BaseModel):
  """
  Модель для ответа с данными товара.
  Используется в GET-запросах.
  """
  id: Annotated[int, Field(description="Уникальный идентификатор товара")]
  name: Annotated[str, Field(description="Название товара")]
  description: Annotated[str | None, Field(description="Описание товара")] = None
  price: Annotated[Decimal, Field(description="Цена товара в рублях", gt=0, decimal_places=2)]
  image_url: Annotated[str | None, Field(description="URL изображения товара")] = None
  stock: Annotated[int, Field(description="Количество товара на складе")]
  category_id: Annotated[int, Field(description="ID категории")]
  is_active: Annotated[bool, Field(description="Активность товара")]

  model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
  """
  Модель для создания и обновления товара.
  Используется в POST и PUT запросах.
  """
  name: Annotated[str, Field(
    min_length=3,
    max_length=100,
    description="Название товара (3-100 символов)"
  )]
  description: Annotated[str | None, Field(
    max_length=500,
    description="Описание товара (до 500 символов)"
  )] = None
  price: Annotated[Decimal, Field(gt=0, description="Цена товара (больше 0)", decimal_places=2)]
  image_url: Annotated[str | None, Field(max_length=200, description="URL изображения товара")] = None
  stock: Annotated[int, Field(ge=0, description="Количество товара на складе (0 или больше)")]
  category_id: Annotated[int, Field(description="ID категории, к которой относится товар")]


ProductFullUpdate = ProductCreate
