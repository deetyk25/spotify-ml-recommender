import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

load_dotenv()

# minimal Spotify client
sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-top-read"
))

# csv helper
def save_csv_with_spaces(df, filename):
    df.to_csv(filename, index=False)
    with open(filename, "r") as f:
        data = f.read()
    data = data.replace(",", ", ")
    with open(filename, "w") as f:
        f.write(data)

# get top tracks and genres without repeated calls to api
top_tracks = sp.current_user_top_tracks(limit=50, time_range='medium_term')

track_tracks = []
track_ids = []
artist_cache = {} 

for track in top_tracks['items']:
    artist_id = track['artists'][0]['id']

    if artist_id not in artist_cache:
        artist_cache[artist_id] = sp.artist(artist_id)['genres']

    genres = artist_cache[artist_id]

    track_tracks.append({
        "Song Name": track['name'],
        "Artist Name": track['artists'][0]['name'],
        "Popularity": track['popularity'],
        "Genres": " ".join(genres),
        "Track ID": track['id']
    })

    track_ids.append(track['id'])

# retrieve songs from my playlists
df_tracks = pd.DataFrame(track_tracks)
print("\nTop Tracks:")
print(df_tracks.head())

current_playlists = sp.current_user_playlists(limit=50)

all_tracks = []

for item in current_playlists['items']:
    playlist_id = item['id']
    playlist_tracks = sp.playlist_tracks(playlist_id, limit=100)

    for track_item in playlist_tracks['items']:
        track = track_item['track']
        if track:
            all_tracks.append({
                "Song Name": track['name'],
                "Artist": track['artists'][0]['name'],
                "Popularity": track['popularity']
            })

df_playlist_tracks = pd.DataFrame(all_tracks)

# TF-IDF on genres
vectorizer = TfidfVectorizer()
genre_matrix = vectorizer.fit_transform(df_tracks["Genres"])

# Scale popularity
scaler = StandardScaler()
scaled_numeric = scaler.fit_transform(df_tracks[["Popularity"]])

# combine features
combined_features = np.hstack([
    genre_matrix.toarray(),
    scaled_numeric
])

# build user taste profile (centroid)
user_profile = combined_features.mean(axis=0).reshape(1, -1)

# remove songs already in my top 50
candidate_tracks = df_playlist_tracks[
    ~df_playlist_tracks["Song Name"].isin(df_tracks["Song Name"])
].copy()

unique_artists = candidate_tracks["Artist"].unique()
artist_name_to_id = {}

for artist_name in unique_artists:
    results = sp.search(q=artist_name, type="artist", limit=1)

    if results["artists"]["items"]:
        artist_id = results["artists"]["items"][0]["id"]
        artist_name_to_id[artist_name] = artist_id

        # cache genres if not already cached
        if artist_id not in artist_cache:
            artist_cache[artist_id] = sp.artist(artist_id)["genres"]

# assign genres using data
candidate_tracks["Genres"] = candidate_tracks["Artist"].apply(
    lambda x: " ".join(
        artist_cache.get(artist_name_to_id.get(x, ""), [])
    )
)

candidate_tracks = candidate_tracks[candidate_tracks["Genres"] != ""]

cand_genre_matrix = vectorizer.transform(candidate_tracks["Genres"])
cand_numeric = scaler.transform(candidate_tracks[["Popularity"]])

cand_combined = np.hstack([
    cand_genre_matrix.toarray(),
    cand_numeric
])

cand_similarity = cosine_similarity(cand_combined, user_profile)

candidate_tracks["Similarity Score"] = cand_similarity.flatten()

candidate_tracks = candidate_tracks.sort_values(
    by="Similarity Score",
    ascending=False
)

print("\nTop 10 Recommendations From Your Library:")
print(candidate_tracks.head(10))

save_csv_with_spaces(candidate_tracks.head(20), "ranked_recommendations.csv")

print("\nTop 10 Recommendations From Your Library:")
print(candidate_tracks.head(10))


