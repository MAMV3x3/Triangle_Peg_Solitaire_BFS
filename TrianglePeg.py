# Author: Miguel Ángel Mireles Vázquez (ma.mirelesvazquez@ugto.mx)

# Node class representing a state in the game
class Node:
    def __init__(self, board, move=None, parent=None):
        self.board = board  # Current state of the game board
        self.move = move  # The move made to reach this board state
        self.parent = parent  # Previous state of the game
        self.children = []  # Possible moves from this state

    def add_child(self, node):
        self.children.append(node)  # Appending a move from this state

# The main game logic for Triangle Peg Solitaire
class TrianglePeg:
    def __init__(self, start_pos, end_pos):
        # Initializing the board with pegs (1 represents a peg, 0 represents an empty slot)
        board = [
            [1],
           [1, 1],
          [1, 1, 1],
         [1, 1, 1, 1],
        [1, 1, 1, 1, 1]
        ]
        board[start_pos[0]][start_pos[1]] = 0  # Remove the peg at the start position
        self.root = Node(board)  # The initial state of the game
        self.goal_node = None  # The desired end state
        self.end_pos = end_pos
    
    # Generate all possible moves from a given state
    def generate_moves(self, node):
        board = node.board
        moves = []
        # All possible movement directions for a peg
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0), (2, 2), (-2, -2)]
        # Iterating over each slot on the board
        for i in range(len(board)):
            for j in range(len(board[i])):
                for dx, dy in directions:
                    # Checking if the movement is within the board boundaries
                    if i + dx >= 0 and i + dx < len(board) and j + dy >= 0 and j + dy < len(board[i + dx]):
                        # If the current slot is empty and the ending slot has a peg and there's a peg in between
                        if board[i][j] == 0 and board[i + dx][j + dy] == 1 and board[i + dx // 2][j + dy // 2] == 1:
                            new_board = [row.copy() for row in board]  # Copying the current state
                            # Making the move on the copied board
                            new_board[i][j] = 1
                            new_board[i + dx][j + dy] = 0
                            new_board[i + dx // 2][j + dy // 2] = 0
                            # Appending the resulting board and the move to the moves list
                            moves.append((new_board, (i, j, i + dx, j + dy)))
        return moves
    
    # Generates a tree of possible moves and states up to a given depth or until the goal state is found
    def generate_tree(self, depth_limit):
        depth = 0
        current_level = [self.root]  # Start with the root node

        while depth < depth_limit and not self.goal_node:
            print(f"Searching at depth {depth}...")
            next_level = []
            # Iterating over each node in the current level
            for node in current_level:
                for new_board, move in self.generate_moves(node):
                    child_node = Node(new_board, move, node)  # Generating a child node with the new state
                    node.add_child(child_node)
                    next_level.append(child_node)  # Preparing for the next level of search

                    # If the current board state is the goal state
                    if self.is_goal_state(new_board):
                        self.goal_node = child_node
                        return
                    
            current_level = next_level
            depth += 1

    # Check if the given board state is the goal state
    def is_goal_state(self, board):
        count_peg = sum(row.count(1) for row in board)
        # The board should have only one peg
        if count_peg == 1:
            # If the end position is not specific or the remaining peg is in the desired position
            if self.end_pos == '*' or board[self.end_pos[0]][self.end_pos[1]] == 1:
                return True
        return False
    
    # Print the solution path if found
    def print_solution(self):
        if not self.goal_node:
            print('No solution found')
            return
        
        path = []
        current_node = self.goal_node
        # Tracing back to the root from the goal node
        while current_node:
            path.append((current_node.board, current_node.move))
            current_node = current_node.parent

        print('Solution found with {} moves'.format(len(path) - 1))
        print('Start position:')
        self.print_board(path[-1][0])
        # Printing each move in the solution path
        for step, (board, move) in enumerate(reversed(path[:-1]), 1):
            if move:
                to_pos = coords_to_notation(move[0], move[1])
                from_pos = coords_to_notation(move[2], move[3])
                print('Step {}: Move peg from {} to {}'.format(step, from_pos, to_pos))
                self.print_board(board)

    # Print the game board
    def print_board(self, board):
        for i, row in enumerate(board):
            print(' ' * (4 - i) + ' '.join(['o' if cell == 1 else '.' for cell in row]))
        print('-' * 13)

# Convert board coordinates to the standard a1, b2, etc. notation
def coords_to_notation(row, col):
    return chr(col + ord('a')) + str(row + 1)

# Convert the standard a1, b2, etc. notation to board coordinates
def notation_to_coords(pos):
    row = int(pos[1]) - 1
    col = ord(pos[0]) - ord('a')
    return row, col

# Main function to execute the game
def main():
    start_pos_notation = input('Enter the start position (e.g. a1, b2, ...): ')
    end_pos_notation = input('Enter the end position (e.g. a1, b2, ...) or "*" for any position: ')
    max_depth = int(input('Enter the maximum depth for the search: '))

    start_pos = notation_to_coords(start_pos_notation)
    # If a specific end position is not given, use '*'
    if end_pos_notation != '*':
        end_pos = notation_to_coords(end_pos_notation)
    else:
        end_pos = '*'

    game = TrianglePeg(start_pos, end_pos)
    game.generate_tree(max_depth)  # Generating the search tree up to the given depth
    game.print_solution()  # Printing the solution path
    
if  __name__ == '__main__':
    main()
