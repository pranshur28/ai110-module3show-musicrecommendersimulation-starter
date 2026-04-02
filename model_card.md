# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

---

## 2. Intended Use  

This system suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, energy level, and acoustic preference. It is designed for classroom exploration and learning about how recommender systems work. It is not intended for real users or production deployment.

**Not intended for:** Replacing a real music streaming service, handling large catalogs with thousands of songs, or serving users whose tastes span multiple genres simultaneously.

---

## 3. How the Model Works  

The system looks at four things about each song and compares them to what the user likes:

1. **Genre** (40% of the score): If the song's genre matches the user's favorite genre exactly, it gets full points. Otherwise it gets zero. This is the most important factor.
2. **Mood** (25% of the score): Same idea — if the song's mood matches what the user wants (like "happy" or "chill"), it gets full points.
3. **Energy** (20% of the score): Instead of an exact match, this measures how close the song's energy level is to the user's target. A song with 0.8 energy scores almost perfectly for a user wanting 0.9, but a song with 0.3 energy scores poorly.
4. **Acousticness** (15% of the score): If the user likes acoustic music, songs with higher acousticness score better. If not, less acoustic songs are preferred.

Each song gets a total score between 0 and 1. The system sorts all songs by score and returns the top results. It also generates a short explanation for each pick, listing which factors matched.

---

## 4. Data  

The catalog contains **10 songs** in `data/songs.csv`. Each song has these features: title, artist, genre, mood, energy, tempo_bpm, valence, danceability, and acousticness.

**Genres represented:** pop (2), lofi (3), rock (1), ambient (1), jazz (1), synthwave (1), indie pop (1).  
**Moods represented:** happy (2), chill (3), intense (2), relaxed (1), moody (1), focused (1).

No songs were added or removed from the starter dataset. Major gaps include: no hip-hop, R&B, classical, country, reggaeton, or electronic/EDM. The dataset skews toward lofi and pop, so users who prefer those genres get more diverse recommendations than fans of rock or jazz, which each have only one song.

---

## 5. Strengths  

- **Intuitive results for well-represented profiles.** A pop/happy fan gets Sunrise City first. A lofi/chill listener gets Library Rain. A rock/intense user gets Storm Runner. These all feel right.
- **Graceful degradation.** When a user's favorite genre doesn't exist in the catalog (e.g., reggaeton), the system doesn't crash or return garbage — it falls back on mood and energy to find reasonable alternatives.
- **Full transparency.** Every recommendation comes with a plain-language explanation of why it was chosen. You can trace exactly which factors contributed to each score, unlike black-box ML models.
- **Tiered ranking.** The weighted scoring creates clear separation: perfect matches score ~0.95+, partial matches ~0.50-0.75, and weak matches ~0.25-0.35. This makes it easy to see how confident the system is.

---

## 6. Limitations and Bias 

The system over-prioritizes genre matching (40% weight), which means users whose favorite genre appears more often in the catalog get richer recommendations while users preferring rare or missing genres (e.g., reggaeton, classical, hip-hop) receive generic fallback results driven only by energy and mood. The dataset itself is biased toward lofi and pop (3 lofi songs, 2 pop songs out of 10), so chill/lofi listeners get more variety than rock or jazz fans. Additionally, the binary genre matching treats "indie pop" and "pop" as completely unrelated, which ignores real-world genre similarity. The system also cannot detect conflicting preferences — a user requesting "lofi + chill + 0.95 energy" still gets lofi songs ranked first even though no lofi track in the catalog has high energy, creating a disconnect between the user's energy preference and what is actually recommended.  

---

## 7. Evaluation  

We tested six user profiles: three standard (High-Energy Pop, Chill Lofi, Deep Intense Rock) and three adversarial/edge-case (Conflicting High Energy + Chill, Genre Not in Dataset, All-Zero Energy Ambient). For each profile, we examined the top 5 recommendations and verified the #1 result matched intuition.

**Key findings:**
- Standard profiles produced intuitive results: Sunrise City topped for pop fans, Library Rain for lofi listeners, Storm Runner for rock fans.
- The "Conflicting" profile (lofi + chill + 0.95 energy) revealed that genre/mood dominate over energy — lofi songs still ranked first despite poor energy fit. This shows the system cannot detect or warn about contradictory preferences.
- The "Genre Not in Dataset" profile (reggaeton) gracefully degraded — with no genre match possible, mood and energy drove the ranking, producing reasonable results (happy, medium-energy songs floated to the top).
- The weight-shift experiment (doubled energy, halved genre) showed rankings are stable at the top but shift meaningfully in the middle. The #1 song for each standard profile stayed the same, but lower-ranked songs shuffled significantly.
- Two pytest unit tests were written to verify that the OOP recommender returns correctly sorted results and non-empty explanation strings. Both pass.

---

## 8. Future Work  

1. **Genre similarity instead of exact matching.** Instead of treating "pop" and "indie pop" as completely unrelated, use a similarity map so related genres get partial credit (e.g., indie pop scores 0.6 against a pop preference instead of 0.0).
2. **Diversity penalty.** Currently the system can recommend 3 lofi songs in a row for a lofi fan. Adding a diversity bonus would ensure variety — if the #1 pick is lofi, bump a non-lofi song higher in the remaining slots.
3. **Use unused features.** The dataset includes tempo_bpm, valence, and danceability, but the scoring ignores them. Adding these would allow richer user profiles (e.g., a user who wants high danceability and positive valence for a party playlist).

---

## 9. Personal Reflection  

**Biggest learning moment:** The weight experiment was eye-opening. Changing just two numbers (doubling energy weight, halving genre weight) didn't change the #1 result for any profile, but it completely reshuffled positions 3-5. This showed me that the top recommendation is often obvious, but the middle of the list is where design decisions really matter — and where users might notice bias the most.

**How AI tools helped:** AI tools were great for scaffolding the scoring logic and generating boilerplate like CSV parsing. But I had to double-check the math manually — when I calculated the expected score for the test case by hand (pop song = 0.97 vs lofi song = 0.135), that's what gave me confidence the weights were right. Trusting the tool without verifying would have been risky, especially for edge cases like conflicting preferences.

**What surprised me:** A weighted sum with four features and 10 songs can produce recommendations that genuinely "feel" right. When I saw Sunrise City rank first for a pop/happy user, it felt like the system understood music taste — but it's really just arithmetic. This made me realize that the "magic" of apps like Spotify isn't necessarily sophisticated AI; a lot of it comes from having the right features and enough data.

**What I'd try next:** I would add collaborative filtering — instead of only matching song features to a single user profile, I'd track what multiple users liked and recommend songs that similar users enjoyed. This is how real systems escape the "filter bubble" that content-based filtering creates.
