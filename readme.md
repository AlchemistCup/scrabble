# Scrabble.py
This is a python package encoding the game logic for Scrabble. APIs also indicate when moves are invalid (against the rules) to enable error detection in game data capture.

## Installation
Simply clone the repo and run:
```
python setup.py install
```

## Usage
All of the classes making up the package can be imported using:
```python
from scrabble import *
```

From there, you can check the code in the [src directory](scrabble/src), all public methods are well-documented. Unit tests are in the [test directory](scrabble/tests), and are probably most easily run directly via an IDE such as VScode. All tests follow the `*_test.py` naming pattern.
