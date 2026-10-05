-- db/spotify_schema.sql
CREATE SCHEMA IF NOT EXISTS spotify;

DROP TABLE IF EXISTS spotify.playlist_signals;

CREATE TABLE IF NOT EXISTS spotify.top_tracks (
    track_id VARCHAR(100) PRIMARY KEY,
    track_name VARCHAR(255),
    artist_name VARCHAR(255),
    album_name VARCHAR(255),
    popularity INT
);