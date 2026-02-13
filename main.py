import sys
from spotify_client import get_spotify_client
from data_loader import (
    get_source_tracks,
    build_user_track_dataframe,
    get_playlist_tracks
)
from recommender import build_user_profile, rank_candidates
from utils import save_csv_with_spaces

VALID_TASTE_MODES = ["short_term", "medium_term", "long_term", "recent"]

def print_options():
    print("Welcome to the Spotify Recommender! 🎶🎧🎸")
    print("Options you can choose:")
    print(f"  1. Timeframe: Which Spotify timeframe to use for top tracks")
    print(f"     Valid options: {', '.join(VALID_TASTE_MODES)} (default: medium_term)")
    print("  2. top_n: Number of top recommendations to show/save (default: 25, range: 10 - 50)")
    print("-" * 50)
    print("example usage: python main.py recent 50 --> returns top 50 based on last month")
    print("example usage: python main.py medium_term 10 --> returns top 10 recommendations from last 6 months")
    print("example usage: python main.py --> prompts for options interactively\n")

def get_user_inputs():
    """Get taste_mode and top_n either from CLI args or interactively."""
    # CLI args
    taste_mode = sys.argv[1] if len(sys.argv) > 1 else None
    top_n = int(sys.argv[2]) if len(sys.argv) > 2 else None

    # Interactive input if not provided via CLI
    if not taste_mode:
        taste_mode = input(f"Enter taste_mode [{'/'.join(VALID_TASTE_MODES)}] (default: medium_term): ") or "medium_term"

    if taste_mode not in VALID_TASTE_MODES:
        print(f"Invalid taste_mode: {taste_mode}, using default 'medium_term'.")
        taste_mode = "medium_term"

    if not top_n:
        top_n_input = input("Enter number of top recommendations (default 25, range 10-50): ")
        top_n = int(top_n_input) if top_n_input else 25

    # Clamp top_n to valid range
    top_n = max(10, min(top_n, 50))

    print(f"\nUsing term: '{taste_mode}' and top {top_n} recommendations.\n")
    return taste_mode, top_n

def main():
    print_options()

    taste_mode, top_n = get_user_inputs()

    sp = get_spotify_client()
    artist_cache = {}

    # Get user tracks
    source_tracks = get_source_tracks(sp, taste_mode)
    df_tracks = build_user_track_dataframe(sp, source_tracks, artist_cache)

    df_playlist_tracks = get_playlist_tracks(sp)

    # Build profile & rank candidates
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

    # Top N recommendations
    top_ranked = ranked.head(top_n)

    print(f"\nTop {top_n} Recommendations:")
    print(top_ranked)

    filename = f"ranked_recommendations_{taste_mode}.csv"
    save_csv_with_spaces(top_ranked, filename)

if __name__ == "__main__":
    main()