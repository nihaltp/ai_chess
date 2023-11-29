import sys
import pygame

# Initialize Pygame
pygame.init()

# Constants
width, height = 600, 500
square_width = 400
rows, columns = 8, 8
square_size = square_width // columns

#import images
pawn_w = pygame.image.load("pieces/pawn_w.png")
pawn_b = pygame.image.load("pieces/pawn_b.png")
knight_w = pygame.image.load("pieces/knight_w.png")
knight_b = pygame.image.load("pieces/knight_b.png")
bishop_w = pygame.image.load("pieces/bishop_w.png")
bishop_b = pygame.image.load("pieces/bishop_b.png")
rook_w = pygame.image.load("pieces/rook_w.png")
rook_b = pygame.image.load("pieces/rook_b.png")
queen_w = pygame.image.load("pieces/queen_w.png")
queen_b = pygame.image.load("pieces/queen_b.png")
king_w = pygame.image.load("pieces/king_w.png")
king_b = pygame.image.load("pieces/king_b.png")

# Introduce a variable to track the selected piece
selected_piece = None

# Complete Chessboard with Pieces
chessboard_dict = {
    'a1': 'rook_w', 'b1': 'knight_w', 'c1': 'bishop_w', 'd1': 'queen_w', 'e1': 'king_w', 'f1': 'bishop_w', 'g1': 'knight_w', 'h1': 'rook_w',
    'a2': 'pawn_w', 'b2': 'pawn_w', 'c2': 'pawn_w', 'd2': 'pawn_w', 'e2': 'pawn_w', 'f2': 'pawn_w', 'g2': 'pawn_w', 'h2': 'pawn_w',
    'a3': 'NA', 'b3': 'NA', 'c3': 'NA', 'd3': 'NA', 'e3': 'NA', 'f3': 'NA', 'g3': 'NA', 'h3': 'NA',
    'a4': 'NA', 'b4': 'NA', 'c4': 'NA', 'd4': 'NA', 'e4': 'NA', 'f4': 'NA', 'g4': 'NA', 'h4': 'NA',
    'a5': 'NA', 'b5': 'NA', 'c5': 'NA', 'd5': 'NA', 'e5': 'NA', 'f5': 'NA', 'g5': 'NA', 'h5': 'NA',
    'a6': 'NA', 'b6': 'NA', 'c6': 'NA', 'd6': 'NA', 'e6': 'NA', 'f6': 'NA', 'g6': 'NA', 'h6': 'NA',
    'a7': 'pawn_b', 'b7': 'pawn_b', 'c7': 'pawn_b', 'd7': 'pawn_b', 'e7': 'pawn_b', 'f7': 'pawn_b', 'g7': 'pawn_b', 'h7': 'pawn_b',
    'a8': 'rook_b', 'b8': 'knight_b', 'c8': 'bishop_b', 'd8': 'queen_b', 'e8': 'king_b', 'f8': 'bishop_b', 'g8': 'knight_b', 'h8': 'rook_b',
}

# Colors
white = (255, 255, 255)
black = (192, 192, 192)
text_color = white

# Create the Pygame window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("AI Chess")

# Where to start the chess board
chess_x = 100
chess_y = 50

chessboard_rows = [8,7,6,5,4,3,2,1]
chessboard_columns = ["a","b","c","d","e","f","g","h"]

# Draw the chessboard# Create a 2D list to represent the chessboard with values
chessboard = [[0] * columns for _ in range(rows)]

# Assign unique values to each square
for row in range(rows):
    for column in range(columns):
        chessboard[row][column] = chessboard_columns[column], chessboard_rows[row]

# Pygame font setup
pygame.font.init()
font = pygame.font.SysFont(None, 30)

# Draw chessboard
def draw_chessboard(rows, columns):
    # Draw each square independently
    for row in range(rows):
        for column in range(columns):
            color = white if (row + column) % 2 == 0 else black
            square_rect = pygame.Rect(chess_x + column * square_size, chess_y + row * square_size, square_size, square_size)
            pygame.draw.rect(screen, color, square_rect)

            # Check chessboard configuration and blit the corresponding image
            piece_key_tuple = chessboard[row][column]
            piece_key = piece_key_tuple[0]+ str(piece_key_tuple[1])
            piece = chessboard_dict[piece_key]
            piece_image = None

            if piece == "pawn_w":
                piece_image = pawn_w
            elif piece == "rook_w":
                piece_image = rook_w
            elif piece == "knight_w":
                piece_image = knight_w
            elif piece == "bishop_w":
                piece_image = bishop_w
            elif piece == "queen_w":
                piece_image = queen_w
            elif piece == "king_w":
                piece_image = king_w
            elif piece == "pawn_b":
                piece_image = pawn_b
            elif piece == "rook_b":
                piece_image = rook_b
            elif piece == "knight_b":
                piece_image = knight_b
            elif piece == "bishop_b":
                piece_image = bishop_b
            elif piece == "queen_b":
                piece_image = queen_b
            elif piece == "king_b":
                piece_image = king_b
            # Handle the case when the piece is not recognized
            else:
                continue

            if piece != None:
                # Blit the piece image
                screen.blit(piece_image, square_rect.topleft)

# Draw chessboard rows
def draw_rows():
    for i, row_value in enumerate(chessboard_rows):
        text = font.render(str(row_value), True, text_color)
        text_rect = text.get_rect(center=(chess_x - 30, chess_y + i * square_size + square_size // 2))
        screen.blit(text, text_rect)
        text_rect = text.get_rect(center=(chess_x + 430, chess_y + i * square_size + square_size // 2))
        screen.blit(text, text_rect)

# Draw chessboard columns
def draw_columns():
    for i, col_value in enumerate(chessboard_columns):
        text = font.render(col_value, True, text_color)
        text_rect = text.get_rect(center=(chess_x + i * square_size + square_size // 2, chess_y - 30))
        screen.blit(text, text_rect)
        text_rect = text.get_rect(center=(chess_x + i * square_size + square_size // 2, chess_y + 430))
        screen.blit(text, text_rect)

#handle events
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_click()

#handle mouse clicks
def handle_mouse_click():
    # Get the mouse coordinates
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Determine the clicked square
    clicked_column = (mouse_x - chess_x) // square_size
    clicked_row = (mouse_y - chess_y) // square_size

    # Check if the click is within the chessboard boundaries
    if 0 <= clicked_row < rows and 0 <= clicked_column < columns:
        clicked_square_value = chessboard[clicked_row][clicked_column]
        clicked_square_value = clicked_square_value[0]+ str(clicked_square_value[1])

        print(f"Mouse clicked at Square : {clicked_square_value}")
    else:
        print(f"Mouse clicked at ({mouse_x}, {mouse_y})")

while True:
    draw_chessboard(rows, columns)
    draw_rows()
    draw_columns()
    handle_events()

    # Update the display
    pygame.display.flip()