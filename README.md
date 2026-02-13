# spotify-ml-recommender

A personalized Spotify music recommendation tool that generates a ranked list of songs based on your listening habits and playlists.

## Features

Fetches top tracks from your Spotify account (short_term, medium_term, long_term) or recently played tracks.

Retrieves tracks from your playlists.

Builds a user taste profile based on track genres and popularity.

Ranks candidate songs from your playlists using cosine similarity.

Saves top recommendations to CSV, with nicely formatted output.

Interactive CLI allows specifying:

taste_mode – timeframe to use for top tracks

top_n – number of recommendations to show/save (10–50)

## Installation
1. Clone the repository

git clone https://github.com/deetyk25/spotify-ml-recommender.git

cd spotify-ml-recommender

2. Install all dependencies
pip install -r requirements.txt

3. Create an .env with Spotify user credentials
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback

## Usage
Run with this command from the root:
python main.py

This will display your options.

You can also provide options directly:
python main.py recent 50
python main.py long_term 10

CSV output files are saved as:
ranked_recommendations_<taste_mode>.csv

## Project Structure
.
├── main.py                  # CLI entrypoint
├── spotify_client.py        # Spotify authentication helper
├── data_loader.py           # Fetch top tracks and playlist tracks
├── recommender.py           # Build user profile and rank candidates
├── utils.py                 # Helper functions (CSV formatting)
└── requirements.txt         # Dependencies

## Next Steps
- Build a GUI: Provide a user-friendly interface so users can select options and view recommendations without using the command line.

- Expand recommendation logic to include Spotify API suggestions.