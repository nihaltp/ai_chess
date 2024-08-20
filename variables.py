# Move history folder
directory = "game_records"

# Stockfish
stockfish_path = r"stockfish\stockfish-windows-x86-64-sse41-popcnt.exe"  # Path to the Stockfish executable
skill_level = 10  # Adjust the skill level here (0-20)
depth = 15  # Adjust the depth limit here (lower depth = easier, higher = harder)
time_stockfish = 2.0  # Time in seconds for stockfish
time_limit = 2.0 # Time that can be added to stockfish

# Draw text
draw_offer_text = "Do you want to offer a draw?"
draw_accept_text = "Do you want to accept the draw?"

# Variables
move = ""
previous_move = ""
selected_piece = None
highlight = False
check = False

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