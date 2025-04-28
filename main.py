import argparse
from src.VibeSorcery import VibeSorcery


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="VibeSorcery: Generate a playlist of songs based on the mood of an input song.")
  parser.add_argument('-o', '--output_dir', type=str, default='playlist', help='Output directory for the generated playlist')
  parser.add_argument('-n', '--num_songs', type=int, default=5, help='Number of songs to generate in the playlist')
  parser.add_argument('-d', '--duration', type=float, default=47.0, help='Duration of each song in seconds')

  print('Summoning the perfect song for your mood, every time 🎼🔮')

  playlist_path = parser.parse_args().output_dir
  num_songs = parser.parse_args().num_songs
  duration = parser.parse_args().duration

  if duration > 47.0:
      print("Duration is too long. Setting to 47.0 seconds.")
      duration = 47.0
  
  vibe_sorcery = VibeSorcery(output_dir=playlist_path)
  playlist_dict = vibe_sorcery.generate_playlist(input_song_path=f'{playlist_path}/playlist_song_0.wav', num_songs=num_songs, duration=duration)

  print("Playlist generated with the following songs:")
  for song in playlist_dict:
      print(f"Song: {song['file_path']}, Caption: {song['caption']}, Moods: {song['moods']}")

  print("Vibe Sorcery completed!🎼🔮")