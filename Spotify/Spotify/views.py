from django.shortcuts import render,  redirect
from django.shortcuts import HttpResponse
import requests
import base64
import json

def Home(request):
    return render(request, 'Spotify/home.html')

def Search(request):
    if(request.method == "POST"):
        name  = request.POST.get('name')
        country = request.POST.get('country')
    client_id = "f8ad59ad353f4c99bce1e6e296e20ff6"
    client_secret = "f2a7160da48a44fe9e02cdd1f6c79722"

    def get_token():
        auth_string = client_id + ":" + client_secret
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization" : 'Basic ' + auth_base64,
            "Content-type" : "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        result = requests.post(url, headers=headers, data=data)
        json_results = json.loads(result.content)     # converts json string into python dictionary.
        token = json_results['access_token']
        return token

    def get_auth_header(token):
        return {"Authorization": "Bearer " + token}

    def get_artist(artist_name, token):
        url = "https://api.spotify.com/v1/search"
        query = f"?q={artist_name}&type=artist&limit=1"
        header = get_auth_header(token)
        query_url = url + query
        result = requests.get(query_url, headers=header)
        data = json.loads(result.content)
        if len(data) == 0:
            return "No artist matched the name"
        else:
            return data['artists']['items'][0]
        
    def get_tracks(token, artist_id):
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country="+country
        header = get_auth_header(token)
        result = requests.get(url, headers=header)
        data = json.loads(result.content)['tracks']
        return data

    token = get_token()
    print(token)

    artist = get_artist(name, token)
    artists_id = artist['id']
    songs = get_tracks(token, artists_id)
    # print(songs)
    song_names = []

    for idx, song in enumerate(songs):
        song_names.append(f"{song['name']}")
    
    params = {'name': name, 'songs': song_names}
    
    return render(request, 'Spotify/result.html', params)