# -*- coding: utf-8 -*-

def company(item):
    """
    Получить данные Юрлица/ИП

    :param item: элемент из списка "suggestions"
    :type item: dict

    :rtype: dict
    :return: Словарь значений: inn, fio, type, name, region, kladr_region, city, kladr_city, employee, okved, okveds
    """
    data = item.get('data', {})
    fio = None
    name = None

    who = data.get('type', None)
    if who == 'LEGAL':
        fio = data.get('management', {}).get('name', None)
        name = data.get('name', {}).get('full_with_opf', None)
    elif who == 'INDIVIDUAL':
        fio = data.get('name', {}).get('full', None)
        name = data.get('opf', {}).get('full', None)

    address = data.get('address', {}).get('data', {})
    kladr_region = address.get('region_kladr_id', None)
    kladr_city = address.get('city_kladr_id', None)
    region = address.get('region_with_type', None)
    city = address.get('city_with_type', None)
    employee = data.get('employee_count', None)

    result = {
        'inn': data.get('inn', None),
        'fio': fio,
        'type': data.get('type', None),
        'name': name,
        'region': region if region else None,
        'kladr_region': kladr_region if kladr_region else None,
        'city': city if city else None,
        'kladr_city': kladr_city if kladr_city else None,
        'employee': employee if employee else None,
        'okved': data.get('okved', None),
        'okveds': None,
    }

    okveds = data.get('okveds', None)

    if isinstance(okveds, list):
        okvs = []
        for okv in okveds:
            okvs.append(okv['code'])
        result['okveds'] = ', '.join(okvs)

    return result
