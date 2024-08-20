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
BUTTON_MARGIN_X = BUTTON_WIDTH // 2
BUTTON_MARGIN_Y = BUTTON_HEIGHT // 2
BUTTON_X = CHESS_X+450
BUTTON_Y = CHESS_Y

BUTTON_HISTORY = (BUTTON_X, BUTTON_Y+50)
BUTTON_HINT = (BUTTON_X, BUTTON_Y+100)
BUTTON_UNDO = (BUTTON_X, BUTTON_Y+150)
BUTTON_DRAW = (BUTTON_X, BUTTON_Y+200)
BUTTON_STOP = (BUTTON_X, BUTTON_Y+250)

PAWN_BUTTON_WIDTH = SCREEN_WIDTH//7
PAWN_BUTTON_HEIGHT = SCREEN_HEIGHT//7
PAWN_BUTTON_X = PAWN_BUTTON_WIDTH
PAWN_BUTTON_Y = PAWN_BUTTON_HEIGHT

PAWN_IMAGE_MARGIN = (PAWN_BUTTON_HEIGHT + PAWN_BUTTON_WIDTH)//20

BUTTON_QUEEN = (PAWN_BUTTON_X, PAWN_BUTTON_Y)
BUTTON_ROOK = (PAWN_BUTTON_X + PAWN_BUTTON_WIDTH*2 , PAWN_BUTTON_Y)
BUTTON_KNIGHT = (PAWN_BUTTON_X, PAWN_BUTTON_Y + PAWN_BUTTON_HEIGHT*2)
BUTTON_BISHOP = (PAWN_BUTTON_X + PAWN_BUTTON_WIDTH*2, PAWN_BUTTON_Y + PAWN_BUTTON_HEIGHT*2)

BUTTONS = [
    "History",
    "Hint",
    "Undo",
    "Draw",
    "Stop"
]

BUTTON_POSITIONS = {
    "History": BUTTON_HISTORY,
    "Hint": BUTTON_HINT,
    "Undo": BUTTON_UNDO,
    "Draw": BUTTON_DRAW,
    "Stop": BUTTON_STOP,

    "queen": BUTTON_QUEEN,
    "rook": BUTTON_ROOK,
    "knight": BUTTON_KNIGHT,
    "bishop": BUTTON_BISHOP
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

FILE_NAMES = ["a", "b", "c", "d", "e", "f", "g", "h"]
RANK_NAMES = ["8", "7", "6", "5", "4", "3", "2", "1"]

# Create a 2D list to represent the chessboard with values
SQUARES = [
    "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8",
    "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
    "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",
    "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
    "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
    "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
    "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
    "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"
]