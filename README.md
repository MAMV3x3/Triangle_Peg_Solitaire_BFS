# Triangle Peg Solitaire

This is a Python implementation of the classic triangle peg solitaire game. The goal of this game is to jump pegs over each other in order to remove them from the board. The final objective is to have only one peg left, preferably in a specific position.
This enhanced version provides a graphical visualization of the solution path using images. It also supports deeper search depths to find a solution.

![image](https://github.com/MAMV3x3/Triangle_Peg_Solitaire_DFS/assets/84588180/e2cafef8-9b6c-464b-a7f8-8e0566989b22)

![solution](https://github.com/MAMV3x3/Triangle_Peg_Solitaire_BFS/assets/84588180/0dab3f76-6b6f-4db8-a617-343e7d078afe)

*Author*: Miguel Ángel Mireles Vázquez (ma.mirelesvazquez@ugto.mx)

## Requirements

- Python 3.x
- PIL (Python Imaging Library)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/MAMV3x3/Triangle_Peg_Solitaire_BFS.git
```

2. Navigate to the directory:
```bash
cd Triangle_Peg_Solitaire_BFS
```

3. Install the required dependences:
```bash
pip install pillow
```

## Usage
Run the game using the command:
```bash
python TrianglePeg.py
```

Follow the on-screen instructions:

1. Enter the start position using the notation e.g. a1, b2, etc.
2. Enter the desired end position using the same notation or use '*' if there's no specific ending position.
3. Enter the the maximum depth for the search.

The game will then generate potential solutions and visualize them, showing you the moves needed to reach the goal. If a solution is found, a GIF illustrating the moves will be saved as solution.gif.

## Dependencies
Aside from Python 3.x, this game relies on the following external Python libraries:
- PIL (Python Imaging Library)
Make sure to install them before running the game.

## Contributions
Contributions are welcome! Please make sure to update the tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
