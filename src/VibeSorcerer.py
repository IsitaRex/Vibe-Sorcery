import os
import time
import librosa
import numpy as np
from typing import List, Dict, Tuple, Optional, Union
from src.Listener import Listener
from src.Captioner import Captioner
from src.Generator import Generator
from pathlib import Path

class VibeSorcerer:
    """
    Class to generate a playlist of songs based on the mood of an input song.
    1. Detects the mood of an input song using the Listener component. (Listener)
    2. Generates captions based on the detected mood using the Captioner component. (Captioner)
    3. Creates new songs based on the generated captions using the Generator component. (Generator)
    4. Uses the generated songs as input for the next iteration.
    """
    
    def __init__(self, 
                 models_dir: str = "models",
                 output_dir: str = "playlist", 
                 device: str = None):
        """
        Initializes the VibeSorcerer with the specified directories and device.
        
        Args:
            models_dir (str): Directory where the models are stored.
            output_dir (str): Directory to save the generated audio files.
            device (str): Device to run the model on. Options are "cuda", "mps", or "cpu".
        """
        self.models_dir = models_dir
        self.output_dir = output_dir
        self.device = device
        
        # Create directories if they don't exist
        os.makedirs(models_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize components
        self.listener = Listener()
        self.captioner = Captioner()
        self.generator = Generator(device=device, output_dir=output_dir)
        
        # Initialize the playlist
        self.playlist = []
        
    def generate_next_song(self, 
                           input_song_path: str, 
                           duration: float = 47.0,
                           seed: Optional[int] = None) -> Dict:
        """
        Generates the next song in the playlist based on the input song.
        
        Args:
            input_song_path (str): Path to the input audio file
            duration (float): Duration of the generated song in seconds
            seed (int, optional): Seed for reproducibility
            
        Returns:
            Dict: Information about the generated song, including file path, caption, and moods
        """
        # Step 1: Detect the mood of the input song
        moods = self.listener.get_moods_from_song(input_song_path)
        primary_mood = moods[0] if moods else "calm"
        secondary_mood = moods[1] if len(moods) > 1 else None
        
        # Step 2: Generate a caption based on the detected mood
        caption = self.captioner.generate_caption(primary_mood, secondary_mood)
        
        # Step 3: Generate the song using the generator
        clean_name = caption.lower().replace(" ", "_")[:20]
        output_filename = f"{clean_name}_{int(time.time())}.wav"
        
        self.generator.generate_song(
            prompt=caption,
            duration=duration,
            seed=seed,
            filename=output_filename
        )
        
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Save the song information
        song_info = {
            "file_path": output_path,
            "caption": caption,
            "moods": moods,
            "primary_mood": primary_mood,
            "secondary_mood": secondary_mood,
            "duration": duration
        }
        
        self.playlist.append(song_info)
        return song_info
        
    def generate_playlist(self, 
                         input_song_path: str, 
                         num_songs: int = 5, 
                         duration: float = 47.0,
                         seed: Optional[int] = None) -> List[Dict]:
        """
        Generates a playlist of songs based on the input song.
        
        Args:
            input_song_path (str): Path to the input audio file
            num_songs (int): Number of songs to generate
            duration (float): Duration of each generated song in seconds
            seeds (List[int], optional): List of seeds for reproducibility
            
        Returns:
            List[Dict]: List of generated songs with their information
        """
        self.playlist = []  # Initialize the playlist
        
        # Validate input song path
        if not os.path.exists(input_song_path):
            raise FileNotFoundError(f"No song: {input_song_path}")
        
        # Generate the first song
        last_song = self.generate_next_song(input_song_path, duration, seed)
        
        # Generate the rest of the songs
        for i in range(1, num_songs):
            print(f"Generating song {i+1}/{num_songs}...")
            # Use the last generated song as input for the next one
            last_song = self.generate_next_song(last_song["file_path"], duration, seed)
        
        print("Vibe Sorcery completed!🎼🔮")
        print(f"Playlist generated with {len(self.playlist)} songs.")
        return self.playlist
    
    def get_playlist_info(self) -> Dict:
        """
        Gets information about the generated playlist.
        
        Returns:
            Dict: Information about the playlist, including number of songs, total duration, and unique moods
        """
        if not self.playlist:
            return {"status": "Empty", "message": "No playlist was generated."}
        
        total_duration = sum(song.get("duration", 0) for song in self.playlist)
        unique_moods = set()
        for song in self.playlist:
            if "moods" in song:
                unique_moods.update(song["moods"])
        
        return {
            "num_songs": len(self.playlist),
            "total_duration_seconds": total_duration,
            "total_duration_formatted": f"{int(total_duration // 60)}:{int(total_duration % 60):02d}",
            "unique_moods": list(unique_moods),
            "songs": [{"file": Path(song["file_path"]).name, 
                       "caption": song["caption"], 
                       "moods": song["moods"][:3]} for song in self.playlist]
        }