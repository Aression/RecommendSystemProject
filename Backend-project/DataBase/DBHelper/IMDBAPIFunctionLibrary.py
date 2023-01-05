# Development!
# ART0189

import requests, json

"""
Send all data requests to:

http://www.omdbapi.com/?apikey=[yourkey]&

Poster API requests:

http://img.omdbapi.com/?apikey=[yourkey]&

By ID or Title
Parameter	Required	Valid Options	Default Value	Description
i	Optional*		<empty>	A valid IMDb ID (e.g. tt1285016)
t	Optional*		<empty>	Movie title to search for.
type	No	movie, series, episode	<empty>	Type of result to return.
y	No		<empty>	Year of release.
plot	No	short, full	short	Return short or full plot.
r	No	json, xml	json	The data type to return.
callback	No		<empty>	JSONP callback name.
v	No		1	API version (reserved for future use).
"""

key = '27443fa3'
api_url = 'http://www.omdbapi.com/?apikey={}&i=tt{}'


def RequestBaseInfoById(IMDBId):
    # BaseURL = "https://imdb-api.com/en/API/SearchTitle/k_mjhfqnod/tt"
    URL = api_url.format(key, IMDBId)
    while True:
        requestRes = Request_Internal(URL)
        if requestRes is not None:
            break
    return requestRes


def RequestDetailInfoById(IMDBId):
    # BaseURL = "https://imdb-api.com/en/API/Title/k_mjhfqnod/tt"
    URL = api_url.format(key, IMDBId)
    while True:
        requestRes = Request_Internal(URL)
        if requestRes is not None:
            break
    return requestRes


def Request_Internal(ValidURL):
    Payload = {}
    Headers = {}
    response = requests.request("GET", ValidURL, headers=Headers, data=Payload)
    return json.loads(response.text.encode('utf8'))
