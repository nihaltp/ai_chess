import pygame

# Constants
width = 700
height = 500
SQUARE_WIDTH = 400
ROWS = 8
COLUMNS = 8
SQUARE_SIZE = SQUARE_WIDTH // COLUMNS

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

PIECE_IMAGE = {
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
SQUARES = [
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
WHITE = (255, 255, 255)
BLACK = (192, 192, 192)
GOLD = (255, 215, 0)

TEXT_COLOR = WHITE
BACKGROUND = (135, 206, 250)
BOARD_BORDER = (0, 0, 0)
