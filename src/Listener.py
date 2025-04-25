
from essentia.standard import MonoLoader, TensorflowPredictEffnetDiscogs, TensorflowPredict2D
from src.utils import mood_tags
import numpy as np

class Listener:
    '''
    This class is used to extract mood features from a song using pre-trained models.
    It uses the Essentia library to load the audio file and extract features.
    '''

    def __init__(self, model_path_embeddings = "models/discogs-effnet-bs64-1.pb", model_path_classification = "models/mtg_jamendo_moodtheme-discogs-effnet-1.pb"):
        
        self.embeddings_model_moods = TensorflowPredictEffnetDiscogs(
            graphFilename=model_path_embeddings,
            output="PartitionedCall:1",
        )

        self.mood_classification_model = TensorflowPredict2D(
            graphFilename=model_path_classification,
            output='model/Sigmoid',
        )

    def get_moods_from_song(self, song_path, threshold=0.07):
        '''
        This function takes a song path and returns the moods detected in the song.
        It uses the pre-trained models to extract features and classify the moods.
        
        Args:
          song_path (str): The path to the song file.
          threshold (float): The threshold value to filter moods.
            
        Returns:
          list: A list of moods detected in the song.
        '''
        audio = MonoLoader(filename=song_path, sampleRate=32000)()
        embeddings = self.embeddings_model_moods(audio)
        activations = self.mood_classification_model(embeddings)

        activation_avs = []
        for i in range(len(activations[0])):
            vals = [activations[j][i] for j in range(len(activations))]
            activation_avs.append(sum(vals) / len(vals))

        activations_dict = {tag: activation_avs[ind] for ind, tag in enumerate(mood_tags)}

        # Filter moods based on the threshold
        moods_above_threshold = [mood for mood, value in activations_dict.items() if value > threshold]
        if len(moods_above_threshold)  < 4:
            # If no moods are above the threshold, return the top k moods
            sorted_moods = sorted(activations_dict.items(), key=lambda item: item[1], reverse=True)
            return [mood for mood, _ in sorted_moods[:4]]

        return moods_above_threshold