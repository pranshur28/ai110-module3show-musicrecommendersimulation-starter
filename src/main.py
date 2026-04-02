"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def run_profile(name: str, user_prefs: dict, songs: list) -> None:
    """Run the recommender for a single user profile and print results."""
    print(f"\n{'='*55}")
    print(f"  Profile: {name}")
    print(f"  Prefs: {user_prefs}")
    print(f"{'='*55}\n")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"  {i}. {song['title']} by {song['artist']} - Score: {score:.2f}")
        print(f"     Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']}")
        print(f"     {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    # --- Standard Profiles ---
    profiles = {
        "High-Energy Pop Fan": {
            "genre": "pop", "mood": "happy", "energy": 0.9
        },
        "Chill Lofi Listener": {
            "genre": "lofi", "mood": "chill", "energy": 0.3,
            "likes_acoustic": True
        },
        "Deep Intense Rock": {
            "genre": "rock", "mood": "intense", "energy": 0.95
        },

        # --- Edge Case / Adversarial Profiles ---
        "Conflicting: High Energy + Chill": {
            "genre": "lofi", "mood": "chill", "energy": 0.95
        },
        "Genre Not in Dataset": {
            "genre": "reggaeton", "mood": "happy", "energy": 0.7
        },
        "All-Zero Energy Ambient": {
            "genre": "ambient", "mood": "chill", "energy": 0.0,
            "likes_acoustic": True
        },
    }

    for name, prefs in profiles.items():
        run_profile(name, prefs, songs)


if __name__ == "__main__":
    main()
