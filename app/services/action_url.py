from fastapi.responses import JSONResponse
from urllib.request import build_opener, HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, HTTPSHandler
import ssl

from app.core.config import settings
from app.core.logging import action_url_logger
from app.crud.phones import phone_crud
from app.services.search_password import get_password_for_number


async def send_call(caller, called):
    url = f'https://{caller.last_ip}/servlet?key=number={called}'
    # url = f'https://10.83.196.19/servlet?key=number={called}'
    # context = ssl._create_unverified_context()
    # Решение проблемы с SSL для старых ТА
    password_phone = get_password_for_number(str(caller.phone_number))
    if password_phone is None:
        action_url_logger.info(f'Не удалось подобрать пароль для номера {phone_number}')
        return JSONResponse(status_code=404,
                            content=f'Не найдены данные для данного номера')
    context = ssl.create_default_context()
    context.check_hostname=False
    context.verify_mode=ssl.CERT_NONE
    context.set_ciphers('DEFAULT@SECLEVEL=1')

    https_handler = HTTPSHandler(context=context)
    password_mgr = HTTPPasswordMgrWithDefaultRealm()
    # password_mgr.add_password(None, url, settings.admin, settings.pass_adm)
    password_mgr.add_password(None, url, settings.admin, password_phone)
    auth_handler = HTTPBasicAuthHandler(password_mgr)
    opener = build_opener(auth_handler, https_handler)
    try:
        response = opener.open(url)
    except Exception as error:
        action_url_logger.error(f'URL: {url}, From {caller.phone_number} error: {error}')
        return JSONResponse(status_code=500,
                            content=f'Ошибка совершения вызова')
    else:
        action_url_logger.info(f'From: {caller.last_ip} - {caller.display_name} - {caller.phone_number} To: {called}')
        return JSONResponse(status_code=200,
                            content=f'Вызов успешно выполнен.')


async def make_call(call_info, session):
    caller = await phone_crud.get_by_number(call_info.caller, session)
    if not caller:
        action_url_logger.error(f'Абонент: {call_info.caller} отсутствует в БД')
        return JSONResponse(status_code=404,
                           content={'result': f'Номер {call_info.caller} не найден'})
    elif call_info.name_caller != caller.display_name.split(' ')[0]:
        action_url_logger.error(f'Пришли данные: "{call_info.name_caller}" в БД фамилия: "{caller.display_name}"')
        return JSONResponse(status_code=400,
                           content={'result': 'Фамилии не совпадают!'})
    # Реализовать проверку что телефон  с которого будет выполняться вызов
    # номер совпадает с тем, который пришел от Битрикса
    return await send_call(caller, call_info.called)