import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

# minimal Spotify client
sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-top-read"
))

# making formatting pretty!!
def save_csv_with_spaces(df, filename):
    """Save DataFrame to CSV and insert space after commas."""
    df.to_csv(filename, index=False)
    with open(filename, "r") as f:
        data = f.read()
    data = data.replace(",", ", ")
    with open(filename, "w") as f:
        f.write(data)

# top 50 tracks
top_tracks = sp.current_user_top_tracks(limit=50, time_range='medium_term')
track_tracks = []
track_ids = []
for track in top_tracks['items']:
    track_tracks.append({
        "Song Name": track['name'],
        "Artist Name": track['artists'][0]['name'],
        "Popularity": track['popularity'],
        "Track ID": track['id']
    })
    track_ids.append(track['id'])

df_tracks = pd.DataFrame(track_tracks)
print(df_tracks.head())
save_csv_with_spaces(df_tracks, "top_50_tracks.csv")

# top 50 artists
top_artists = sp.current_user_top_artists(limit=50, time_range='medium_term')
track_artists = []
for artist in top_artists['items']:
    track_artists.append({
        "Artist Name": artist['name'],
        "Popularity": artist['popularity']
    })

df_artists = pd.DataFrame(track_artists)
print(df_artists.head())
save_csv_with_spaces(df_artists, "top_50_artists.csv")


# recently
recently_played = sp.current_user_recently_played(limit=50)
track_songs = []
for item in recently_played['items']:
    track = item['track']
    track_songs.append({
        "Song Name": track['name'],
        "Artist": track['artists'][0]['name'],
        "Played_at": item['played_at'],
        "Popularity": track['popularity']
    })

df_recent = pd.DataFrame(track_songs)
print(df_recent.head())
save_csv_with_spaces(df_recent, "recently_played.csv")

public_playlists = sp.current_user_playlists(limit=50)
playlist_data = []
for item in public_playlists['items']:
    playlist_data.append({
        "Playlist Name": item['name'],
        "Owner": item['owner']['display_name'],
        "Tracks Count": item['tracks']['total'],
        "Href": item['href']
    })

df_playlists = pd.DataFrame(playlist_data)
print(df_playlists.head())
save_csv_with_spaces(df_playlists, "my_playlists.csv")

# user playlists
current_playlists = sp.current_user_playlists(limit=50)

playlist_data = []
all_tracks = []

for item in current_playlists['items']:
    playlist_id = item['id']
    playlist_name = item['name']
    owner = item['owner']['display_name']
    track_count = item['tracks']['total']

    playlist_data.append({
        "Playlist Name": playlist_name,
        "Owner": owner,
        "Tracks Count": track_count,
        "Href": item['href']
    })

    # --- tracks from each playlist ---
    playlist_tracks = sp.playlist_tracks(playlist_id, limit=100)  # adjust limit if you want more
    for track_item in playlist_tracks['items']:
        track = track_item['track']
        if track:  # sometimes local files or empty tracks show up
            all_tracks.append({
                "Playlist Name": playlist_name,
                "Song Name": track['name'],
                "Artist": track['artists'][0]['name'],
                "Popularity": track['popularity']
            })

# save playlists
df_playlists = pd.DataFrame(playlist_data)
print(df_playlists.head())
save_csv_with_spaces(df_playlists, "my_playlists.csv")

# save tracks from playlists
df_playlist_tracks = pd.DataFrame(all_tracks)
print(df_playlist_tracks.head())
save_csv_with_spaces(df_playlist_tracks, "my_playlist_tracks.csv")



