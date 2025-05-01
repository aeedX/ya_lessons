import requests


def get_params(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        pass

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    pt = toponym["Point"]["pos"].replace(' ', ',')
    bbox = '~'.join(data.replace(' ', ',') for data in toponym['boundedBy']['Envelope'].values())

    apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

    map_params = {
        'bbox': bbox,
        'pt': pt,
        "apikey": apikey}

    return map_params