
class Tile:
    LETTER_VALUES = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4,
                     'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1,
                     'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1,
                     'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
                     'Y': 4, 'Z': 10, '?': 0}

    def __init__(self, letter: str):
        if letter not in self.LETTER_VALUES:
            raise ValueError(f"Invalid letter {letter}")
        self._letter = letter.upper()
        self._custom_letter = None

    @property
    def value(self) -> int:
        return self.LETTER_VALUES[self._letter]
    
    @property
    def is_blank(self) -> bool:
        return self._letter == '?'

    def set_letter(self, custom_letter: str):
        if not self.is_blank:
            raise ValueError("Cannot set a letter for a non-blank tile")
        elif self._custom_letter is not None:
            raise ValueError(f"Letter for blank tile already set to {self._custom_letter}")
        
        if not custom_letter.isalpha():
            raise ValueError(f"Invalid blank tile letter {custom_letter}")
        
        # Store in lowercase to match Woogles omgwords format
        self._custom_letter = custom_letter.lower()

    def __repr__(self):
        if self.is_blank and self._custom_letter is not None:
            return f"Tile('{self._letter} = {self._custom_letter}')"
        else:
            return f"Tile('{self._letter}')"
