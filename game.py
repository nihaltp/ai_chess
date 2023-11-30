import sys
import chess
import pygame

# Initialize Pygame
pygame.init()

# Constants
width = 700
height = 500
square_width = 400
rows = 8
columns = 8
square_size = square_width // columns

# Where to start the chess board
chess_x = 150
chess_y = 50

# Variables
selected_piece = None
highlight = False

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

piece_image = {
    "pawn_w": pawn_w,
    "rook_w": rook_w,
    "knight_w": knight_w,
    "bishop_w": bishop_w,
    "queen_w": queen_w,
    "king_w": king_w,
    "pawn_b": pawn_b,
    "rook_b": rook_b,
    "knight_b": knight_b,
    "bishop_b": bishop_b,
    "queen_b": queen_b,
    "king_b": king_b,
}

# Complete Chessboard with Pieces
chessboard = {
    'a1': 'rook_w', 'b1': 'knight_w', 'c1': 'bishop_w', 'd1': 'queen_w', 'e1': 'king_w', 'f1': 'bishop_w', 'g1': 'knight_w', 'h1': 'rook_w',
    'a2': 'pawn_w', 'b2': 'pawn_w', 'c2': 'pawn_w', 'd2': 'pawn_w', 'e2': 'pawn_w', 'f2': 'pawn_w', 'g2': 'pawn_w', 'h2': 'pawn_w',
    'a3': 'NA', 'b3': 'NA', 'c3': 'NA', 'd3': 'NA', 'e3': 'NA', 'f3': 'NA', 'g3': 'NA', 'h3': 'NA',
    'a4': 'NA', 'b4': 'NA', 'c4': 'NA', 'd4': 'NA', 'e4': 'NA', 'f4': 'NA', 'g4': 'NA', 'h4': 'NA',
    'a5': 'NA', 'b5': 'NA', 'c5': 'NA', 'd5': 'NA', 'e5': 'NA', 'f5': 'NA', 'g5': 'NA', 'h5': 'NA',
    'a6': 'NA', 'b6': 'NA', 'c6': 'NA', 'd6': 'NA', 'e6': 'NA', 'f6': 'NA', 'g6': 'NA', 'h6': 'NA',
    'a7': 'pawn_b', 'b7': 'pawn_b', 'c7': 'pawn_b', 'd7': 'pawn_b', 'e7': 'pawn_b', 'f7': 'pawn_b', 'g7': 'pawn_b', 'h7': 'pawn_b',
    'a8': 'rook_b', 'b8': 'knight_b', 'c8': 'bishop_b', 'd8': 'queen_b', 'e8': 'king_b', 'f8': 'bishop_b', 'g8': 'knight_b', 'h8': 'rook_b',
}


FILE_NAMES = ["a", "b", "c", "d", "e", "f", "g", "h"]
RANK_NAMES = ["1", "2", "3", "4", "5", "6", "7", "8"]

# Draw the chessboard# Create a 2D list to represent the chessboard with values
squares = [
    "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1",
    "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
    "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
    "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
    "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
    "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",
    "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
    "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8",
]

# Colors
white = (255, 255, 255)
black = (192, 192, 192)
gold = (255, 215, 0)
text_color = white
background = (135, 206, 250)
board_border = (0, 0, 0)

# Create the Pygame window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("AI Chess")

# Pygame font setup
pygame.font.init()
font = pygame.font.SysFont(None, 30)

# Draw chessboard
def draw_chessboard(rows, columns):
    global highlight, mouse_x, mouse_y

    screen.fill(background)
    square_rect = pygame.Rect(chess_x - 2, chess_y - 2, square_width + 4, square_width + 4)
    pygame.draw.rect(screen, board_border, square_rect, width = 2 )

    # Draw each square independently
    for row in range(rows):
        for column in range(columns):
            color = white if (row + column) % 2 == 0 else black
            square_rect = pygame.Rect(chess_x + column * square_size, chess_y + row * square_size, square_size, square_size)
            pygame.draw.rect(screen, color, square_rect)

            # Check chessboard configuration and blit the corresponding image
            value = row * 8 + column
            piece_key = squares[value]
            piece = chessboard[piece_key]
            draw_piece(piece, square_rect)

    draw_rows()
    draw_columns()

    if highlight:
        highlight_square(mouse_x, mouse_y)

# Function to draw pieces on the board
def draw_piece(piece, square_rect):
    global piece_image

    # Get the piece image from the dictionary
    piece_img = piece_image.get(piece)

    if piece_img is not None:
        # Blit the piece image
        screen.blit(piece_img, square_rect.topleft)

# Draw chessboard rows
def draw_rows():
    for i, row_value in enumerate(RANK_NAMES):
        text = font.render(str(row_value), True, text_color)
        text_rect = text.get_rect(center=(chess_x - 30, chess_y + i * square_size + square_size // 2))
        screen.blit(text, text_rect)
        text_rect = text.get_rect(center=(chess_x + 430, chess_y + i * square_size + square_size // 2))
        screen.blit(text, text_rect)

# Draw chessboard columns
def draw_columns():
    for i, col_value in enumerate(FILE_NAMES):
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
    global highlight, mouse_x, mouse_y

    square_rect = pygame.Rect(chess_x - 2, chess_y - 2, square_width + 4, square_width + 4)
    pygame.draw.rect(screen, white, square_rect, width = 2 )

    # Get the mouse coordinates
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Determine the clicked square
    clicked_column = (mouse_x - chess_x) // square_size
    clicked_row = (mouse_y - chess_y) // square_size

    # Check if the click is within the chessboard boundaries
    if 0 <= clicked_row < rows and 0 <= clicked_column < columns:
        value = clicked_row*8 + clicked_column
        clicked_square_value = squares[value]
        print(f"Mouse clicked at Square : {clicked_square_value}")
        #Change the border to white when clicked
        highlight = True

    else:
        print(f"Mouse clicked at ({mouse_x}, {mouse_y})")
        highlight = False

def highlight_square(mouse_x, mouse_y):
    # Determine the clicked square
    clicked_column = (mouse_x - chess_x) // square_size
    clicked_row = (mouse_y - chess_y) // square_size

    x = chess_x + (clicked_column * square_size)
    y = chess_y + (clicked_row * square_size)

    square_rect = pygame.Rect(x, y, square_size, square_size)
    pygame.draw.rect(screen, gold, square_rect, width = 2 )

def game():
    draw_chessboard(rows, columns)
    handle_events()

    # Update the display
    pygame.display.flip()

while __name__ == "__main__":
    game()

