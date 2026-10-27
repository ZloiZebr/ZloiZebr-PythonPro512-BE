from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal

from app.core.db.base import int_pk
from app.core.db.session import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from apps.categories.models import Category


class Product(Base):
  __tablename__ = "products"

  id: Mapped[int_pk]
  name: Mapped[str] = mapped_column(String(100)) # Здесь у нас: nullable=False
  description: Mapped[str | None] = mapped_column(String(500)) # Здесь у нас: nullable=True
  price: Mapped[Decimal] = mapped_column(Numeric(10, 2)) # Здесь у нас: nullable=False
  image_url: Mapped[str | None] = mapped_column(String(200)) # Здесь у нас: nullable=True
  stock: Mapped[int] # Здесь у нас: mapped_column(Integer, nullable=False)
  is_active: Mapped[bool] = mapped_column(default=True) # Здесь у нас: Boolean, nullable=False
  category_id: Mapped[int] = mapped_column(ForeignKey("categories.id")) # Здесь у нас: nullable=False

  category: Mapped["Category"] = relationship(back_populates="products") # Здесь у нас: "Category"
  # параметры которые я указал в комментариях можно указать явно
