from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import Depends
from collections.abc import Generator

from app.core.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]: # Возвращаемый тип Generator[Session, None, None] означает: генератор yield’ит Session, ничего внутрь не принимает (.send не используется), и ничего не возвращает (return без значения → None).
  """
  Зависимость для получения сессии базы данных.
  Создаёт новую сессию для каждого запроса и закрывает её после обработки.
  """
  db: Session = SessionLocal()
  try: # Гарантирует закрытие сессии (db.close()) после выполнения запроса, даже если произойдёт ошибка.
    yield db # Если написать return, до db.close() функция не доберётся, в итоге сессия останется открытой в памяти.
  finally:
    db.close()


SessionDep = Annotated[Session, Depends(get_db)]
