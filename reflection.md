# Reflection: Profile Comparisons

## High-Energy Pop Fan vs. Chill Lofi Listener

These two profiles are nearly opposite in every dimension. The Pop fan (energy 0.9, happy mood) gets Sunrise City and Gym Hero at the top — both high-energy, upbeat tracks. The Lofi listener (energy 0.3, chill mood, likes acoustic) gets Library Rain and Midnight Coding — low-energy, acoustic-heavy tracks. There is zero overlap in their top 5, which makes sense because the scoring correctly separates high-energy/pop from low-energy/lofi. The system does what it should here: two very different taste profiles get completely different recommendations.

## Deep Intense Rock vs. High-Energy Pop Fan

Both profiles want high energy (0.95 and 0.9), but differ in genre and mood. Storm Runner dominates for the rock fan (genre + mood + energy all match), while Sunrise City wins for the pop fan. Interestingly, Gym Hero (pop, intense, 0.93 energy) appears in both top 5s — it's a bridge song that shares energy with rock fans and genre with pop fans. This shows how a single song can serve different audiences for different reasons, which mirrors how real playlists work on Spotify.

## Conflicting Profile (Lofi + Chill + 0.95 Energy) vs. Chill Lofi Listener

The conflicting profile is almost identical to the Chill Lofi listener except for energy (0.95 vs 0.3). Despite this massive energy difference, the top 2 songs are the same (Midnight Coding, Library Rain) — just with lower scores (0.79 vs 0.93). This reveals that genre and mood dominate the ranking so heavily that energy barely reshuffles results. In a real system, this could be a problem: the user explicitly asked for high energy but still gets the same low-energy lofi tracks. A smarter system would either flag the contradiction or balance the weights dynamically.

## Genre Not in Dataset (Reggaeton) vs. High-Energy Pop Fan

When the genre doesn't exist in the catalog, the system falls back on mood and energy. The reggaeton fan (happy, 0.7 energy) gets Sunrise City and Rooftop Lights at the top — both happy, medium-high energy songs. These are reasonable suggestions, but the scores are much lower (0.55 vs 0.97) because the 40% genre weight contributes zero. This shows a graceful degradation, but also highlights how dependent the system is on genre matching. A real recommender would use genre similarity (e.g., reggaeton is close to Latin pop) rather than exact string matching.
