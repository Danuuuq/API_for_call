from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_async_session
from app.core.logging import action_url_logger, db_logger
from app.crud.phones import phone_crud
from app.schemas.calling import Calling, ResultCall
from app.schemas.phones import PhoneBase, PhoneUpdateBase
from app.services.action_url import make_call


router = APIRouter()

@router.post('/call')
async def make_call_from_bitrix(
    call_info: Calling,
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    if request.client.host not in settings.ip_service:
        action_url_logger.error(f'Запрос на звонок с IP:{request.client.host}')
        return JSONResponse(status_code=403,
                            content={'result': 'Доступ запрещен!'})
    return await make_call(call_info, session)


@router.post('/phones')
async def update_or_create_table_phone(
    obj_in: PhoneBase | list[PhoneBase],
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    if request.client.host not in settings.ip_mkd:
        db_logger.error(f'Запрос к БД с IP:{request.client.host}')
        return JSONResponse(status_code=403,
                            content={'result': 'Доступ запрещен!'})
    await phone_crud.create_or_update_objects(obj_in, session)


@router.patch('/phones')
async def update_table_phone(
    obj_in: PhoneUpdateBase,
    request: Request,
    session: AsyncSession = Depends(get_async_session)
) -> PhoneBase:
    if request.client.host not in settings.ip_mkd:
        db_logger.error(f'Запрос к БД с IP:{request.client.host}')
        return JSONResponse(status_code=403,
                            content={'result': 'Доступ запрещен!'})
    db_obj = await phone_crud.get_by_number(obj_in.phone_number, session)
    if db_obj:
        return await phone_crud.update(db_obj, obj_in, session)
    else:
        db_logger.error(f'Номер {obj_in.phone_number} отсутствует в БД')
        return JSONResponse(status_code=404,
                            content={'result': 'Объекта нет в БД!'})
