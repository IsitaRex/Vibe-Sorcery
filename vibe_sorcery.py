import numpy as np
import librosa
from src.utils import mood_tags
from essentia.standard import MonoLoader, TensorflowPredictEffnetDiscogs, TensorflowPredictVGGish,TensorflowPredict2D

# Load the audio file
audio_path = 'input_song.wav'
audio_data, sample_rate = librosa.load(audio_path)

# Use  MTG models to extract features
embeddings_model_moods = TensorflowPredictEffnetDiscogs(
    graphFilename="models/discogs-effnet-bs64-1.pb",
    output="PartitionedCall:1",
)

mood_classification_model = TensorflowPredict2D(
    graphFilename="models/mtg_jamendo_moodtheme-discogs-effnet-1.pb",
    output='model/Sigmoid',
)

embeddings_model_av = TensorflowPredictVGGish(
   graphFilename="models/audioset-vggish-3.pb", 
   output="model/vggish/embeddings"
   )

av_classification_model = TensorflowPredict2D(
   graphFilename="models/deam-audioset-vggish-2.pb", 
   output="model/Identity"
  )

def get_arousal_valence(wav_filepath):
  audio = MonoLoader(filename=wav_filepath, sampleRate=16000, resampleQuality=4)()
  embeddings = embeddings_model_av(audio)
  predictions = av_classification_model(embeddings)
  arousal, valence = np.mean(predictions, axis = 0)
  return arousal, valence


def get_mood_activations_dict(wav_filepath):
  audio = MonoLoader(filename=wav_filepath, sampleRate=32000)()
  embeddings = embeddings_model_moods(audio)
  activations = mood_classification_model(embeddings)
  activation_avs = []
  for i in range(0, len(activations[0])):
    vals = [activations[j][i] for j in range(0, len(activations))]
    # Note - this does the averaging bit
    activation_avs.append(sum(vals)/len(vals))
  activations_dict = {}
  for ind, tag in enumerate(mood_tags):
    activations_dict[tag] = activation_avs[ind]
  return activations_dict

def get_moods(mood_dict, threshold=0.05, k=5):
    """
    Returns the moods that are above a certain threshold. If no moods are above the threshold, it returns the top k moods.

    Args:
        mood_dict (dict): A dictionary mapping mood tags to activation values.
        threshold (float): The threshold value to filter moods.

    Returns:
        list: A list of the mood tags that are above the threshold.
    """

    # Sort the mood dictionary by activation values in descending order
    sorted_moods = sorted(mood_dict.items(), key=lambda item: item[1], reverse=True)
    moods = [mood[0] for mood in sorted_moods if mood[1] > threshold]
    # If no moods are above the threshold, return the top k moods
    if not moods:
        return [mood[0] for mood in sorted_moods[:5]]
    # Return the top k moods
    return [mood[0] for mood in sorted_moods if mood[1] > threshold]

mood_dict = get_mood_activations_dict(audio_path)
top_moods = get_moods(mood_dict, threshold=0.06)
print("Top moods:", top_moods)

arousal, valence = get_arousal_valence(audio_path)
print("Valence:", valence)
print("Arousal:", arousal)