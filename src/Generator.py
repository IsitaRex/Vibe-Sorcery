import os
import torch
import soundfile as sf
from typing import Optional, Union, List, Dict
from diffusers import StableAudioPipeline

class Generator:
    """
    Class to generate music from textual descriptions using diffusion models like StableAudio.
    """
    
    def __init__(self, model_name: str = "stabilityai/stable-audio-open-1.0", 
                 device: str = None, 
                 output_dir: str = "playlist"):
        """
        Initializes the Generator with the specified model and device.
        
        Args:
            model_name (str): Name of the model to use for generation.
            device (str): Device to run the model on. Options are "cuda", "mps", or "cpu".
            output_dir (str): Directory to save the generated audio files.
        """
        self.model_name = model_name
        
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
        else:
            self.device = device
        
        self.output_dir = output_dir
        
        # Create the output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # load the model
        try:
            self.pipe = StableAudioPipeline.from_pretrained(
                self.model_name, 
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            )
            self.pipe = self.pipe.to(self.device)
            print(f"Model {self.model_name} loaded on {self.device}")
        except Exception as e:
            print(f"Error to load the model: {e}")
            self.pipe = None
    
    def generate_song(self, 
                      prompt: str, 
                      negative_prompt: str = "Low quality, noise, distortion, artifacts",
                      duration: float = 47.0,
                      seed: Optional[int] = None,
                      filename: Optional[str] = None,
                      return_audio: bool = False) -> Optional[torch.Tensor]:
        """
        Generates a song based on the provided prompt and saves it to a file.
        
        Args:
            prompt (str): Description of the song to generate.
            negative_prompt (str): Features to avoid in the generation.
            duration (float): Duration of the song in seconds.
            seed (int, optional): Seed for random number generation.
            filename (str, optional): Name of the output file. If None, a default name is generated.
            return_audio (bool): True to return the generated audio tensor, False to just save it.
            
        Returns:
            torch.Tensor or None: El tensor de audio si return_audio es True, 
                                 None en caso contrario.
        """
        if self.pipe is None:
            print("No model loaded. Please initialize the generator first.")
            return None
        
        try:
            if seed is not None:
                gen = torch.Generator(self.device).manual_seed(seed)
            else:
                gen = torch.Generator(self.device).manual_seed(torch.randint(0, 1000000, (1,)).item())
            
            # Generate audio
            audio = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                audio_end_in_s=duration,
                num_waveforms_per_prompt=1,
                generator=gen,
            ).audios
            
            output = audio[0].T.float().cpu().numpy()
            
            # Create name if not provided
            if filename is None:
                files = [f for f in os.listdir(self.output_dir) if f.startswith("playlist_song_") and f.endswith(".wav")]
                if files:
                    # Get the last number used
                    last_number = max([int(f.split("_")[-1].split(".")[0]) for f in files])
                    filename = f"playlist_song_{last_number + 1}.wav"
                else:
                    filename = "playlist_song_1.wav"
                
            # Save the audio to a file
            filepath = os.path.join(self.output_dir, filename)
            sf.write(filepath, output, self.pipe.vae.sampling_rate)
            print(f"Song generated in: {filepath}")
            
            if return_audio:
                return audio[0]
            return None
        
        except Exception as e:
            print(f"Error generating the song: {e}")
            return None
    
    def get_model_info(self) -> Dict:
        """
        Obtiene información sobre el modelo cargado.
        
        Returns:
            Dict: Diccionario con información del modelo.
        """
        if self.pipe is None:
            return {"status": "No disponible", "error": "Modelo no inicializado"}
        
        return {
            "model_name": self.model_name,
            "device": self.device,
            "output_directory": self.output_dir,
            "sampling_rate": self.pipe.vae.sampling_rate if hasattr(self.pipe, "vae") else "desconocido"
        }