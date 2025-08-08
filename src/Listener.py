from essentia.standard import MonoLoader, TensorflowPredictEffnetDiscogs, TensorflowPredict2D
from src.utils import mood_tags, genre_tags
import numpy as np
import random
from typing import List, Dict, Tuple, Optional


class Listener:
    """
    Extracts mood and genre features from songs using pre-trained models.
    Uses the Essentia library to load audio files and extract features.
    """

    def __init__(self, 
                 embeddings_model_path: str = "discogs-effnet-bs64-1.pb", 
                 moods_model_path: str = "mtg_jamendo_moodtheme-discogs-effnet-1.pb",
                 genre_model_path: str = "mtg_jamendo_genre-discogs-effnet-1.pb") -> None:
        
        self.embeddings_model = TensorflowPredictEffnetDiscogs(
            graphFilename=embeddings_model_path,
            output="PartitionedCall:1",
        )

        self.mood_model = TensorflowPredict2D(
            graphFilename=moods_model_path,
            output='model/Sigmoid',
        )

        self.genre_model = TensorflowPredict2D(
            graphFilename=genre_model_path
        )
        
    def _load_and_extract_embeddings(self, song_path: str) -> np.ndarray:
        """Load audio and extract embeddings."""
        audio = MonoLoader(filename=song_path, sampleRate=32000)()
        return self.embeddings_model(audio)
    
    def _get_average_activations(self, activations: List[List[float]]) -> List[float]:
        """Calculate average activations across time."""
        return [
            sum(activations[j][i] for j in range(len(activations))) / len(activations)
            for i in range(len(activations[0]))
        ]
    
    def _filter_predictions(self, predictions_dict: Dict[str, float], 
                          threshold: float, min_items: int, max_items: Optional[int] = None) -> List[str]:
        """Filter predictions based on threshold and quantity limits."""
        # Filter by threshold
        above_threshold = [tag for tag, value in predictions_dict.items() if value > threshold]
        
        # If too few, take top min_items
        if len(above_threshold) < min_items:
            sorted_predictions = sorted(predictions_dict.items(), key=lambda x: x[1], reverse=True)
            above_threshold = [tag for tag, _ in sorted_predictions[:min_items]]
        
        # If too many, limit randomly
        if max_items and len(above_threshold) > max_items:
            above_threshold = random.sample(above_threshold, max_items)
            
        return above_threshold

    def get_moods_from_song(self, song_path: str, threshold: float = 0.07) -> List[str]:
        """
        Detect moods in a song.

        Args:
            song_path: Path to the audio file
            threshold: Threshold value to filter moods

        Returns:
            List of moods detected in the song
        """
        embeddings = self._load_and_extract_embeddings(song_path)
        activations = self.mood_model(embeddings)
        activation_averages = self._get_average_activations(activations)
        
        predictions_dict = {tag: activation_averages[i] for i, tag in enumerate(mood_tags)}
        
        return self._filter_predictions(predictions_dict, threshold, min_items=4)

    def get_genres_from_song(self, song_path: str, threshold: float = 0.1) -> List[str]:
        """
        Detect genres in a song.

        Args:
            song_path: Path to the audio file
            threshold: Threshold value to filter genres

        Returns:
            List of genres detected in the song
        """
        embeddings = self._load_and_extract_embeddings(song_path)
        activations = self.genre_model(embeddings)
        activation_averages = self._get_average_activations(activations)
        
        predictions_dict = {tag: activation_averages[i] for i, tag in enumerate(genre_tags)}
        
        return self._filter_predictions(predictions_dict, threshold, min_items=1, max_items=4)

    def get_moods_and_genres(self, song_path: str, 
                           mood_threshold: float = 0.07, 
                           genre_threshold: float = 0.1) -> Tuple[List[str], List[str]]:
        """
        Detect both moods and genres in a song efficiently.

        Args:
            song_path: Path to the audio file
            mood_threshold: Threshold value to filter moods
            genre_threshold: Threshold value to filter genres

        Returns:
            Tuple containing (list_of_moods, list_of_genres)
        """
        # Extract embeddings once for both predictions
        embeddings = self._load_and_extract_embeddings(song_path)
        
        # Predict moods
        mood_activations = self.mood_model(embeddings)
        mood_averages = self._get_average_activations(mood_activations)
        mood_predictions = {tag: mood_averages[i] for i, tag in enumerate(mood_tags)}
        moods = self._filter_predictions(mood_predictions, mood_threshold, min_items=4)
        
        # Predict genres
        genre_activations = self.genre_model(embeddings)
        genre_averages = self._get_average_activations(genre_activations)
        genre_predictions = {tag: genre_averages[i] for i, tag in enumerate(genre_tags)}
        genres = self._filter_predictions(genre_predictions, genre_threshold, min_items=1, max_items=4)
        
        return moods, genres

    # Keep compatibility with previous method
    def get_genre(self, song_path: str, threshold: float = 0.1) -> List[str]:
        """Legacy method - use get_genres_from_song() instead."""
        return self.get_genres_from_song(song_path, threshold)