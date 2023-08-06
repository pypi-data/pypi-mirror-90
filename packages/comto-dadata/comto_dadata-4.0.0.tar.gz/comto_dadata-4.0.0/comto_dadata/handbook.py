# -*- coding: utf-8 -*-
import http.client

site = 'suggestions.dadata.ru'


def okved(token, okved):
    """
    Получить вид деятельности по коду (ОКВЭД 2)

    :param token: API-ключ
    :type token: str
    :param okved: код ОКВЕД
    :type okved: str

    :rtype: str
    :return: JSON-строка, где в ключе "suggestions" список словарей
    """
    ready_payload = '{"query": "%s"}' % okved
    url = '/suggestions/api/4_1/rs/findById/okved2'
    return _request(site, token, ready_payload, url)


def okpd(token, okpd):
    """
    Получить вид продукции по коду (ОКПД 2)

    :param token: API-ключ
    :type token: str
    :param okpd: код ОКПД
    :type okpd: str

    :rtype: str
    :return: JSON-строка, где в ключе "suggestions" список словарей
    """
    ready_payload = '{"query": "%s"}' % okpd
    url = '/suggestions/api/4_1/rs/findById/okpd2'
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
