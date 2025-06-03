import re
import http.client
import json

URL = '10.7.83.208:9000'
HEADERS = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}
FILENAME = 'reg_from_mkd.json'

with open(FILENAME, 'r', encoding='utf-8') as file:
    content = file.read()

# Ищем id и IP-адрес в SIP-записи
matches = re.findall(
    r'id="(\d+)";\s+contacts=\{\{\s*"sip:[^@]+@([\d\.]+):\d+"', content)

# Выводим результат
for phone_number, ip_address in matches:
    phones = {'phone_number': phone_number, 'last_ip': ip_address}
    json_data = json.dumps(phones, indent=3)
    conn_url = http.client.HTTPConnection(URL)
    conn_url.request('PATCH', '/phones', body=json_data, headers=HEADERS)
    response = conn_url.getresponse()
    if response.status != 200:
        response_data = response.read().decode()
        print(response_data + phone_number)
