import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv("../.env")

def get_client_id():
    return os.getenv("CLIENT_ID")

def get_client_secret():
    return os.getenv("CLIENT_SECRET")

# Function to get access token
def get_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials'
    }, auth=HTTPBasicAuth(client_id, client_secret))

    auth_response_data = auth_response.json()
    return auth_response_data['access_token']

# Function to get song data
def get_song_data(song_id):

    client_id = get_client_id()

    client_secret = get_client_secret()

    access_token = get_access_token(client_id, client_secret)
    base_url = 'https://api.spotify.com/v1/tracks/'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(base_url + song_id, headers=headers)
    return response.json()

def get_song_features(song_id):

    client_id = get_client_id()

    client_secret = get_client_secret()

    access_token = get_access_token(client_id, client_secret)
    base_url = 'https://api.spotify.com/v1/audio-features/'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(base_url + song_id, headers=headers)
    return response.json()
