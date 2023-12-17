import pygame

# Constants
SCREEN_WIDTH = 700.0
SCREEN_HEIGHT = 700.0

ROWS = 8
COLUMNS = 8
SQUARE_WIDTH = 400.0
SQUARE_SIZE = SQUARE_WIDTH // COLUMNS

# Where to start the chess board
CHESS_X = (SCREEN_WIDTH - SQUARE_WIDTH)/2
CHESS_Y = (SCREEN_HEIGHT - SQUARE_WIDTH)/2

# Buttons
BUTTON_WIDTH = SCREEN_WIDTH/8
BUTTON_HEIGHT = SQUARE_WIDTH/10
BUTTON_MARGIN_x = BUTTON_WIDTH/4
BUTTON_MARGIN_Y = BUTTON_HEIGHT/10
BUTTON_X = CHESS_X+450
BUTTON_Y = CHESS_Y

BUTTON_HISTORY_POS = (BUTTON_X, BUTTON_Y+50)
BUTTON_HINT_POS = (BUTTON_X, BUTTON_Y+100)
BUTTON_UNDO_POS = (BUTTON_X, BUTTON_Y+150)
BUTTON_DRAW_POS = (BUTTON_X, BUTTON_Y+200)
BUTTON_STOP_POS = (BUTTON_X, BUTTON_Y+250)

BUTTON_POSITIONS = {
    'History': BUTTON_HISTORY_POS,
    'Hint': BUTTON_HINT_POS,
    'Undo': BUTTON_UNDO_POS,
    'Draw': BUTTON_DRAW_POS,
    'Stop': BUTTON_STOP_POS
}

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (192, 192, 192)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
BLUE = (135, 206, 250)
BLUE_1 = (70, 130, 180)  # a shade of blue

TEXT_COLOR = WHITE
BACKGROUND = BLUE
BOARD_BORDER = BLACK 
BUTTON_COLOR = BLUE_1

# Variables
move = ""
selected_piece = None
highlight = False

#import images
pawn_w = pygame.image.load("pieces/pawn_w.png")
knight_w = pygame.image.load("pieces/knight_w.png")
bishop_w = pygame.image.load("pieces/bishop_w.png")
rook_w = pygame.image.load("pieces/rook_w.png")
queen_w = pygame.image.load("pieces/queen_w.png")
king_w = pygame.image.load("pieces/king_w.png")
pawn_b = pygame.image.load("pieces/pawn_b.png")
knight_b = pygame.image.load("pieces/knight_b.png")
bishop_b = pygame.image.load("pieces/bishop_b.png")
rook_b = pygame.image.load("pieces/rook_b.png")
queen_b = pygame.image.load("pieces/queen_b.png")
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

PIECE_VALUE = {
    ".": "NA",
    "P": "pawn_w",
    "R": "rook_w",
    "N": "knight_w",
    "B": "bishop_w",
    "Q": "queen_w",
    "K": "king_w",
    "p": "pawn_b",
    "r": "rook_b",
    "n": "knight_b",
    "b": "bishop_b",
    "q": "queen_b",
    "k": "king_b",
}

FILE_NAMES = ["a", "b", "c", "d", "e", "f", "g", "h"]
RANK_NAMES = ["8", "7", "6", "5", "4", "3", "2", "1"]

# Create a 2D list to represent the chessboard with values
SQUARES = [
    'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
    'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
    'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
    'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
    'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
    'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
    'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
    'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'
]

SQUARES_NUMBER = [
    "0", "1", "2", "3", "4", "5", "6", "7",
    "8", "9", "10", "11", "12", "13", "14",
    "15", "16", "17", "18", "19", "20", "21",
    "22", "23", "24", "25", "26", "27", "28",
    "29", "30", "31", "32", "33", "34", "35",
    "36", "37", "38", "39", "40", "41", "42",
    "43", "44", "45", "46", "47", "48", "49",
    "50", "51", "52", "53", "54", "55", "56",
    "57", "58", "59", "60", "61", "62", "63",
]

# Complete Chessboard with Pieces
chessboard = {
    "a1": "rook_w", "b1": "knight_w", "c1": "bishop_w", "d1": "queen_w", "e1": "king_w", "f1": "bishop_w", "g1": "knight_w", "h1": "rook_w",
    "a2": "pawn_w", "b2": "pawn_w", "c2": "pawn_w", "d2": "pawn_w", "e2": "pawn_w", "f2": "pawn_w", "g2": "pawn_w", "h2": "pawn_w",
    "a3": "NA", "b3": "NA", "c3": "NA", "d3": "NA", "e3": "NA", "f3": "NA", "g3": "NA", "h3": "NA",
    "a4": "NA", "b4": "NA", "c4": "NA", "d4": "NA", "e4": "NA", "f4": "NA", "g4": "NA", "h4": "NA",
    "a5": "NA", "b5": "NA", "c5": "NA", "d5": "NA", "e5": "NA", "f5": "NA", "g5": "NA", "h5": "NA",
    "a6": "NA", "b6": "NA", "c6": "NA", "d6": "NA", "e6": "NA", "f6": "NA", "g6": "NA", "h6": "NA",
    "a7": "pawn_b", "b7": "pawn_b", "c7": "pawn_b", "d7": "pawn_b", "e7": "pawn_b", "f7": "pawn_b", "g7": "pawn_b", "h7": "pawn_b",
    "a8": "rook_b", "b8": "knight_b", "c8": "bishop_b", "d8": "queen_b", "e8": "king_b", "f8": "bishop_b", "g8": "knight_b", "h8": "rook_b",
}