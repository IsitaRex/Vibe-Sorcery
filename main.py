from src.Listener import Listener
from src.Captioner import Captioner
from src.Generator import Generator

listener = Listener()
song_path = 'playlist/input_song.wav'

moods = listener.get_moods_from_song(song_path, threshold=0.07)
print("Moods detected:", moods)

captioner = Captioner()
captions = captioner.generate_captions(moods[0])
print("Generated captions:")
for caption in captions:
    print(caption)


generator = Generator(device="cpu")
generator.generate_song(moods[0])