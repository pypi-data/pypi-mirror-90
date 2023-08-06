# -*- coding: utf-8 -*-

def company(item):
    """
    Получить данные запрошенного Юрлица/ИП

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
    district = address.get('federal_district', None)
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
        'district': district if district else None,
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


def address(item):
    """
    Получить данные по запрошенному адресу

    :param item: элемент из списка "suggestions"
    :type item: dict

    :rtype: dict
    :return: Словарь значений
    """
    address_full = item.get('unrestricted_value', None)
    data = item.get('data', {})
    is_town = data.get('city_kladr_id', None)

    if is_town:
        place_fias_id = data.get('city_fias_id', None)
        place_kladr_id = data.get('city_kladr_id', None)
    else:
        place_fias_id = data.get('settlement_fias_id', None)
        place_kladr_id = data.get('settlement_kladr_id', None)

    result = {
        'address_full': address_full,
        'geo_lat': data.get('geo_lat', None),
        'geo_lon': data.get('geo_lon', None),
        'postal_code': data.get('postal_code', None),
        'federal_district': data.get('federal_district', None),
        'region_fias_id': data.get('region_fias_id', None),
        'region_kladr_id': data.get('region_kladr_id', None),
        'place_fias_id': place_fias_id,
        'place_kladr_id': place_kladr_id,
        'street_fias_id': data.get('street_fias_id', None),
        'street_kladr_id': data.get('street_kladr_id', None),
        'house_fias_id': data.get('house_fias_id', None),
        'house_kladr_id': data.get('house_kladr_id', None),
        'fias_id': data.get('fias_id', None),
        'fias_code': data.get('fias_code', None),
        'kladr_id': data.get('kladr_id', None),
    }

    return result
