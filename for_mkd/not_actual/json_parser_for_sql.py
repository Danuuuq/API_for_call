import re
import http.client
import json

FILENAME = 'reg_from_mkd.json'

with open(FILENAME, 'r', encoding='utf-8') as file:
    content = file.read()

# Ищем id и IP-адрес в SIP-записи
matches = re.findall(
    r'id="(\d+)";\s+contacts=\{\{\s*"sip:[^@]+@([\d\.]+):\d+"', content)

phones = {}
# Выводим результат
for phone_number, ip_address in matches:
    phones[phone_number] = ip_address
print(phones)
