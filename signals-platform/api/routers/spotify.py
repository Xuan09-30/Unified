# api/routers/spotify.py
from fastapi import APIRouter
from ingestion.db import get_db_connection

router = APIRouter(prefix="/spotify", tags=["Quantified Self"])

@router.get("/top-tracks")
def get_top_tracks():
    """Returns the user's top Spotify tracks ranked by algorithmic popularity."""
    query = """
        SELECT 
            track_name, 
            artist_name, 
            album_name, 
            popularity
        FROM spotify.top_tracks
        ORDER BY popularity DESC;
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            results = cur.fetchall()
    return results