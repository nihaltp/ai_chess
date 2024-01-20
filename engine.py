import pickle
from config import *
from icecream import ic

# Load the transposition table from a file if it exists
try:
    with open(TRANSPOSITION_TABLE_FILE, "rb") as file:
        transposition_table = pickle.load(file)
except FileNotFoundError:
    transposition_table = {}

# Function to generate possible moves for a given position
def generate_moves(board):
    moves = []
    for move in board.legal_moves:
        moves.append(move.uci())
    return moves

# Evaluation function
def evaluate_position(chessboard):
    # Implement a simple evaluation based on piece values for now
    # TODO: Add more advanced evaluation techniques
    # TODO: Modify VALUE dictionary
    evaluation = 0
    for square in SQUARES:
        piece = chessboard[square]
        ic(square, piece)
        if piece != "NA":
            value = VALUE[piece]
            evaluation += value
            ic(piece, value, evaluation)

    return evaluation

# Minimax algorithm
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        position_key = board.board_fen()
        if position_key in transposition_table:
            return transposition_table[position_key]
        else:
            evaluation = evaluate_position(chessboard)
            transposition_table[position_key] = evaluation
            return evaluation

    legal_moves = generate_moves(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push_uci(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            board.pop()

            if beta <= alpha:
                break  # Beta cut-off
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push_uci(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            board.pop()

            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval

# Save the transposition table to a file
def save_transposition():
    with open(TRANSPOSITION_TABLE_FILE, "wb") as file:
        pickle.dump(transposition_table, file)

# Function to get the best move using minimax
def best_move(board, depth):
    legal_moves = generate_moves(board)
    best_score = float('-inf')
    best_move = None

    for move in legal_moves:
        board.push_uci(move)
        score = minimax(board, depth, float('-inf'), float('inf'), False)  # Adjust depth as needed
        board.pop()

        if score > best_score:
            best_score = score
            best_move = move

    save_transposition()
    return best_move