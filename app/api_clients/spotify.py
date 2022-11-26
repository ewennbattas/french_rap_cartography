import os
import json
from functools import lru_cache

import requests
from dotenv import load_dotenv


load_dotenv()


class SpotifyAPI:
    def __init__(self, client_id, client_secret):
        self.AUTH_URL = 'https://accounts.spotify.com/api/token'
        self.BASE_URL = 'https://api.spotify.com/v1/'

        # POST
        auth_response = requests.post(self.AUTH_URL, {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
        })

        # convert the response to JSON
        auth_response_data = auth_response.json()

        # save the access token
        access_token = auth_response_data['access_token']

        self.headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
        }

    @lru_cache()
    def get_response(self, query):
        return requests.get(self.BASE_URL + query, headers=self.headers)

    def get_data_from_response(self, query):
        return json.loads(self.get_response(query).text)

    def get_artist(self, artist_id):
        return self.get_data_from_response(f"artists/{artist_id}")

    def get_album(self, album_id):
        return self.get_data_from_response(f"albums/{album_id}")

    def get_track(self, track_id):
        return self.get_data_from_response(f"tracks/{track_id}")

    def get_artist_albums(self, artist_id):
        return self.get_data_from_response(f"artists/{artist_id}/albums")

    def get_album_tracks(self, album_id):
        return self.get_data_from_response(f"albums/{album_id}/tracks")

    def search_artist(self, artist_name):
        return self.get_data_from_response(f"search?q=artist:{artist_name}&type=artist")

    def get_artist_featurings(self, artist_id=None, artist_name=None):
        if not (artist_id or artist_name):
            raise ValueError("You should specify either artist_id or artist_name")
        if artist_name:
            artist_id = self.search_artist(artist_name)['artists']['items'][0]['id']

        featurings = {}
        albums = self.get_artist_albums(artist_id)['items']
        for album in albums:
            album_id = album['id']
            tracks = self.get_album_tracks(album_id)['items']

            for track in tracks:
                track_id = track['id']
                artists = self.get_track(track_id)['artists']

                for artist in artists:
                    if artist['id'] != artist_id:
                        featurings[(artist['id'], artist['name'])] = {
                            "track": track['name'],
                            "album": album['name']
                        }
        return featurings


if __name__ == "__main__":
    auth_params = {
        "client_id": os.getenv('SPOTIPY_CLIENT_ID'),
        "client_secret": os.getenv('SPOTIPY_CLIENT_SECRET')
    }
    client = SpotifyAPI(**auth_params)
