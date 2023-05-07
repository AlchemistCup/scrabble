class Pos:
    MAX_SIZE = 15

    def __init__(self, row: int, col: int):
        assert(Pos._in_bounds(row))
        assert(Pos._in_bounds(col))
        self._row = row
        self._col = col

    @property
    def row(self):
        return self._row
    
    @property
    def col(self):
        return self._col
    
    def get_adjacent(self):
        """
        Generates all valid positions adjacent to itself
        """
        def adjacent_1D(x_or_y):
            for displacement in [-1, 1]:
                new_pos = x_or_y(self) + displacement
                if Pos._in_bounds(new_pos):
                    yield new_pos

        for new_row in adjacent_1D(lambda pos: pos.row):
            yield Pos(new_row, self.col)
        
        for new_col in adjacent_1D(lambda pos: pos.col):
            yield Pos(self.row, new_col)

    @staticmethod
    def _in_bounds(x: int):
        # Scrabble boards are 15x15
        return 0 <= x < Pos.MAX_SIZE

    def __add__(self, other):
        return Pos(self.row + other.row, self.col + other.col)
    
    def __sub__(self, other):
        return Pos(self.row - other.row, self.col - other.col)
    
    def __eq__(self, other) -> bool:
        return (self.row == other.row) and (self.col == other.col)
    
    def __lt__(self, other) -> bool:
        return (self.row, self.col) < (other.row, other.col)
    
    def __hash__(self) -> int:
        return hash((self.row, self.col))

    def __repr__(self) -> str:
        return f"Pos({self._row}, {self._col})"
    
    # Convert to match Woggles omgwords position format
    def __str__(self) -> str:
        assert False, "Currently unimplemented"
        return f""