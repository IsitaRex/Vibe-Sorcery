import random
from src.utils import mood_synonyms
from typing import List, Dict, Set, Optional, Tuple, Union
class Captioner:
    """
    Class to generate captions for songs based on their mood.
    It uses grammars and synonyms to create unique descriptions.
    """

    def __init__(self):
        self.mood_synonyms = mood_synonyms
        self.grammar_templates = self._initialize_grammar_templates()

    def _initialize_grammar_templates(self) -> List[List[str]]:
        """
        Initializes the grammar templates used for generating captions.
        Now supports both {mood} and {genre} placeholders.
        """
        return [
            ["A", "{genre}", "tune for your", "{mood}", "moments"],
            ["The perfect", "{genre}", "sountrack, for your", "{mood}", "day"],
            ["A", "{genre}", "track that blends", "{mood}", "vibes"],
            ["A", "{genre}", "song with", "{mood}", "vibes"],
            ["{genre}", "music to feel", "{mood}"],
            ["A", "{genre}", "piece that evokes a", "{mood}", "atmosphere"]
        ]

    def get_synonym(self, mood: str) -> str:
        """
        Get a random synonym for a given mood.

        Args:
            mood (str): The mood for which to find a synonym.

        Returns:
            str: A random synonym.
        """
        synonyms = self.mood_synonyms.get(mood, [mood])
        return random.choice(synonyms)

    def _join_moods(self, moods: List[str]) -> str:
        """
        Joins a list of moods into a comma-separated string with proper grammar.

        Args:
            moods (List[str]): List of moods to join

        Returns:
            str: Comma-separated string of moods
        """
        if len(moods) == 1:
            return moods[0]
        return ", ".join(moods[:-1]) + " and " + moods[-1]

    def generate_caption(self, genres: List[str], moods: Optional[List[str]] = None) -> str:
        """
        Generates a unique caption based on the primary and optional secondary moods.

        Args:
            primary_moods (List[str]): The primary moods of the song.
            secondary_moods (List[str], optional): Optional secondary moods.

        Returns:
            str: A generated caption.
        """
        
        # Choose a random template
        template = random.choice(self.grammar_templates)
        first_part = False

        # Use synonyms for the moods base on random chance
        moods = [self.get_synonym(mood) if random.random() > 0.5 else mood for mood in moods]

        # Process the template
        caption_parts = []
        for part in template:
            if part == "{mood}":
                caption_parts.append(", ".join(moods))
            elif part == "{genre}":
                caption_parts.append(", ".join(genres))
            else:
                caption_parts.append(part)

        # Join the parts to form the final caption
        caption = " ".join(caption_parts)
        return caption[0].upper() + caption[1:]