import re
import sqlite3
import http.client
import json

# Перед этим сделайте копию БД в директорию где запускается скрипт.
# Копию лучше выполнять через crontab так как Python медленный
# и создавать копию через него небезопасно
URL = '10.7.83.208:9000'
HEADERS = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}
DB_NAME = 'phones.sqlite'
FILENAME = 'reg_from_mkd.json'

with open(FILENAME, 'r', encoding='utf-8') as file:
    content = file.read()

# Ищем id и IP-адрес в SIP-записи
matches = re.findall(
    r'id="(\d+)";\s+contacts=\{\{\s*"sip:[^@]+@([\d\.]+):\d+"', content)

phones_mkd = {}
for phone_number, ip_address in matches:
    phones_mkd[phone_number] = ip_address

conn_db = sqlite3.connect(DB_NAME)
cursor = conn_db.cursor()

# Получаем данные из БД
query = """
        SELECT last_ip,
               json_extract(json_extract(json_extract(config, '$.features[0]'), '$.params'),'$.phone_number') AS phone_number,
               json_extract(json_extract(json_extract(config, '$.features[0]'), '$.params'), '$.display_name') AS display_name
        FROM phones
        WHERE phone_number not null AND last_ip not null AND display_name not null
"""
cursor.execute(query)
name_fields = [name[0] for name in cursor.description]
rows = cursor.fetchall()

for row in rows:
    if phones_mkd.get(row[1]) is None:
        continue
    phones = {
        name_fields[1]: row[1],
        name_fields[0]: phones_mkd[row[1]],
        name_fields[2]: row[2],
    }
    print(phones)
    json_data = json.dumps(phones, indent=3)
    conn_url = http.client.HTTPConnection(URL)
    conn_url.request('POST', '/phones', body=json_data, headers=HEADERS)

conn_db.close()