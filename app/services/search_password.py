import re

from app.core.config import settings
from app.core.logging import action_url_logger

# Шаблоны номерного плана
number_plan = {
    "Администрация": [r"33\d{3}", r"34\d{3}"],
    "ГС": [r"32[2-5]\d{2}"],
    "СЗ": [r"35[4-9]\d{2}"],
    "Надым": [r"190\d{2}", r"178[89]\d?", r"1790\d?"],
    "Новый Уренгой": [r"17[5-7]\d{2}", r"178[0-7]\d?", r"179[1-9]\d?"],
    "Ноябрьск": [r"18[5-8]\d{2}"],
    "Иркутск": [r"18[0-4]\d{2}", r"189\d{2}"],
    "Реконструкция": [r"12\d{3}", r"35[23]\d{2}"],
    "Томск": [r"19[5-9]\d{2}", r"112\d{2}"],
    "Ремонт": [r"13\d{3}"],
    "Сахалин": [r"11[0-1]\d{2}"],
}

# Пароли по направлениям
region_passwords = {
    "Администрация": settings.pass_adm,
    "ГС": settings.pass_gs,
    "СЗ": settings.pass_sz,
    "Надым": settings.pass_nadym,
    "Новый Уренгой": settings.pass_urengoy,
    "Ноябрьск": settings.pass_noyabrsk,
    "Иркутск": settings.pass_irkutsk,
    "Реконструкция": settings.pass_reconst,
    "Томск": settings.pass_tomsk,
    "Ремонт": settings.pass_remont,
    "Сахалин": settings.pass_sakhalin,
}

# Получить направление по номеру
def find_region(phone_number: str) -> str | None:
    for region, patterns in number_plan.items():
        for pattern in patterns:
            if re.fullmatch(pattern, phone_number):
                return region
    return None

# Получить пароль по номеру
def get_password_for_number(phone_number: str) -> str | None:
    region = find_region(phone_number)
    if region:
        return region_passwords.get(region)
    return None
