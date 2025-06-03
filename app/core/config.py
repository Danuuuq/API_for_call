from typing import Optional

from zoneinfo import ZoneInfo

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_title: str = 'Портал взаимодействия с телефонами'
    description: str = 'Сервис для звонков по API и другим взаимодействиям с телефоном'
    database_url: str = 'sqlite+aiosqlite:///./phone.db'
    log_format: Optional[str] = '%(asctime)s - %(levelname)s - %(message)s'
    timezone: ZoneInfo = ZoneInfo('Europe/Moscow')
    admin: Optional[str] = None
    ip_mkd: Optional[list[str]] = None
    ip_service: Optional[list[str]] = None
    pass_adm: Optional[str] = None  
    pass_gs: Optional[str] = None
    pass_sz: Optional[str] = None
    pass_nadym: Optional[str] = None
    pass_urengoy: Optional[str] = None
    pass_noyabrsk: Optional[str] = None
    pass_irkutsk: Optional[str] = None
    pass_reconst: Optional[str] = None
    pass_tomsk: Optional[str] = None
    pass_remont: Optional[str] = None
    pass_sakhalin: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
