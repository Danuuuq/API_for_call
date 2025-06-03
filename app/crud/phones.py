from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import commit_change
from app.models.phones import Phone


class PhoneCRUD:
    def __init__(self, model):
        self.model = model

    async def get_by_number(
        self,
        phone_number: int,
        session: AsyncSession
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.phone_number == phone_number
            )
        )
        return db_obj.scalars().first()

    async def create(
        self,
        obj_in,
        session: AsyncSession
    ):
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        return await commit_change(session, db_obj, 'создание')

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession
    ):
        update_data = obj_in.dict(exclude_unset=True)
        obj_data = jsonable_encoder(db_obj)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        return await commit_change(session, db_obj, 'обновление')

    async def create_or_update_objects(
        self,
        objs_in,
        session: AsyncSession
    ):
        if isinstance(objs_in, list):
            for obj_in in objs_in:
                data_obj = await self.get_by_number(obj_in.phone_number, session)
                if data_obj:
                    await self.update(data_obj, obj_in, session)
                else:
                    await self.create(obj_in, session)
        else:
            data_obj = await self.get_by_number(objs_in.phone_number, session)
            if data_obj:
                await self.update(data_obj, objs_in, session)
            else:
                await self.create(objs_in, session)


phone_crud = PhoneCRUD(Phone)
