# -*- coding: utf-8 -*-
import http.client
import json


def stat(token, secret, service='suggestions'):
    """
    Получить статистику по всем сервисам: стандартизация, подсказки, поиск дублей

    :param token: API-ключ
    :type token: str
    :param secret: Секретный ключ для стандартизации
    :type secret: str
    :param service: Название сервиса
    :type service: str

    :rtype: int
    :return: Количество сделанных запросов по данному токену
    """
    headers = {
        'Authorization': 'Token %s' % token,
        'X-Secret': '%s' % secret
    }
    jsn = _request(headers, "/api/v2/stat/daily")
    return jsn['services'][service]


def balance(token, secret):
    """
    Получить текущий баланс вашего счета

    :param token: API-ключ
    :type token: str
    :param secret: Секретный ключ для стандартизации
    :type secret: str

    :rtype: float
    :return: Сумма в рублях и копейках (9922.30)
    """
    headers = {
        'Authorization': 'Token %s' % token,
        'X-Secret': '%s' % secret
    }
    jsn = _request(headers, "/api/v2/profile/balance")
    return jsn['balance']


def version(token):
    """
    Получить даты актуальности справочников (ФИАС, ЕГРЮЛ, банки и другие)

    :param token: API-ключ
    :type token: str

    :rtype: dict
    :return: JSON как словарь
    """
    headers = {
        'Authorization': 'Token %s' % token
    }
    return _request(headers, "/api/v2/version")


def _request(headers, url):
    """
    Запрос к сервису

    :param headers: Заголовки
    :type headers: dict
    :param url: URL на домене
    :type url: str

    :rtype: str
    :return: JSON-строка, где в ключе "suggestions" список словарей
    """
    conn = http.client.HTTPSConnection('dadata.ru')
    conn.request("GET", url, '', headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))
