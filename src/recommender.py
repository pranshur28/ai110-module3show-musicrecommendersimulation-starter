import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> float:
        genre = 1.0 if song.genre == user.favorite_genre else 0.0
        mood = 1.0 if song.mood == user.favorite_mood else 0.0
        energy = 1.0 - abs(song.energy - user.target_energy)
        acoustic = song.acousticness if user.likes_acoustic else (1.0 - song.acousticness)
        return 0.40 * genre + 0.25 * mood + 0.20 * energy + 0.15 * acoustic

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = [(self._score(user, song), song) for song in self.songs]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [song for _, song in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"matches your favorite genre ({song.genre})")
        if song.mood == user.favorite_mood:
            reasons.append(f"matches your preferred mood ({song.mood})")
        energy_diff = abs(song.energy - user.target_energy)
        if energy_diff <= 0.2:
            reasons.append(f"energy level ({song.energy:.1f}) is close to your target ({user.target_energy:.1f})")
        if user.likes_acoustic and song.acousticness > 0.5:
            reasons.append("has the acoustic sound you enjoy")
        if not reasons:
            reasons.append("it has a unique vibe you might enjoy")
        return f"Recommended because it {'; '.join(reasons)}."

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['id'] = int(row['id'])
            row['tempo_bpm'] = float(row['tempo_bpm'])
            for key in ('energy', 'valence', 'danceability', 'acousticness'):
                row[key] = float(row[key])
            songs.append(row)
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    fav_genre = user_prefs.get("genre", "")
    fav_mood = user_prefs.get("mood", "")
    target_energy = user_prefs.get("energy", 0.5)
    likes_acoustic = user_prefs.get("likes_acoustic", False)

    def score(song):
        g = 1.0 if song.get("genre") == fav_genre else 0.0
        m = 1.0 if song.get("mood") == fav_mood else 0.0
        e = 1.0 - abs(float(song.get("energy", 0.5)) - target_energy)
        a = float(song.get("acousticness", 0.5))
        a = a if likes_acoustic else (1.0 - a)
        return 0.40 * g + 0.25 * m + 0.20 * e + 0.15 * a

    def explain(song):
        reasons = []
        if song.get("genre") == fav_genre:
            reasons.append(f"matches your favorite genre ({fav_genre})")
        if song.get("mood") == fav_mood:
            reasons.append(f"matches your preferred mood ({fav_mood})")
        if abs(float(song.get("energy", 0.5)) - target_energy) <= 0.2:
            reasons.append("energy level is close to your target")
        if likes_acoustic and float(song.get("acousticness", 0.5)) > 0.5:
            reasons.append("has the acoustic sound you enjoy")
        if not reasons:
            reasons.append("it has a unique vibe you might enjoy")
        return f"Recommended because it {'; '.join(reasons)}."

    scored = [(song, score(song)) for song in songs]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [(song, sc, explain(song)) for song, sc in scored[:k]]
