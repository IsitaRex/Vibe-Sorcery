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
            ["A", "{mood}", "song"],
            ["A", "{mood}", "tune for your", "{mood}", "moments"],
            ["The perfect", "{mood}", "soundtrack for your day"],
            ["A song that blends", "{mood}", "and", "{mood}", "vibes"],
            ["A", "{mood}", "song with hints of", "{mood}", "undertones"],
            ["A", "{mood}", "composition with", "{mood}", "undertones"],
            ["Music to feel", "{mood}", "and", "{mood}"],
            ["A song that evoques a", "{mood}", "atmosphere with", "{mood}", "progressions"]
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
    
    def _generate_mood_subsets(self, moods: List[str]) -> Tuple[List[str], List[str]]:
        """
        Generates non-overlapping subsets of moods for primary and secondary moods.
        
        Args:
            moods (List[str]): List of available moods
            
        Returns:
            Tuple[List[str], List[str]]: (primary_moods, secondary_moods)
        """
        # Shuffle the moods to ensure randomness
        shuffled_moods = moods.copy()
        random.shuffle(shuffled_moods)
        
        # Determine split point (at least 1 mood for each subset)
        split_point = random.randint(1, len(shuffled_moods) - 1)
        
        primary_moods = shuffled_moods[:split_point]
        secondary_moods = shuffled_moods[split_point:]

        # Take a random sample of moods for both primary and secondary
        primary_moods = random.sample(primary_moods, k=random.randint(1, len(primary_moods)))
        secondary_moods = random.sample(secondary_moods, k=random.randint(1, len(secondary_moods)))
        
        return (primary_moods, secondary_moods)
    
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
    
    def generate_caption(self, primary_moods: List[str], secondary_moods: Optional[List[str]] = None) -> str:
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

        # Process the template
        caption_parts = []
        for part in template:
            if part == "{mood}":
                if not first_part:
                    # Use the first primary mood
                    use_mood = primary_moods
                    first_part = True
                else:
                    use_mood = secondary_moods
                caption_parts.append(", ".join(use_mood))
            else:
                caption_parts.append(part)
        
        # Join the parts to form the final caption
        caption = " ".join(caption_parts)
        return caption[0].upper() + caption[1:]
    
    def generate_from_moods(self, moods: List[str]) -> str:
        """
        Generate a caption based on a list of moods.
        
        Args:
            moods (List[str]): List of moods to base the caption on.
            
        Returns:
            str: Generated description.
        """
        # Use synonyms for the moods base on random chance
        moods = [self.get_synonym(mood) if random.random() > 0.5 else mood for mood in moods]

        # Generate random subsets of moods
        primary_moods, secondary_moods = self._generate_mood_subsets(moods)
        
        # Generate caption with the mood subsets
        return self.generate_caption(primary_moods, secondary_moods)