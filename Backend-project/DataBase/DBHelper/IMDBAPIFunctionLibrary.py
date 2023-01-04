# Development!
# ART0189

import requests, json


def RequestBaseInfoById(IMDBId):
    BaseURL = "https://imdb-api.com/en/API/SearchTitle/k_mjhfqnod/tt"
    URL = BaseURL + IMDBId
    return Request_Internal(URL)


def RequestDetailInfoById(IMDBId):
    BaseURL = "https://imdb-api.com/en/API/Title/k_mjhfqnod/tt"
    URL = BaseURL + IMDBId
    return Request_Internal(URL)


def Request_Internal(ValidURL):
    Payload = {}
    Headers = {}
    response = requests.request("GET", ValidURL, headers=Headers, data=Payload)
    return json.loads(response.text.encode('utf8'))
