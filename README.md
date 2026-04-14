# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This project is a content-based music recommender that scores a catalog of 10 songs against a user's taste profile using a weighted sum of four features: genre (40%), mood (25%), energy closeness (20%), and acousticness preference (15%). It returns the top-k songs with plain-language explanations for each pick. The system was tested against six user profiles — three standard and three adversarial/edge-case — to evaluate its strengths and failure modes.

---

## How The System Works

### Song Features

Each `Song` has 10 attributes: `id`, `title`, `artist`, `genre`, `mood`, `energy` (0–1), `tempo_bpm`, `valence` (0–1), `danceability` (0–1), and `acousticness` (0–1). Of these, the scoring function currently uses **genre**, **mood**, **energy**, and **acousticness**. The remaining features (tempo, valence, danceability) are loaded but reserved for future experiments.

### User Profile

A `UserProfile` stores four preferences:
- `favorite_genre` — exact genre string (e.g., "pop", "lofi")
- `favorite_mood` — exact mood string (e.g., "happy", "chill")
- `target_energy` — a float from 0 to 1 representing desired energy level
- `likes_acoustic` — a boolean indicating acoustic preference

### Scoring Logic

The `Recommender._score()` method computes a weighted sum for each song:

```
score = 0.40 × genre_match + 0.25 × mood_match + 0.20 × energy_closeness + 0.15 × acoustic_fit
```

- **Genre match**: 1.0 if exact match, 0.0 otherwise
- **Mood match**: 1.0 if exact match, 0.0 otherwise
- **Energy closeness**: `1.0 - |song.energy - user.target_energy|`
- **Acoustic fit**: `song.acousticness` if user likes acoustic, else `1.0 - song.acousticness`

### Recommendation Selection

All songs are scored, sorted in descending order, and the top `k` (default 5) are returned. Each recommendation includes a plain-language explanation listing which factors contributed.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

### Weight Shift Experiment
Changed genre weight from 0.40 to 0.20 and doubled energy weight from 0.20 to 0.40. The #1 result for each standard profile stayed the same (Sunrise City for pop fans, Library Rain for lofi listeners, Storm Runner for rock fans), but positions 3–5 shuffled significantly. This confirmed that the top pick is robust, while mid-list rankings are sensitive to weight tuning.

### Adversarial / Edge-Case Profiles
- **Conflicting preferences (lofi + chill + 0.95 energy):** The system still ranked lofi songs first because genre (40%) and mood (25%) dominated over energy (20%). It cannot detect or warn the user that their preferences are contradictory.
- **Genre not in dataset (reggaeton):** With no genre match possible, all songs scored 0 on genre. Mood and energy drove the ranking, producing reasonable fallback results — happy, medium-energy songs floated to the top.
- **All-zero energy ambient:** The ambient song Spacewalk Thoughts ranked first as expected. The acoustic preference bonus helped separate it from other low-energy songs.

### Profile Comparison
Three standard profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock) all produced intuitive #1 picks. The lofi listener got more variety (3 lofi songs in the catalog) than the rock fan (only 1 rock song), exposing the catalog-size bias.

---

## Limitations and Risks

- **Tiny catalog (10 songs):** Genres with only 1 song (rock, jazz, ambient) give users almost no variety, while lofi fans get 3 options.
- **Binary genre matching:** "indie pop" and "pop" are treated as completely unrelated, ignoring real-world genre similarity.
- **No conflict detection:** A user who asks for "lofi + chill + 0.95 energy" gets lofi songs ranked first even though none have high energy. The system silently returns mismatched results.
- **No lyrics, language, or cultural context:** The system has no understanding of what a song sounds like beyond its numeric features.
- **Single-user, single-moment design:** It cannot track listening history, detect mood changes over time, or combine preferences from multiple users for group recommendations.
- **Catalog bias:** Since lofi and pop are overrepresented, the system gives richer recommendations to fans of those genres, which could create an unfair experience if deployed.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this system showed me that recommenders turn data into predictions through surprisingly simple arithmetic. A weighted sum of four features and a catalog of 10 songs can produce recommendations that genuinely "feel" right — when I saw Sunrise City rank first for a pop/happy user, it felt like the system understood music taste, but it's really just matching labels and computing distances. The "magic" of apps like Spotify isn't necessarily sophisticated AI; a lot of it comes from choosing the right features, assigning reasonable weights, and having enough data to work with.

The bias and fairness issues became obvious through testing. The dataset has 3 lofi songs and only 1 rock song, so a lofi fan gets meaningful variety while a rock fan gets one correct pick followed by irrelevant filler. This mirrors a real-world problem: if a streaming platform's catalog underrepresents certain genres (or the cultures and communities behind them), the recommender will systematically give those listeners a worse experience — not because the algorithm is intentionally biased, but because the data it was trained on reflects existing inequalities. The weight experiment also revealed that small design choices (like giving genre 40% weight) have outsized effects on who gets good recommendations and who doesn't.


---

## Model Card

The full model card with detailed evaluation, limitations, future work, and personal reflection is in:

[**model_card.md**](model_card.md)

