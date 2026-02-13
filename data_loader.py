import pandas as pd

def get_source_tracks(sp, taste_mode):
    if taste_mode == "recent":
        recent = sp.current_user_recently_played(limit=50)
        return [item["track"] for item in recent["items"]]
    else:
        top_tracks = sp.current_user_top_tracks(
            limit=50,
            time_range=taste_mode
        )
        return top_tracks["items"]


def build_user_track_dataframe(sp, source_tracks, artist_cache):
    tracks_data = []

    for track in source_tracks:
        artist_id = track['artists'][0]['id']

        if artist_id not in artist_cache:
            artist_cache[artist_id] = sp.artist(artist_id)['genres']

        genres = artist_cache[artist_id]

        tracks_data.append({
            "Song Name": track['name'],
            "Artist Name": track['artists'][0]['name'],
            "Popularity": track['popularity'],
            "Genres": " ".join(genres),
            "Track ID": track['id']
        })

    return pd.DataFrame(tracks_data)


def get_playlist_tracks(sp):
    playlists = sp.current_user_playlists(limit=50)
    all_tracks = []

    for item in playlists['items']:
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

    df = pd.DataFrame(all_tracks)
    return df.drop_duplicates(subset=["Song Name", "Artist"])