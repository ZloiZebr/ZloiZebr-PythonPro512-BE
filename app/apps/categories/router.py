from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status
from sqlalchemy import select, update

from app.core.db.dependencies import SessionDep
from app.apps.categories.schemas import CategoryCreate, CategoryFullUpdate, CategoryResponse
from app.apps.categories.models import Category

from app.apps.products.models import Product

# Создаём маршрутизатор с префиксом и тегом
router = APIRouter(
  prefix="/categories",
  tags=["categories"],
)


@router.get("")
async def get_all_categories(
  db: SessionDep
) -> list[CategoryResponse]:
  """
  Возвращает список всех активных категорий.
  """
  stmt = select(Category).where(Category.is_active == True)
  categories = db.scalars(stmt).all() # Можно так: db.execute(stmt).scalars().all()
  return categories


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_category(
  db: SessionDep,
  category_create: CategoryCreate
) -> CategoryResponse:
  """
  Создаёт новую категорию.
  """
  # Проверка существования parent_id, если указан
  if category_create.parent_id is not None:
    stmt = select(Category).where(
      Category.id == category_create.parent_id,
      Category.is_active == True
    )
    parent = db.scalar(stmt) # scalar() вернет объект или None # Можно так: db.execute(stmt).scalars().first() или db.scalars(stmt).first()
    if parent is None:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Parent category not found"
      )

  # Создание новой категории
  db_category = Category(**category_create.model_dump())
  db.add(db_category)
  db.commit()
  # db.refresh(db_category) # Необязательно
  return db_category


@router.put("/{category_id}")
async def update_category(
  category_id: Annotated[int, Path(ge=1)],
  category_full_update: CategoryFullUpdate,
  db: SessionDep
) -> CategoryResponse:
  """
  Обновляет категорию по её ID.
  """
  if category_id == category_full_update.parent_id:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="The category isn't its own parent"
    )


  # Проверка существования категории
  stmt = select(Category).where(
    Category.id == category_id,
    Category.is_active == True
  )
  db_category = db.scalar(stmt) # scalar() вернет объект или None # Можно так: db.execute(stmt).scalars().first() или db.scalars(stmt).first()
  if db_category is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

  # Проверка существования parent_id, если указан
  if category_full_update.parent_id is not None:
    parent_stmt = select(Category).where(
      Category.id == category_full_update.parent_id,
      Category.is_active == True
    )
    parent = db.scalar(parent_stmt) # scalar() вернет объект или None # Можно так: db.execute(stmt).scalars().first() или db.scalars(stmt).first()
    if parent is None:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parent category not found")
    elif parent.parent.id == category_id:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="There are no cyclical relationships"
      )
    # id      parent_id
    # 1   -   2
    # 2   -   1

  # Обновление категории
  db.execute(
    update(Category)
    .where(Category.id == category_id)
    .values(**category_full_update.model_dump())
  )
  db.commit()
  # db.refresh(db_category)
  return db_category

# Короче, сейчас имеется некоторая проблема. Если пользователь в endpoint передаст parent_id равный category_id то получится, что категория - родитель сама себе. Это явно будет неправильно в рамках БД. Есть другой вариант, пользователь укажет что категория 1 это родитель категории 2, и наоборот, получится циклические связи.
# Мы отбили это 2 доп условиями на уровне объектов пайтон:


@router.delete("/{category_id}")
async def delete_category(
  category_id: Annotated[int, Path(ge=1)],
  db: SessionDep
) -> dict:
  """
  Логически удаляет категорию по её ID, устанавливая is_active=False.
  """
  # Проверка существования активной категории
  stmt = select(Category).where(Category.id == category_id, Category.is_active == True)
  category = db.scalar(stmt) # scalar() вернет объект или None # Можно так: db.execute(stmt).scalars().first() или db.scalars(stmt).first()
  if category is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

  # Логическое удаление категории (установка is_active=False)
  category.is_active = False # Можно так: db.execute(update(Category).where(Category.id == category_id).values(is_active=False))
  db.commit()

  return {"status": "success", "message": "Category marked as inactive"}

# 1) Если мы все же хотим не отключить, а полностью удалить категорию (и все ее подкатегории и товары) мы можем сделать следующее:
# 1. Дополнить модель алхимии:
# Добавляем каскадное удаление дочерним категориям, чтоб если удаляем родителя дочерние не остались сиротами (что может привести к ошибкам)
# parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE")) # +ondelete="CASCADE"
# children: Mapped[list["Category"]] = relationship(
#     back_populates="parent",
#     cascade="all, delete-orphan"
# ) # +cascade="all, delete-orphan"

# В модели Product
# category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"))


# products: Mapped[list["Product"]] = relationship(
#     back_populates="category",
#     cascade="all, delete" # Удалит товары только при удалении всей категории
# )

# 2. Изменить поведение эндпоинта на полное удаление:
# @router.delete("/{category_id}")
# async def delete_category(
#     category_id: Annotated[int, Path(gt=1)],
#     db: SessionDep
# ) -> CategorySchema:
#     """
#     Удаляет категорию.
#     """
#     # stmt = select(Category).where(Category.id == category_id)
#     # category = db.scalar(stmt)  # получаем категорию или None
#     category = db.get(Category, category_id)
#     if category:
#         response = CategorySchema.model_validate(
#             category
#         )  # готовим тело ответа до удаления, что бы избежать ошибок (преобразовываем модель алхимии в схему пайдентика)

#         db.delete(category)  # удаляем категорию и все ее дочерние категории и товары
#         db.commit()
#         return response

#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND, detail="Category not found."
#     )



# 2) Обычно категории представляют иерархию, где дочерние категории теряют смысл без родителя (например как у нас категории товаров в интернет-магазине), то почти всегда выбирают рекурсивное удаление.
# А так, в список parents_ids получаем id категории и id всех ее потомков, и выполняем запрос:
# db.execute(
#     update(Category)
#     .where(Category.id.in_(parents_ids))
#     .values(is_active=False)
# )
# Я не стал это делать, так как вложенность категорий у нас не ограничена ничем, и это уже задача на логику, а не на работу в FastAPI и SQLAlchemy))

