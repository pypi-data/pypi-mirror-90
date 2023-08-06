# -*- coding: utf-8 -*-
import http.client

domain_suggest = 'suggestions.dadata.ru'
domain_clean = 'cleaner.dadata.ru'


def suggest(token, query):
    """
    Поиск адреса по любой части адреса от региона до дома, а так же - по почтовому индексу

    :param token: API-ключ
    :type token: str
    :param query: адрес
    :type query: str

    :rtype: str
    :return: JSON-строка, где в ключе "suggestions" список словарей
    """
    ready_payload = '{"query": "%s"}' % query
    url = '/suggestions/api/4_1/rs/suggest/address'
    return _request(domain_suggest, token, ready_payload, url)


def geocoding(token, secret, address):
    """
    Геокодирование (координаты по адресу)

    :param token: API-ключ
    :type token: str
    :param secret: Секретный ключ для стандартизации
    :type secret: str
    :param address: адрес
    :type address: str

    :rtype: str
    :return: JSON-строка, где в ключе "suggestions" список словарей
    """
    ready_payload = '["%s"]' % address
    url = '/api/v1/clean/address'
    return _request(domain_clean, token, ready_payload, url, secret)


def geocoding_reverse(token, lat, lon):
    """
    Обратное геокодирование (адрес по координатам)

    :param token: API-ключ
    :type token: str
    :param lat: широта
    :type lat: str
    :param lon: долгота
    :type lon: str

    :rtype: str
    :return: JSON-строка, где в ключе "suggestions" список словарей
    """
    url = '/suggestions/api/4_1/rs/geolocate/address?lat=%s&lon=%s' % (lat, lon)
    return _request(domain_suggest, token, '', url, '', 'GET')


def by_ip(token, ip):
    """
    Получить город по IP-адресу

    :param token: API-ключ
    :type token: str
    :param ip: IP-адрес
    :type ip: str

    :rtype: str
    :return: JSON-строка, где в ключе "suggestions" список словарей
    """
    url = '/suggestions/api/4_1/rs/iplocate/address?ip=%s' % ip
    return _request(domain_suggest, token, '', url, '', 'GET')


def by_fias(token, fias):
    """
    Получить адрес по коду КЛАДР или ФИАС

    :param token: API-ключ
    :type token: str
    :param fias: код КЛАДР или ФИАС
    :type fias: str

    :rtype: str
    :return: JSON-строка, где в ключе "suggestions" список словарей
    """
    ready_payload = '{"query": "%s"}' % fias
    url = '/suggestions/api/4_1/rs/findById/address'
    return _request(domain_suggest, token, ready_payload, url)


def postal_unit(token, street):
    """
    Получить ближайшее почтовое отделение по адресу или индексу

    :param token: API-ключ
    :type token: str
    :param street: адрес или индекс
    :type street: str

    :rtype: str
    :return: JSON-строка, где в ключе "suggestions" список словарей
    """
    ready_payload = '{"query": "%s"}' % street
    url = '/suggestions/api/4_1/rs/suggest/postal_unit'
    return _request(domain_suggest, token, ready_payload, url)


def delivery_uid(token, kladr):
    """
    Получить идентификатор города в СДЭК, Boxberry и DPD

    :param token: API-ключ
    :type token: str
    :param kladr: код ФИАС или КЛАДР
    :type kladr: str

    :rtype: str
    :return: JSON-строка, где в ключе "suggestions" список словарей
    """
    ready_payload = '{"query": "%s"}' % kladr
    url = '/suggestions/api/4_1/rs/findById/delivery'
    return _request(domain_suggest, token, ready_payload, url)


def dict_by_fias(token, fias):
    """
    Найти адрес в справочнике ФИАС по коду КЛАДР или ФИАС

    :param token: API-ключ
    :type token: str
    :param fias: код ФИАС или КЛАДР
    :type fias: str

    :rtype: str
    :return: JSON-строка, где в ключе "suggestions" список словарей
    """
    ready_payload = '{"query": "%s"}' % fias
    url = '/suggestions/api/4_1/rs/findById/fias'
    return _request(domain_suggest, token, ready_payload, url)


def country(token, code):
    """
    Получить описание страны по коду (RU, DE, US)

    :param token: API-ключ
    :type token: str
    :param code: Справочник стран мира по стандарту ISO 3166
    :type code: str

    :rtype: str
    :return: JSON-строка, где в ключе "suggestions" список словарей
    """
    ready_payload = '{"query": "%s"}' % code
    url = '/suggestions/api/4_1/rs/suggest/country'
    return _request(domain_suggest, token, ready_payload, url)


def _request(domain, token, payload, url, secret='', method="POST"):
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
    :param secret: Секретный ключ для стандартизации
    :type secret: str
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

    if secret:
        headers['X-Secret'] = secret

    conn.request(method, url, payload.encode('utf-8'), headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")
