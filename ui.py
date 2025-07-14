import streamlit as st
import pandas as pd

st.title("Spotify ML Playlist Recommender")

# Show top tracks table
st.subheader("Your Top Tracks Audio Features")
df = pd.read_csv("top_tracks_audio_features.csv")
st.dataframe(df)

# Mood input
mood = st.selectbox("Choose your mood", ["Happy", "Chill", "Workout", "Party"])

if st.button("Get Recommendations"):
    # placeholder for recommendation logic
    st.write(f"Recommending songs for mood: {mood}")
