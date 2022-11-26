import os

from dotenv import load_dotenv

from .api_clients.spotify import SpotifyAPI


load_dotenv()


def add_artist(self, path, id, name, ):
    with open(path, "w") as f:
        f.writelines([
            f'{id},"{name}"'
        ])


def add_feat(self, path, artist_a_id, track, album, artist_b_id):
    with open(path, "w") as f:
        f.writelines([
            f'{artist_a_id},"{track}","{album}",{artist_b_id},FEATED_WITH'
        ])


def add_feats_of_artist(client, artist_name):


if __file__ == "__main__":
    artists_path = "/home/ewennb/Documents/dev/french_rap_cartography/app/data/artists.csv"
    feats_path = "/home/ewennb/Documents/dev/french_rap_cartography/app/data/feats.csv"

    auth_params = {
        "client_id": os.getenv('SPOTIPY_CLIENT_ID'),
        "client_secret": os.getenv('SPOTIPY_CLIENT_SECRET')
    }
    client = SpotifyAPI(**auth_params)
