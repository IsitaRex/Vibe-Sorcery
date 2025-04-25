import os
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Optional, Union
from essentia.standard import MonoLoader, TensorflowPredictVGGish, TensorflowPredict2D
from scipy.spatial.distance import euclidean
from pathlib import Path
import matplotlib.colors as mcolors


class Evaluator:
    """
    Class for evaluating the emotional coherence of a playlist.
    Analyzes the arousal and valence values of songs to measure the playlist quality.
    """
    
    def __init__(self,  model_path_embeddings = "models/audioset-vggish-3.pb", model_path_classification = "models/deam-audioset-vggish-2.pb"):
        """
        Initialize the Evaluator with the necessary models.
        
        Args:
            models_dir (str): Directory where the models are stored.
        """
        
        # Initialize the models for arousal-valence prediction
        self.embeddings_model_av = TensorflowPredictVGGish(
            graphFilename=model_path_embeddings, 
            output="model/vggish/embeddings"
        )

        self.av_classification_model = TensorflowPredict2D(
            graphFilename=model_path_classification, 
            output="model/Identity"
        )
    
    def get_arousal_valence(self, wav_filepath: str) -> Tuple[float, float]:
        """
        Extract arousal and valence values from an audio file.
        
        Args:
            wav_filepath (str): Path to the audio file.
            
        Returns:
            Tuple[float, float]: Tuple containing (arousal, valence) values.
        """
        audio = MonoLoader(filename=wav_filepath, sampleRate=16000, resampleQuality=4)()
        embeddings = self.embeddings_model_av(audio)
        predictions = self.av_classification_model(embeddings)
        arousal, valence = np.mean(predictions, axis=0)
        return arousal, valence
    
    def analyze_playlist(self, playlist_dir: str) -> Dict:
        """
        Analyze a playlist by calculating arousal-valence values for each song.
        
        Args:
            playlist_dir (str): Directory containing the audio files.
            
        Returns:
            Dict: Dictionary with analysis results, including songs data and metrics.
        """
        # Get all wav files in the directory
        audio_files = [os.path.join(playlist_dir, f) for f in os.listdir(playlist_dir) 
                      if f.endswith('.wav') or f.endswith('.mp3')]
        audio_files.sort()  # Ensure consistent ordering
        
        if not audio_files:
            return {"error": "No audio files found in the specified directory"}
        
        songs_data = []
        
        # Process each song
        for i, file_path in enumerate(audio_files):
            filename = os.path.basename(file_path)
            arousal, valence = self.get_arousal_valence(file_path)
            
            songs_data.append({
                "id": i,
                "filename": filename,
                "path": file_path,
                "arousal": float(arousal),
                "valence": float(valence)
            })
        
        # Calculate metrics
        metrics = self._calculate_metrics(songs_data)
        
        return {
            "songs": songs_data,
            "metrics": metrics
        }
    
    def _calculate_metrics(self, songs_data: List[Dict]) -> Dict:
        """
        Calculate various metrics to evaluate playlist coherence.
        
        Args:
            songs_data (List[Dict]): List of dictionaries containing song data.
            
        Returns:
            Dict: Dictionary containing the calculated metrics.
        """
        metrics = {}
        
        # Extract arousal-valence pairs
        av_pairs = [(song["arousal"], song["valence"]) for song in songs_data]
        
        # 1. Average distance between consecutive songs
        if len(av_pairs) > 1:
            distances = [euclidean(av_pairs[i], av_pairs[i+1]) for i in range(len(av_pairs)-1)]
            metrics["avg_consecutive_distance"] = float(np.mean(distances))
            
            # 2. Maximum distance between consecutive songs
            metrics["max_consecutive_distance"] = float(np.max(distances))
            
            # Store all distances for detailed analysis
            metrics["consecutive_distances"] = [float(d) for d in distances]
        else:
            metrics["avg_consecutive_distance"] = 0.0
            metrics["max_consecutive_distance"] = 0.0
            metrics["consecutive_distances"] = []
        
        # 3. Average arousal and valence (center)
        avg_arousal = np.mean([song["arousal"] for song in songs_data])
        avg_valence = np.mean([song["valence"] for song in songs_data])
        metrics["avg_arousal"] = float(avg_arousal)
        metrics["avg_valence"] = float(avg_valence)
        
        # 4. Distances from center
        center = (avg_arousal, avg_valence)
        center_distances = [euclidean((song["arousal"], song["valence"]), center) for song in songs_data]
        metrics["avg_center_distance"] = float(np.mean(center_distances))
        metrics["max_center_distance"] = float(np.max(center_distances))
        metrics["center_distances"] = [float(d) for d in center_distances]
        
        # 5. Variance in arousal and valence
        metrics["arousal_variance"] = float(np.var([song["arousal"] for song in songs_data]))
        metrics["valence_variance"] = float(np.var([song["valence"] for song in songs_data]))
        
        # 6. Total traverse distance (sum of all consecutive distances)
        metrics["total_traverse_distance"] = float(np.sum(metrics["consecutive_distances"]))
        
        return metrics
    
    def plot_arousal_valence_plane(self, 
                              playlist_data: Dict, 
                              output_path: Optional[str] = None,
                              title: str = "Arousal-Valence Analysis",
                              highlight_first: bool = True) -> None:
        """
        Plot the arousal-valence plane with song positions and trajectory.
        
        Args:
            playlist_data (Dict): Data returned by the analyze_playlist method.
                Should contain 'songs' list with 'arousal' and 'valence' entries,
                and 'metrics' dict with average values.
            output_path (str, optional): Path to save the plot. If None, the plot is displayed but not saved.
            title (str): Title for the plot.
            highlight_first (bool): Whether to highlight the first song in the playlist.
            
        Raises:
            ValueError: If the input data is malformed or missing required fields.
        """
        # Validate input data
        if not playlist_data or 'songs' not in playlist_data or 'metrics' not in playlist_data:
            raise ValueError("Input data must contain 'songs' and 'metrics' keys")
        
        if not playlist_data['songs']:
            raise ValueError("No songs found in the input data")
        
        # Create figure and axis
        plt.figure(figsize=(10, 8))
        ax = plt.subplot(111)
        
        # Create a colormap for the trajectory
        cmap = plt.get_cmap('viridis')
        
        songs = playlist_data["songs"]
        
        # # Set the limits of the plot to the arousal-valence range [0,1]
        ax.set_xlim(1, 9)
        ax.set_ylim(1, 9)
        
        # Draw quadrant lines
        ax.axhline(y=5.0, color='gray', linestyle='-', alpha=0.3)
        ax.axvline(x=5.0, color='gray', linestyle='-', alpha=0.3)
        
        # Add quadrant labels
        # Add quadrant labels
        ax.text(3, 8, "Low Valence\nHigh Arousal", ha='center', fontsize=10, alpha=0.7)
        ax.text(7, 8, "High Valence\nHigh Arousal", ha='center', fontsize=10, alpha=0.7)
        ax.text(3, 2, "Low Valence\nLow Arousal", ha='center', fontsize=10, alpha=0.7)
        ax.text(7, 2, "High Valence\nLow Arousal", ha='center', fontsize=10, alpha=0.7)
        
        # Add labels and title
        ax.set_xlabel('Valence', fontsize=12)
        ax.set_ylabel('Arousal', fontsize=12)
        ax.set_title(title, fontsize=14)
        
        # Add a color bar to show the progression
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, len(songs)-1))
        sm.set_array([])  # trick to satisfy the ScalarMappable
        cbar = plt.colorbar(sm, ax=ax)
        cbar.set_label('Song Sequence')

        # Plot each song
        for i, song in enumerate(songs):
            color_val = i / max(1, len(songs) - 1)  # Normalize to [0, 1]
            color = cmap(color_val)
            
            if i == 0 and highlight_first:
                # Highlight the first song with a different marker and label
                ax.scatter(song["valence"], song["arousal"], s=150, color='red', 
                        marker='*', label="First Song", zorder=5)
            else:
                ax.scatter(song["valence"], song["arousal"], s=100, color=color, 
                        alpha=0.7, zorder=4)
            
            # Add song number label
            ax.annotate(str(i+1), (song["valence"], song["arousal"]), 
                    fontsize=10, ha='center', va='center', color='white', 
                    fontweight='bold', zorder=6)
        
        # Plot the trajectory line
        if len(songs) > 1:
            points = [(song["valence"], song["arousal"]) for song in songs]
            breakpoint()
            
            # Draw arrows connecting consecutive points to show direction
            for i in range(len(points) - 1):
                color_val = i / max(1, len(songs) - 2)  # Normalize to [0, 1]
                color = cmap(color_val)
                
                ax.annotate('', xy=points[i+1], xytext=points[i],
                        arrowprops=dict(arrowstyle='->', color=color, linewidth=2, alpha=0.7))
        
        # Add central point (average arousal-valence)
        metrics = playlist_data["metrics"]
        ax.scatter(metrics["avg_valence"], metrics["avg_arousal"], s=150,
                marker='X', color='black', label='Center', alpha=0.5, zorder=3)
        
        # Draw a circle with radius equal to average center distance
        circle = plt.Circle((metrics["avg_valence"], metrics["avg_arousal"]), 
                        metrics["avg_center_distance"], fill=False, 
                        linestyle='--', color='gray', alpha=0.4)
        ax.add_patch(circle)
        
        
        # Add a legend
        ax.legend(loc='upper right')
        
        # Add metrics annotations
        metrics_text = (
            f"Metrics:\n"
            f"Avg. Consecutive Distance: {metrics['avg_consecutive_distance']:.3f}\n"
            f"Max. Consecutive Distance: {metrics['max_consecutive_distance']:.3f}\n"
            f"Avg. Center Distance: {metrics['avg_center_distance']:.3f}\n"
            f"Total Traverse Distance: {metrics['total_traverse_distance']:.3f}"
        )
        
        plt.figtext(0.02, 0.02, metrics_text, fontsize=10, 
                bbox=dict(facecolor='white', alpha=0.7))
        
        # Save or show the plot
        plt.tight_layout()
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {output_path}")
        else:
            plt.show()
    
    def evaluate_playlist_quality(self, playlist_data: Dict) -> Dict:
        """
        Evaluate the overall quality of a playlist based on the calculated metrics.
        
        Args:
            playlist_data (Dict): Data returned by the analyze_playlist method.
            
        Returns:
            Dict: Dictionary containing quality scores and recommendations.
        """
        metrics = playlist_data["metrics"]
        songs = playlist_data["songs"]
        
        # Initialize scores
        scores = {}
        
        # 1. Coherence score (based on average consecutive distance)
        # Lower distance = higher coherence
        # Scale: 0 (poor) to 10 (excellent)
        avg_dist = metrics["avg_consecutive_distance"]
        scores["coherence"] = max(0, 10 - (avg_dist * 10))
        
        # 2. Smoothness score (based on max consecutive distance)
        # Lower max distance = smoother transitions
        max_dist = metrics["max_consecutive_distance"]
        scores["smoothness"] = max(0, 10 - (max_dist * 10))
        
        # 3. Variety score (based on the total area covered in AV space)
        # Higher center distance variance = more variety
        center_distance_var = np.var(metrics["center_distances"])
        scores["variety"] = min(10, center_distance_var * 50)
        
        # 4. Emotional range score
        arousal_range = np.max([s["arousal"] for s in songs]) - np.min([s["arousal"] for s in songs])
        valence_range = np.max([s["valence"] for s in songs]) - np.min([s["valence"] for s in songs])
        emotional_range = (arousal_range + valence_range) / 2
        scores["emotional_range"] = min(10, emotional_range * 10)
        
        # 5. Overall journey quality
        # Combination of the above metrics
        scores["overall"] = (
            scores["coherence"] * 0.3 +  # 30% weight on coherence
            scores["smoothness"] * 0.3 +  # 30% weight on smoothness
            scores["variety"] * 0.2 +     # 20% weight on variety
            scores["emotional_range"] * 0.2  # 20% weight on emotional range
        )
        
        # Generate recommendations
        recommendations = []
        
        if scores["coherence"] < 5:
            recommendations.append("Consider improving the coherence by selecting songs with more similar emotional qualities.")
            
        if scores["smoothness"] < 5:
            # Identify the problematic transition
            distances = metrics["consecutive_distances"]
            if distances:
                worst_transition_idx = np.argmax(distances)
                song1 = songs[worst_transition_idx]["filename"]
                song2 = songs[worst_transition_idx + 1]["filename"]
                recommendations.append(f"The transition between song {worst_transition_idx+1} ({song1}) and song {worst_transition_idx+2} ({song2}) is abrupt. Consider adding an intermediate song.")
        
        if scores["variety"] < 3:
            recommendations.append("The playlist may be too emotionally uniform. Consider adding songs with different moods.")
        
        if scores["variety"] > 8:
            recommendations.append("The playlist may be too emotionally scattered. Consider grouping similar songs together.")
        
        if scores["emotional_range"] < 4:
            recommendations.append("The emotional range is limited. Consider adding songs with more diverse emotional qualities.")
        
        # Return the evaluation results
        return {
            "scores": {k: round(v, 2) for k, v in scores.items()},
            "recommendations": recommendations
        }