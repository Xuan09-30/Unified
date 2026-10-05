import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sqlalchemy import create_engine
from dotenv import load_dotenv

# 1. Database Connection
load_dotenv()
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

# 2. Spotify Authentication 
print("Authenticating with Spotify...")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope="user-top-read"
))

# 3. Fetch User's Top Tracks
print("Fetching your Top Tracks for the last month...")
results = sp.current_user_top_tracks(limit=50, time_range='short_term')
tracks = results['items']

if not tracks:
    print("No top tracks found. Go listen to some music!")
    exit()

# 4. Extract tracks and assign Personal Affinity Score
track_data = []
total_tracks = len(tracks)

for index, item in enumerate(tracks):
    track_data.append({
        "track_id": item.get('id', f'unknown_{index}'),
        "track_name": item.get('name', 'Unknown Track'),
        "artist_name": item.get('artists', [{'name': 'Unknown'}])[0]['name'],
        "album_name": item.get('album', {}).get('name', 'Unknown Album'),
        # Assign 50 points to the #1 track, down to 1 point for the 50th
        "popularity": total_tracks - index 
    })

# 5. Overwrite PostgreSQL
df = pd.DataFrame(track_data)
print(f"Overwriting database with {len(df)} tracks and new Affinity Scores...")
df.to_sql('top_tracks', engine, schema='spotify', if_exists='replace', index=False)

print("Database successfully updated!")