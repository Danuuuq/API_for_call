# 📞 Корпоративный сервис вызовов по actionURL

FastAPI-сервис для интеграции корпоративного веб-портала с IP-телефонией на базе Протей. Позволяет инициировать вызовы на рабочие телефоны сотрудников по нажатию кнопки на портале (actionURL).   
Для авторизации пользователей используется внешний бэкенд с SSO авторизацией через AD, что обеспечивает поступление качественных данных.

---

## 🚀 Возможности

* Обработка URL-запросов с корпоративного портала
* Генерация actionURL-запросов к телефонным аппаратам (ТА)
* Перебор паролей для доступа к ТА филиалов
* Логирование действий и ошибок
* Фильтрация доступа по IP-адресам
* Создание/обновление таблицы телефонов
* Обновление отдельных записей в таблице по номеру

---
## 📦 API Эндпоинты

### `POST /call`

Инициировать звонок между двумя абонентами

**Payload:**

```json
{
  "caller": 101,
  "name_caller": "Иванов И.И.",
  "called": 202
}
```

**Response:**

```json
{
  "result": "Вызов запущен"
}
```

---

### `POST /phones`

Создать или обновить список телефонов (один или несколько)

**Payload:**

```json
[
  {
    "phone_number": 101,
    "user_name": "Иванов И.И."
  },
  {
    "phone_number": 102,
    "user_name": "Петров П.П."
  }
]
```

---

### `PATCH /phones`

Обновить пользователя по номеру телефона

**Payload:**

```json
{
  "phone_number": 101,
  "user_name": "Новое имя"
}
```

---

## 🔐 Безопасность

* **IP-фильтрация**: разрешены только IP-адреса, указанные в `settings.ip_service` и `settings.ip_mkd`
* **Без авторизации**: проверка выполняется только по IP, без токенов и логинов

---

## 🛠 Технологии

* **FastAPI** — основной backend-фреймворк
* **Uvicorn** — ASGI-сервер
* **Pydantic** — валидация входных данных
* **logging** — логирование запросов и статуса

---

## ⚙️ Пример запроса

```http
POST /call
Authorization: Bearer <your_token>

{
  "extension": "101",
  "target_number": "+79001234567"
}
```



### Запуск приложения:  
1. В директории: `/home/conference/api_for_call` выполнить:  `. venv/bin/activate`  
2. В директории: `/home/conference/api_for_call/app` выполнить: `uvicorn app.main:app --reload --host 10.7.83.208 --port 9000`  

Обновление БД номеров выполнять на АТС:  
1. Копирование Базы данных в директорию с скриптом  
cp /home/protei/Protei-PPS/Server/data/data.sqlite /home/support/database_for_api/phones.sqlite  
2. Отправка актуальных данных на сервер:  
python3 sqlite_drivers.py  
или
python3 sqlite_drivers_bulk.py

Актуальные IP адреса для телефонов:
1. Скопировать файл базы МКД
cp /home/protei/Protei-MKD/MKD/profiles/registrations.db /home/support/database_for_api/reg_from_mkd.json
Выполнить python3 json_parser.py 

Интеграция филиалов в API(загрузка и обновление данных):  
Выполнять первый раз:  
0. Все под sudo su;  
1. Создаем директорию /home/support/data_for_api: mkdir data_for_api  
Выполнять когда добавляются новые абонементы:  
2. Копируем БД с ППС: cp /home/protei/Protei-PPS/Server/data/data.sqlite /home/support/data_for_api/phones.sqlite 
3. Копируем json с МКД с актуальными IP-адресами: cp /home/protei/Protei-MKD/MKD/profiles/registrations.db /home/support/data_for_api/reg_from_mkd.json  
4. Запускаем скрипт по загрузке абонентов с БД ППС и МКД: python3 sqlite_driver.py   
Выполняем для обновления IP адресов на актуальные:  
3. Копируем json с МКД с актуальными IP-адресами: cp /home/protei/Protei-MKD/MKD/profiles/registrations.db /home/support/data_for_api/reg_from_mkd.json 
5. Обновить IP адреса абонентов (можно проверить кого нет в БД) на актуальные с МКД: python3 json_update.py{jh}

Скрипт по работе с данными:
1. chmod +x manage_data.sh  
2. ./manage_data.sh  
3. Выбор действий:  
echo "1. 🔧 Инициализация (первая выгрузка данных)"  
echo "2. ➕ Добавить новых пользователей"  
echo "3. 🌐 Обновить IP адреса"  
