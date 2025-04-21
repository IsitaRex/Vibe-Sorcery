# Vibe Sorcerer 🎼🔮  
**Summoning the perfect song for your mood, every time.**

## Overview (10%) [300 Words]
*Vibe Sorcerer* is a mood-based playlist generator designed to create emotionally cohesive listening experiences. Rather than compiling a random selection of tracks, it curates playlists that feel intentional and immersive—each song smoothly transitioning into the next to maintain a consistent emotional arc. The core hypothesis is that a great playlist mirrors an emotional journey, and cohesion can be achieved by ensuring continuity in the emotional states evoked by each track.

The system generates playlists iteratively. Starting with a single input song, it identifies its emotional qualities using [MTG Listening Models](https://github.com/MTG/essentia). It then generates a descriptive caption reflecting the song’s mood using a grammar-based system. This caption serves as input for Riffusion, a music generation model, which creates the next song in the sequence. This process repeats until the desired playlist length is reached, ensuring each transition is emotionally logical and musically fluid.

The motivation behind Vibe Sorcerer stems from a lifelong passion for music. Listening has always been a way for me to clear my mind, process emotions, and stay present. I believe music is one of the most powerful tools for emotional awareness and expression. This project is a personal exploration of how technology can amplify the emotional power of music—and how generative systems can be used not just to create sound, but to shape feeling. In the future, this idea of playlist generation could support therapeutic practices by guiding listeners through carefully curated emotional states.

## Key Features  
- **Mood-Based Playlists**: Generate playlists tailored to your current emotional state.  
- **Seamless Transitions**: Each song is carefully selected to complement the previous one, avoiding abrupt emotional shifts.  
- **Iterative Generation**: Build a full playlist by repeating the process, one song at a time.  

## Why Vibe Sorcerer?  
Creating a playlist that *feels right* is harder than it seems. It’s not just about picking good songs—it’s about how those songs fit together. Vibe Sorcerer takes the guesswork out of playlist curation, ensuring every track aligns with the mood and flows naturally into the next.  

## How to Use  
1. Provide a starting song or mood.  
2. Let Vibe Sorcerer generate the next song based on your input.  
3. Repeat the process to build a full playlist.  

## Hypothesis  
A great playlist is defined by its emotional cohesion. Songs shouldn’t jump from one extreme mood to another—instead, they should transition smoothly, creating a unified listening experience. Vibe Sorcerer is built on this principle, ensuring every playlist feels like a curated journey.  
