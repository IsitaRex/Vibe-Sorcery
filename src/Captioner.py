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
        """
        return [
            # Simple patterns
            ["This is a", "{mood}", "song"],
            ["A", "{mood}", "tune for your", "{mood}", "moments"],
            ["Feeling", "{mood}", "? This track captures that vibe"],
            ["The perfect", "{mood}", "soundtrack for your day"],

            # Comparative patterns
            ["Like", "{mood}", "meets", "{mood}", "in this melodic journey"],
            ["A blend of", "{mood}", "and", "{mood}", "vibes"],
            ["More", "{mood}", "than a", "{mood}", "sunset"],
            ["A", "{mood}", "song with hints of", "{mood}", "undertones"],
            
            # Descriptive patterns
            ["A", "{mood}", "composition with", "{mood}", "undertones"],
            ["Full of", "{mood}", "energy and", "{mood}", "harmonies"],
            ["A", "{mood}", "soundscape that feels", "{mood}"],
            ["Intricate", "{mood}", "textures layered with", "{mood}", "elements"],

            # Emotional patterns
            ["When you need something", "{mood}", "and", "{mood}"],
            ["For those", "{mood}", "nights and", "{mood}", "days"],
            ["Music to feel", "{mood}", "and", "{mood}"],
            ["A", "{mood}", "journey through", "{mood}", "emotions"],
            
            # Atmospheric patterns
            ["A", "{mood}", "atmosphere with", "{mood}", "progressions"],
            ["Close your eyes and feel the", "{mood}", "waves of sound"],
            ["Transport yourself to a", "{mood}", "dimension"],
            ["This track creates a", "{mood}", "ambiance that feels", "{mood}"]
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
    
    def generate_caption(self, primary_mood: str, secondary_mood: Optional[str] = None) -> str:
        """
        Generates a unique caption based on the primary and optional secondary mood.
        
        Args:
            primary_mood (str): The primary mood of the song.
            secondary_mood (str, optional): An optional secondary mood.
            
        Returns:
            str: A generated caption.
        """
        # Choose a random template
        template = random.choice(self.grammar_templates)
        
        # Process the template
        caption_parts = []
        for part in template:
            if part == "{mood}":
                # Alternate between primary and secondary mood
                if secondary_mood and random.random() > 0.6:
                    use_mood = secondary_mood
                else:
                    use_mood = primary_mood
                    
                # Use a synonym for the mood 50% of the time
                if random.random() > 0.5:
                    caption_parts.append(self.get_synonym(use_mood))
                else:
                    caption_parts.append(use_mood)
            else:
                caption_parts.append(part)
        
        # Join the parts to form the final captionß
        caption = " ".join(caption_parts)
        return caption[0].upper() + caption[1:]
    
    def generate_from_moods(self, moods: List[str]) -> List[str]:
        """
        Generate a caption based on a list of moods.
        Args:
            moods (List[str]): List of moods to base the caption on.
            
        Returns:
            List[str]: Lista de descripciones generadas.
        """
        
        primary_mood = moods[0]
        secondary_mood = moods[1] if len(moods) > 1 else None
        
        return self.generate_caption(primary_mood, secondary_mood)