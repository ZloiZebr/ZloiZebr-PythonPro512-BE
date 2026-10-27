
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select, update

from app.core.db.dependencies import SessionDep
from app.apps.categories.models import Category
from app.apps.products.models import Product
from app.apps.products.schemas import ProductCreate, ProductFullUpdate, ProductResponse

# Создаём маршрутизатор для товаров
router = APIRouter(
  prefix="/products",
  tags=["products"],
)


@router.get("")
async def get_all_products(
  db: SessionDep
) -> list[ProductResponse]:
  """
  Возвращает список всех товаров.
  """
  # stmt = select(Product).where(
  #   Product.is_active == True
  # )
  stmt = select(Product).join(Category).where(
    Product.is_active == True,
    Category.is_active == True,
  )

  return db.scalars(stmt).all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_product(
  product_create: ProductCreate,
  db: SessionDep
) -> ProductResponse:
  """
  Создаёт новый товар.
  """
  category_db = db.scalar(
    select(Category).where(
      Category.id == product_create.category_id,
      Category.is_active == True
    )
  )
  if category_db is None:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found or inactive")

  new_product_db = Product(**product_create.model_dump())
  db.add(new_product_db)
  db.commit()
  # db.refresh(new_product_db)
  return new_product_db


@router.get("/category/{category_id}")
async def get_products_by_category(
  category_id: int,
  db: SessionDep
) -> list[ProductResponse]:
  """
  Возвращает список товаров в указанной категории по её ID.
  """
  category_db = db.scalar(
    select(Category).where(
      Category.id == category_id,
      Category.is_active == True
    )
  )
  if category_db is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found or inactive")

  products_db = db.scalars(
    select(Product).where(
      Product.category_id == category_id,
      Product.is_active == True
    )
  ).all()
  return products_db


@router.get("/{product_id}")
async def get_product(
  product_id: int,
  db: SessionDep
) -> ProductResponse:
  """
  Возвращает детальную информацию о товаре по его ID.
  """
  product_db = db.scalar(
    select(Product).where(
      Product.id == product_id,
      Product.is_active == True
    )
  )
  if product_db is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or inactive")

  category_db = db.scalar(
    select(Category).where(
      Category.id == product_db.category_id,
      Category.is_active == True
    )
  )
  if category_db is None:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found or inactive")

  return product_db


@router.put("/{product_id}")
async def update_product(
  product_id: int,
  product_full_update: ProductFullUpdate,
  db: SessionDep
) -> ProductResponse:
  """
  Обновляет товар по его ID.
  """
  product_db = db.scalar(
    select(Product).where(
      Product.id == product_id,
      Product.is_active == True
    )
  )
  if product_db is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

  category_db = db.scalar(
    select(Category).where(
      Category.id == product_full_update.category_id,
      Category.is_active == True
    )
  )
  if category_db is None:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found or inactive")

  db.execute(
    update(Product).where(
      Product.id == product_id
    ).values(**product_full_update.model_dump())
  )
  db.commit()
  # db.refresh(product_db)
  return product_db


@router.delete("/{product_id}")
async def delete_product(product_id: int, db: SessionDep) -> dict:
  """
  Удаляет товар по его ID.
  """
  product_db = db.scalar(
    select(Product).where(
      Product.id == product_id,
      Product.is_active == True
    )
  )
  if product_db is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or inactive")

  product_db.is_active = False # Можно так: db.execute(update(Product).where(Product.id == product_id).values(is_active=False))
  db.commit()
  return {"status": "success", "message": "Product marked as inactive"}
