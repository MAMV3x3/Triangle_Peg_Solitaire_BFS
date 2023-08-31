from PIL import Image, ImageDraw, ImageFont
import math

# Author: Miguel Ángel Mireles Vázquez (ma.mirelesvazquez@ugto.mx)

# Node class representing a state in the game
class Node:
    def __init__(self, board, move=None, parent=None):
        self.board = board  # Current state of the board
        self.move = move  # Move made to reach this board state
        self.parent = parent  # The previous state or node in the game
        self.children = []  # Potential moves/states from this board state

    def add_child(self, node):
        self.children.append(node)  # Appending the child node to the children list

# The main logic for Triangle Peg Solitaire
class TrianglePeg:
    def __init__(self, start_pos, end_pos):
        # Initializing the board in a triangular shape with pegs
        board = [
            [1],
           [1, 1],
          [1, 1, 1],
         [1, 1, 1, 1],
        [1, 1, 1, 1, 1]
        ]
        board[start_pos[0]][start_pos[1]] = 0  # Removing peg from the starting position
        self.root = Node(board)  # Root node represents the initial state of the game
        self.goal_node = None  # Target state we're trying to reach
        self.end_pos = end_pos  # End position for the remaining peg
    
    # Generate all valid moves from a given board state
    def generate_moves(self, node):
        board = node.board
        moves = []
        # All possible movement directions for a peg
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0), (2, 2), (-2, -2)]
        for i in range(len(board)):
            for j in range(len(board[i])):
                for dx, dy in directions:
                    # Validate if the move stays within the board boundaries
                    if i + dx >= 0 and i + dx < len(board) and j + dy >= 0 and j + dy < len(board[i + dx]):
                        # Check for valid move conditions
                        if board[i][j] == 0 and board[i + dx][j + dy] == 1 and board[i + dx // 2][j + dy // 2] == 1:
                            new_board = [row.copy() for row in board]  # Duplicate the current board state
                            # Applying the move on the new board
                            new_board[i][j] = 1
                            new_board[i + dx][j + dy] = 0
                            new_board[i + dx // 2][j + dy // 2] = 0
                            moves.append((new_board, (i, j, i + dx, j + dy)))  # Storing the resultant board and move details
        return moves
    
    # Create a tree of moves and states up to a specified depth or until the goal state is identified
    def generate_tree(self, depth_limit):
        depth = 0
        current_level = [self.root]  # Beginning with the root node
        while depth < depth_limit and not self.goal_node:
            print(f"Searching at depth {depth}...")
            next_level = []
            for node in current_level:
                for new_board, move in self.generate_moves(node):
                    child_node = Node(new_board, move, node)  # Create a child node for the new board state
                    node.add_child(child_node)
                    next_level.append(child_node)  # Prepare for the subsequent depth level

                    if self.is_goal_state(new_board):
                        self.goal_node = child_node
                        return
                    
            current_level = next_level
            depth += 1

    # Check if a board state is the goal state
    def is_goal_state(self, board):
        count_peg = sum(row.count(1) for row in board)
        if count_peg == 1:
            if self.end_pos == '*' or board[self.end_pos[0]][self.end_pos[1]] == 1:
                return True
        return False
    
    # Display the solution path, if found
    def print_solution(self):
        if not self.goal_node:
            print('No solution found')
            return
        
        path = []
        current_node = self.goal_node
        while current_node:
            path.append((current_node.board, current_node.move))
            current_node = current_node.parent

        print('Solution found with {} moves'.format(len(path) - 1))
        print('Start position:')
        self.print_board(path[-1][0])

        # Visualizing the solution using a series of images
        images = [self.draw_board(self.root.board)]
        for step, (board, move) in enumerate(reversed(path[:-1]), 1):
            if move:
                from_pos = coords_to_notation(move[2], move[3])
                to_pos = coords_to_notation(move[0], move[1])
                print(f'Step {step}: Move peg from {from_pos} to {to_pos}')
                self.print_board(board)
                images.append(self.draw_board(board, move))
        
        # Create a gif of the solution path
        if images:
            images[0].save('solution.gif', save_all=True, append_images=images[1:], duration=2000, loop=0)

    # Print the game board to console
    def print_board(self, board):
        for i, row in enumerate(board):
            print(' ' * (4 - i) + ' '.join(['o' if cell == 1 else '.' for cell in row]))
        print('-' * 13)

    # Render the game board as an image using PIL
    def draw_board(self, board, move=None):
        cell_size = 50  # Size of a single cell
        img_size = (cell_size * 9, cell_size * 9) # Size of the image
        img = Image.new('RGB', img_size, 'white')
        draw = ImageDraw.Draw(img) # Drawing context
        font_size = 15
        try:
            font = ImageFont.truetype('arial.ttf', font_size)
        except ImportError:
            font = ImageFont.load_default()

        img_center_x = img_size[0] // 2
        img_center_y = img_size[1] // 2
        board_center_y = (cell_size * len(board)) // 2  # Considering triangular shape

        vertical_spacing = int(cell_size * 0.87)  # Adjusted for equilateral triangles

        # Adjust offsets to center the board
        y_offset = img_center_y - board_center_y + vertical_spacing // 2
        for i, row in enumerate(board):
            x_offset = img_center_x - (cell_size * len(row)) // 2 + cell_size // 2
            for j, cell in enumerate(row):
                x_center = x_offset + j * cell_size
                y_center = y_offset + i * vertical_spacing

                # Drawing pegs, holes, and annotating coordinates
                color = 'blue'
                if move:
                    if (move[0], move[1]) == (i, j):  # Destination
                        color = 'green'  # Highlighted destination peg

                if cell == 1: # Draw peg
                    draw.ellipse([(x_center - cell_size//3, y_center - cell_size//3),
                                (x_center + cell_size//3, y_center + cell_size//3)], fill=color, outline='black')
                else: # Draw hole
                    draw.ellipse([(x_center - cell_size//3, y_center - cell_size//3),
                                (x_center + cell_size//3, y_center + cell_size//3)], fill='white', outline='black')
                    
                # Annotation
                notation = coords_to_notation(i, j)
                bbox = draw.textbbox((x_center, y_center), notation, font)
                text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                draw.text((x_center - text_w // 2, y_center - text_h // 2), notation, font=font, fill='black')
        
        if move:
            triangle_height = (3**0.5)/2 * cell_size  # Height of an equilateral triangle

            # Drawing the arrow
            start_x = move[3] * cell_size + img_center_x - (cell_size * len(board[move[2]])) // 2 + cell_size // 2
            start_y = move[2] * triangle_height + y_offset
            end_x = move[1] * cell_size + img_center_x - (cell_size * len(board[move[0]])) // 2 + cell_size // 2
            end_y = move[0] * triangle_height + y_offset
            self.arrow(draw, start_x, start_y, end_x, end_y, 'red')

            # Annotating the move
            from_pos = coords_to_notation(move[2], move[3])
            to_pos = coords_to_notation(move[0], move[1])
            text = f"{from_pos} to {to_pos}"
            bbox = draw.textbbox((img_size[0], 10), text, font)
            text_w = bbox[2] - bbox[0]
            draw.text((img_size[0] - text_w - 10, 10), text, fill='black', font=font)

        return img
    
    # Draw an arrow between two points
    def arrow(self, draw, x1, y1, x2, y2, color, arrow_size=10):
        draw.line([(x1, y1), (x2, y2)], fill=color, width=2)
        angle = math.atan2(y2 - y1, x2 - x1)
        draw.polygon([(x2 - arrow_size * math.cos(angle - math.pi / 6),
                    y2 - arrow_size * math.sin(angle - math.pi / 6)),
                    (x2, y2),
                    (x2 - arrow_size * math.cos(angle + math.pi / 6),
                    y2 - arrow_size * math.sin(angle + math.pi / 6))], fill=color)

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
