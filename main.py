import sys
from spotify_client import get_spotify_client
from data_loader import (
    get_source_tracks,
    build_user_track_dataframe,
    get_playlist_tracks
)
from recommender import build_user_profile, rank_candidates
from utils import save_csv_with_spaces


def main():
    taste_mode = sys.argv[1] if len(sys.argv) > 1 else "medium_term"

    sp = get_spotify_client()
    artist_cache = {}

    source_tracks = get_source_tracks(sp, taste_mode)
    df_tracks = build_user_track_dataframe(sp, source_tracks, artist_cache)

    df_playlist_tracks = get_playlist_tracks(sp)

    vectorizer, scaler, user_profile = build_user_profile(df_tracks)

    ranked = rank_candidates(
        sp,
        df_tracks,
        df_playlist_tracks,
        vectorizer,
        scaler,
        user_profile,
        artist_cache
    )

    print("\nTop 10 Recommendations:")
    print(ranked.head(10))

    filename = f"ranked_recommendations_{taste_mode}.csv"
    save_csv_with_spaces(ranked.head(50), filename)


if __name__ == "__main__":
    main()