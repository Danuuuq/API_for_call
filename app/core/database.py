from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from sqlalchemy import Column, Integer, func, DateTime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker, Mapped, mapped_column

from app.core.config import settings
from app.core.logging import db_logger


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)
    update_at: Mapped[datetime] = mapped_column(DateTime(),
        default=lambda: datetime.now(settings.timezone),
        onupdate=lambda: datetime.now(settings.timezone)
    )


engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session


async def commit_change(session: AsyncSession, obj=None, action=None):
    """Безопасное выполнение сохранения в БД"""
    try:
        await session.commit()
        if obj:
            await session.refresh(obj)
    except SQLAlchemyError as error:
        await session.rollback()
        db_logger.error(f'Ошибка применения действий в БД: {error}')
        raise HTTPException(
            status_code=500,
            detail='Ошибка сохранения в БД, сообщите администратору')
    else:
        db_logger.info(f'Успешное {action} абонента {obj.phone_number}')
        return obj