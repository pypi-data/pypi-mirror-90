# -*- coding: utf-8 -*-
import http.client
import json

site = 'suggestions.dadata.ru'

"""
Пример словаря "payload"

payload = {
    'query': 'Иванов Александр',
    'count': 20,
    'status': ["ACTIVE"],
    'locations': [{"kladr_id": "1300000100000"}],
}
"""


def suggest(token, payload):
    """
    Расширенный поиск компаний и индивидуальных предпринимателей

    :param token: API-ключ
    :type token: str
    :param payload: Словарь для формирования запроса
    :type payload: dict

    :rtype: str
    :return: JSON-строка, где в ключе "suggestions" список словарей
    """
    ready_payload = json.dumps(payload)
    url = '/suggestions/api/4_1/rs/suggest/party'
    return _request(site, token, ready_payload, url)


def by_inn(token, inn):
    """
    Поиск компаний и индивидуальных предпринимателей по ИНН или ОГРН

    :param token: API-ключ
    :type token: str
    :param inn: искомый ИНН или ОГРН
    :type inn: str

    :rtype: str
    :return: JSON-строка, где в ключе "suggestions" список словарей
    """
    ready_payload = '{"query": "%s"}' % inn
    url = '/suggestions/api/4_1/rs/findById/party'
    return _request(site, token, ready_payload, url)


def affiliated(token, inn):
    """
    Поиск аффилированных компаний по ИНН

    :param token: API-ключ
    :type token: str
    :param inn: искомый ИНН
    :type inn: str

    :rtype: str
    :return: JSON-строка, где в ключе "suggestions" список словарей
    """
    ready_payload = '{"query": "%s"}' % inn
    url = '/suggestions/api/4_1/rs/findAffiliated/party'
    return _request(site, token, ready_payload, url)


def _request(domain, token, payload, url, method="POST"):
    """
    Запрос к сервису

    :param domain: Запрашиваемый домен
    :type domain: str
    :param token: Токен (API-ключ)
    :type token: str
    :param payload: Запрос
    :type payload: str
    :param url: URL на домене
    :type url: str
    :param method: Тип запроса
    :type method: str

    :rtype: str
    :return: JSON-строка, где в ключе "suggestions" список словарей
    """
    conn = http.client.HTTPSConnection(domain)

    headers = {
        'Authorization': 'Token %s' % token,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    conn.request(method, url, payload.encode('utf-8'), headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")
