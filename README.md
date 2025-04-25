# Vibe Sorcery 🎼🔮  
**Summoning the perfect song for your mood, every time.**

*Vibe Sorcerer* is a mood-based playlist generator designed to create emotionally cohesive listening experiences. Rather than compiling a random selection of tracks, it curates playlists that feel intentional and immersive—each song smoothly transitioning into the next to maintain a consistent emotional arc. The core hypothesis is that a great playlist mirrors an emotional journey, and cohesion can be achieved by ensuring continuity in the emotional states evoked by each track.

The system generates playlists iteratively. Starting with a single input song, it identifies its emotional qualities using [MTG Listening Models](https://github.com/MTG/essentia). It then generates a descriptive caption reflecting the song’s mood using a grammar-based system. This caption serves as input for Riffusion, a music generation model, which creates the next song in the sequence. This process repeats until the desired playlist length is reached, ensuring each transition is emotionally logical and musically fluid.

The motivation behind Vibe Sorcerer stems from a lifelong passion for music. Listening has always been a way for me to clear my mind, process emotions, and stay present. I believe music is one of the most powerful tools for emotional awareness and expression. This project is a personal exploration of how technology can amplify the emotional power of music—and how generative systems can be used not just to create sound, but to shape feeling. In the future, this idea of playlist generation could support therapeutic practices by guiding listeners through carefully curated emotional states. Moreover, using generated songs helps ensure that the emotional response they evoke is not influenced by cultural or contextual associations tied to commercial music, allowing for a clearer and more controlled induction of specific emotional states.


## Getting Started with *Vibe Sorcery*

### 1. Clone the repository
Begin by cloning the repository to your local machine:
```
git clone https://github.com/IsitaRex/Vibe-Sorcery.git
```
### 2. Install Dependencies
Navigate to the project directory and install the required dependencies:
```
pip install -r requirements.txt
```

### 3. Download Pre-trained Models
Download the necessary pre-trained models and save them in a folder named `Models`. Use the following commands:
Download the pre-trained models and save them inside a folder called 
 ```bash
mkdir -p Models && cd Models
```
 ```
wget https://essentia.upf.edu/models/music-style-classification/discogs-effnet/discogs-effnet-bs64-1.pb
 ```
  ```
wget https://essentia.upf.edu/models/classification-heads/mtg_jamendo_moodtheme/mtg_jamendo_moodtheme-discogs-effnet-1.pb
 ```
  ```
wget https://essentia.upf.edu/models/classification-heads/deam/deam-audioset-vggish-2.pb
 ```
  ```
wget https://essentia.upf.edu/models/feature-extractors/vggish/audioset-vggish-3.pb
 ```
Once the setup is complete, you're ready to generate mood-based playlists with Vibe Sorcery! 🎼🔮

 ```bash
mkdir -p Models && cd Models
wget https://essentia.upf.edu/models/music-style-classification/discogs-effnet/discogs-effnet-bs64-1.pb
wget https://essentia.upf.edu/models/classification-heads/mtg_jamendo_moodtheme/mtg_jamendo_moodtheme-discogs-effnet-1.pb
wget https://essentia.upf.edu/models/classification-heads/deam/deam-audioset-vggish-2.pb
wget https://essentia.upf.edu/models/feature-extractors/vggish/audioset-vggish-3.pb
 ```