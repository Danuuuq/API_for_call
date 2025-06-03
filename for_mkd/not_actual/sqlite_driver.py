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
    phones = {
        name_fields[0]: row[0],
        name_fields[1]: row[1],
        name_fields[2]: row[2],
    }
    print(phones)
    json_data = json.dumps(phones, indent=3)
    conn_url = http.client.HTTPConnection(URL)
    conn_url.request('POST', '/phones', body=json_data, headers=HEADERS)

conn_db.close()
