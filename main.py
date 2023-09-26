import json
import base64
import webbrowser
from urllib.parse import urlencode
import requests



#Сначала надо получить CLIENT_ID и CLIENT_SECRETE из оф. сайта spotify
CLIENT_ID = 'enter your client_id'
CLIENT_SECRET = 'enter your client_secret'


#функция получения токена для написания последующих запросов
def get_token():
    auth_string = CLIENT_ID + ":" + CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = requests.post(url, headers=headers, data=data)
    json_result = json.loads(result.content)

    access_token = json_result["access_token"]
    return access_token

#функция авторизации в spotify
def get_auth_header():
    token = get_token()
    return {"Authorization" : "Bearer " +token}

#функция получения url трека
def get_track_url(Track_url):
    parts = Track_url.split('track/')
    part = parts[1]
    Track_id = part
    return (Track_id)

#Функцция запроса метаинформации трека
def get_Track_Metainfo(Track_url):
    Track_id = get_track_url(Track_url)
    header = get_auth_header()
    url = "https://api.spotify.com/v1/tracks/"
    query = url + Track_id

    response = requests.get(query,headers=header)
    json_result = json.loads(response.content)

    return json_result

#Функция получения url плейлиста
def get_Playlist_url(Playlist_url):
    parts = Playlist_url.split('/playlist/')
    part = parts[1]
    playlist_id = part
    return (playlist_id)

#Функция запроса состава плейлиста
def get_playlist_items(Playlist_url):
    Playlist_id =  get_Playlist_url(Playlist_url)
    header = get_auth_header()
    url = "https://api.spotify.com/v1/playlists/" + Playlist_id
    response = requests.get(url,headers=header)
    json_result = response.json()
    valueList = json_result

#Пример запроса на вывод автор-название трека, можно кастомизировать по желанию
    for i in range(len(json_result["tracks"]["items"])):
        print(valueList['tracks']['items'][i]["track"]['artists'][0]['name'] + ': ' +
              valueList['tracks']['items'][i]["track"]['name'])

    return valueList


#Функция авторизации аккаунта и получения разрешений
def Authorization():
    #SCOPE = 'user-read-private user-read-email user-read-playback-state user-modify-playback-state user-read-recently-played user-top-read playlist-read-private'
    auth_headers = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": "http://localhost:7777/callback",
        "scope": "user-library-read playlist-read-private playlist-modify-public",


    }

    webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))


#Функция получения сохраненных треков пользователя
def get_my_saved_track():
    url = "https://api.spotify.com/v1/me/tracks"
    headers = get_auth_header()
    result = requests.get(url = url,headers=headers)
    json_result = result.json()
    print(json_result)


if __name__ == '__main__':
    #Пример использования
    print(get_Track_Metainfo('https://open.spotify.com/track/04KS4huulIeXs5jjHV2QfE?si=7672f34850ba45e3'))
    print(get_playlist_items("https://open.spotify.com/playlist/37i9dQZF1DWT6MhXz0jw61"))