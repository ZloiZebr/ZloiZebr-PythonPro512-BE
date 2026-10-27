from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.base import int_pk
from app.core.db.session import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from apps.products.models import Product


class Category(Base):
  __tablename__ = "categories"

  id: Mapped[int_pk]
  name: Mapped[str] = mapped_column(String(50)) # Здесь у нас: nullable=False
  is_active: Mapped[bool] = mapped_column(default=True) # Здесь у нас: Boolean, nullable=False
  parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id")) # Здесь у нас: nullable=True

  products: Mapped[list["Product"]] = relationship(back_populates="category") # Здесь у нас: "Product"
  parent: Mapped["Category | None"] = relationship( # Если вы напишете Mapped["Category" | None], Python попытается выполнить операцию «ИЛИ» (|) между строкой "Category" и типом None. Это вызовет ошибку TypeError, потому что нельзя объединять строку и объект Category.
    back_populates="children",
    remote_side="Category.id" # Сложно
  ) # Здесь у нас: "Category"
  children: Mapped[list["Category"]] = relationship( # None не нужно писать, т. к. список может быть пустым
    back_populates="parent"
  ) # Здесь у нас: "Category"
  # параметры которые я указал в комментариях можно указать явно


# id          name               is_active               parent_id
# 1           Электроника        true                    NULL
# 2           Телефоны           true                    1
# 3           Телевизоры         false                   1
# 4           Одежда             true                    NULL
# 5           Мужская            true                    4
