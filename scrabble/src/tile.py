
class Tile:
    LETTER_VALUES = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4,
                     'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1,
                     'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1,
                     'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
                     'Y': 4, 'Z': 10, '?': 0}

    def __init__(self, letter: str):
        self._letter = letter.upper()
        if self._letter not in self.LETTER_VALUES:
            raise ValueError(f"Invalid letter {self._letter}")
        self._custom_letter = None

    @classmethod
    def fromstr(cls, tile_str):
        """
        Constructs a Tile based on a string in the Woogles format.
        """
        if len(tile_str) != 1:
            raise ValueError(f"Cannot construct tile from {tile_str}, Tiles can only be constructed from single characters")
        
        if tile_str.isupper():
            return cls(tile_str)
        elif tile_str.islower():
            return cls('?').set_letter(tile_str)
        else:
            raise ValueError(f"Cannot construct tile from invalid letter {tile_str}")

    @property
    def value(self) -> int:
        return self.LETTER_VALUES[self._letter]
    
    @property
    def is_blank(self) -> bool:
        return self._letter == '?'
    
    @property
    def is_set(self) -> bool:
        return not self.is_blank or self._custom_letter is not None

    def set_letter(self, custom_letter: str):
        if not self.is_blank:
            raise ValueError("Cannot set a letter for a non-blank tile")
        elif self._custom_letter is not None:
            raise ValueError(f"Letter for blank tile already set to {self._custom_letter}")
        
        if not custom_letter.isalpha() or len(custom_letter) != 1:
            raise ValueError(f"Invalid blank tile letter {custom_letter}")
        
        # Store in lowercase to match Woogles omgwords format
        self._custom_letter = custom_letter.lower()

        return self

    def format(self):
        """
        Converts a tile to Woogles string format: "<letter>" (uppercase). If a tile is blank, "<custom_letter>" is displayed instead (lowercase).
        """
        if self.is_blank:
            assert self._custom_letter is not None
            return self._custom_letter
        return self._letter

    def __repr__(self):
        if self.is_blank and self._custom_letter is not None:
            return f"Tile('{self._letter} = {self._custom_letter}')"
        else:
            return f"Tile('{self._letter}')"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Tile):
            return False

        if self.is_blank:
            return self._custom_letter == other._custom_letter
        return self._letter == other._letter