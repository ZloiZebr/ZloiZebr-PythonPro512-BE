from decimal import Decimal
from enum import Enum
from sqlalchemy import Date,DateTime,ForeignKey,Numeric,String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import date, datetime

class Base(DeclarativeBase):
    pass

# 1. связь один(Manufacturer) ко многим (Products)
class Manufacturer(Base):
    __tablename__ = "manufacturers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    country: Mapped[str] = mapped_column(String(100))
    website: Mapped[str] = mapped_column(String(100))
    
    products: Mapped[list["Product"]] = relationship(
        back_populates="manufacturer"
    )


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(default=True) 
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey("manufacturers.id"))

    manufacturer: Mapped["Manufacturer"] = relationship(
        back_populates="products",
        uselist=False
    )

# 2. связь один(User) к одному (Profile)
class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    
    customers_profile: Mapped["CustomerProfile"] = relationship(
        uselist=False,
        back_populates="customer"
    )

class CustomerProfile(Base):
    __tablename__ = "customers_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    phone: Mapped[str] = mapped_column(String(20))
    address: Mapped[str] = mapped_column(String(100))
    birthday: Mapped[date] = mapped_column(Date())
    
    customer: Mapped["Customer"] = relationship(
        uselist=False,
        back_populates="customers_profile"
    )


# 3. связь многие (Order) ко многим (OrderItem)
class OrderStatus(Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.IN_PROGRESS)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(tz=0)
    )

    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan"
    )

class OrderItem(Base):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int]
    price: Mapped[Decimal] = mapped_column(Numeric(20, 2))
    
    order: Mapped["Order"] = relationship(
        back_populates="order_items",
    )