# DaData Commercito
Пакет для работы с сервисом "[dadata.ru](https://dadata.ru/ "Информация о клиентах и контрагентах")".  
Его удобно использовать совместно с пакетом "[comto-core](https://pypi.org/project/comto-core/ "Набор полезных функций для повседневной работы")".

## Использование

### Поиск адресов
```python
from comto_dadata import address

token = 'your-token'
secret = 'your-secret'

print(address.suggest(token, 'москва твер'))
print(address.geocoding(token, secret, "москва сухонская 11"))
print(address.geocoding_reverse(token, '55.878', '37.653'))
print(address.by_ip(token, '46.226.227.20'))
print(address.by_fias(token, '9120b43f-2fae-4838-a144-85e43c2bfb29'))
print(address.postal_unit(token, 'дежнева 2а'))
print(address.delivery_uid(token, '3100400100000'))
print(address.dict_by_fias(token, '9120b43f-2fae-4838-a144-85e43c2bfb29'))
print(address.country(token, 'DE'))
```

### Поиск компаний
```python
from comto_dadata import company

payload = {
    'query': 'Иванов Александр',
    'count': 20,
    'status': ["ACTIVE"],
    'locations': [{"kladr_id": "1300000100000"}],
}

response = company.suggest('your-token', payload)
```

### Справочники

```python
from comto_dadata import handbook

okved = handbook.okved('your-token', '51.22.3')
okpd = handbook.okpd('your-token', '95.23.10.133')
```

### Личный кабинет

```python
from comto_dadata import profile

stat = profile.stat('your-token', 'your-secret')
balance = profile.balance('your-token', 'your-secret')
version = profile.version('your-token')
```

### Парсинг ответа сервиса

```python
import json
from comto_dadata import company
from comto_dadata import parse

response = company.by_inn('your-token', '1327048147')
print(response)
response = json.loads(response)
items = response.get('suggestions')
if len(items):
    for item in items:
        person = parse.company(item)
        print(person)
```

Пример парсинга ответа

```json
{
	"inn": "1327048147",
	"fio": "Иванов Иван Иванович",
	"type": "LEGAL",
	"name": "ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО \"СПЕЦИАЛИЗИРОВАННЫЙ ЗАСТРОЙЩИК \"ДОМОСТРОИТЕЛЬНЫЙ КОМБИНАТ\"",
	"region": "Респ Мордовия",
	"kladr_region": "1300000000000",
	"city": "г Саранск",
	"kladr_city": "1300000100000",
	"employee": 78,
	"okved": "41.20",
	"okveds": "41.20, 01.41, ..., 85.42"
}
```