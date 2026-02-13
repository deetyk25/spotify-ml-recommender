import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


def build_user_profile(df_tracks):
    vectorizer = TfidfVectorizer()
    genre_matrix = vectorizer.fit_transform(df_tracks["Genres"])

    scaler = StandardScaler()
    scaled_numeric = scaler.fit_transform(df_tracks[["Popularity"]])

    combined = np.hstack([
        genre_matrix.toarray(),
        scaled_numeric
    ])

    user_profile = combined.mean(axis=0).reshape(1, -1)

    return vectorizer, scaler, user_profile


def rank_candidates(sp, df_tracks, df_playlist_tracks, vectorizer, scaler, user_profile, artist_cache):
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

            if artist_id not in artist_cache:
                artist_cache[artist_id] = sp.artist(artist_id)["genres"]

    candidate_tracks["Genres"] = candidate_tracks["Artist"].apply(
        lambda x: " ".join(
            artist_cache.get(artist_name_to_id.get(x, ""), [])
        )
    )

    candidate_tracks = candidate_tracks[candidate_tracks["Genres"] != ""]

    genre_matrix = vectorizer.transform(candidate_tracks["Genres"])
    numeric = scaler.transform(candidate_tracks[["Popularity"]])

    combined = np.hstack([
        genre_matrix.toarray(),
        numeric
    ])

    similarity = cosine_similarity(combined, user_profile)
    candidate_tracks["Similarity Score"] = similarity.flatten()

    return candidate_tracks.sort_values(
        by="Similarity Score",
        ascending=False
    )