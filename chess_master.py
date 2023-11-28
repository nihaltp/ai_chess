import chess

def get_player_names():
    player1 = input("Enter Player 1's name: ")
    player2 = input("Enter Player 2's name: ")
    return player1, player2

def offer_draw():
    draw_offer = input("Do you want to offer a draw? (yes/no): ")
    if draw_offer.lower() in ["yes", "y"]:
        return True

def accept_draw():
    draw_accept = input("Do you accept the draw offer? (yes/no): ")
    if draw_accept.lower() in ["yes", "y"]:
        return True

def valid_moves(board):
    print("Valid Moves:")
    for move in board.legal_moves:
        print(move.uci())

def history(max_moves,player1_moves,player2_moves):
    for i in range(max_moves):
        move1 = player1_moves[i].uci() if i < len(player1_moves) else "N/A"
        move2 = player2_moves[i].uci() if i < len(player2_moves) else "N/A"
        print(f"{player1} : {move1}, {player2} : {move2}")

def undo(players,player1_moves,player2_moves,board):
    if len(player1_moves) >= 1 or len(player2_moves) >= 1:
        last_move_player1 = None
        last_move_player2 = None

        if len(player1_moves) >= 1:
            last_move_player1 = player1_moves.pop()  # Remove Player 1's last move
            board.pop()  # Undo last move on the board
        else:
            last_move_player1 = None
                
        if len(player2_moves) >= 1:
            last_move_player2 = player2_moves.pop()  # Remove Player 2's last move
            board.pop()  # Undo last move on the board
        else:
            last_move_player2 = None
                    
        if last_move_player1 is not None:
            print(f"{players[0]} undid their last move: {last_move_player1.uci()}")
        if last_move_player2 is not None:
            print(f"{players[1]} undid their last move: {last_move_player2.uci()}")

    else:
        print("No moves to undo.")

def is_draw(player1_moves,player2_moves):
    if len(player1_moves) >= 2 and len(player2_moves) >= 2:
        print("Draw conditions are satisfied.")
        if offer_draw():
            if accept_draw():
                print("The game is a draw by agreement.")
                return True
            else:
                print(f"{players[current_player]} declined the draw offer.")
        else:
            print(f"{players[current_player]} declined the draw offer.")
    else:
        print("Draw offer rejected. Both players need to have made at least two moves.")

# Function to print the chessboard
def print_board(board):
    print("  a b c d e f g h")
    print(" +----------------")
    rows = str(board).split('\n')
    for i, row in enumerate(rows):
        print(f"{8 - i}| {row}")

# Function to save moves to a text file
def save_to_file(player1_moves, player2_moves, player1, player2):
    p1s = str(player1)
    p2s = str(player2)
    p1r = p1s.replace(" ", "_")
    p2r = p2s.replace(" ", "_")
    file = (p1r+"_"+p2r+".txt")
    with open(file, 'a') as file:
        file.write(f"Game between {player1} and {player2}:\n")
        for move1, move2 in zip(player1_moves, player2_moves):
            file.write(f"{player1}: {move1.uci()}, {player2}: {move2.uci()}\n")
    
def play_game(player1, player2):
    player1_moves = []  # Store Player 1's moves separately
    player2_moves = []  # Store Player 2's moves separately
    current_player = 0
    players = [player1, player2]
    board = chess.Board()

    while not board.is_game_over():
        max_moves = max(len(player1_moves), len(player2_moves))  # Calculate max_moves here
        print_board(board)
        print(f"{players[current_player]}'s turn.")
        move = input("Enter your move (e.g., e2e4): ")

        if move.lower() in ["history", "hist", "moves", "move", "m"]:
            history(max_moves,player1_moves,player2_moves)
            continue

        if move.lower() in ["hint", "hints", "h"]:
            valid_moves(board)
            continue

        if move.lower() in ["undo", "u"]:
            undo(players,player1_moves,player2_moves,board)
            continue  # Allow the player to input a new move

        if move.lower() in ["draw", "d"]:
            if is_draw(player1_moves,player2_moves):
                break
            continue

        try:
            move = chess.Move.from_uci(move.lower())
            if move in board.legal_moves:
                if board.is_castling(move):  # Check for castling
                    board.push(move)  # Perform castling
                    if move.from_square == chess.E1 and move.to_square == chess.G1:  # Kingside castling for white
                        board.push(chess.Move.from_uci("e1g1"))  # Move the King
                        board.push(chess.Move.from_uci("h1f1"))  # Move the Rook

                    elif move.from_square == chess.E1 and move.to_square == chess.C1:  # Queenside castling for white
                        board.push(chess.Move.from_uci("e1c1"))  # Move the King
                        board.push(chess.Move.from_uci("a1d1"))  # Move the Rook

                    elif move.from_square == chess.E8 and move.to_square == chess.G8:  # Kingside castling for black
                        board.push(chess.Move.from_uci("e8g8"))  # Move the King
                        board.push(chess.Move.from_uci("h8f8"))  # Move the Rook

                    elif move.from_square == chess.E8 and move.to_square == chess.C8:  # Queenside castling for black
                        board.push(chess.Move.from_uci("e8c8"))  # Move the King
                        board.push(chess.Move.from_uci("a8d8"))  # Move the Rook

                else:
                    board.push(move)  # For normal moves

                if current_player == 0:
                    player1_moves.append(move)  # Store Player 1's move
                else:
                    player2_moves.append(move)  # Store Player 2's move

                current_player = 1 - current_player  # Switch players

                if board.is_checkmate():
                    print(f"Checkmate! {players[current_player]} wins.")
                    break
                elif board.is_stalemate():
                    print("Stalemate! The game is a draw.")
                    break
                elif board.is_insufficient_material():
                    print("Insufficient material! The game is a draw.")
                    break
                elif board.is_check():
                    print("Check!")
            else:
                print("Invalid move! Try again.")
        except ValueError:
            print("Invalid move format! Use UCI format (e.g., e2e4).")

    print("Game over.")
    print("Result: " + board.result())

    print("\nGame history:")
    for i in range(max_moves):
        max_moves = max(len(player1_moves), len(player2_moves))
        move1 = player1_moves[i].uci() if i < len(player1_moves) else "N/A"
        move2 = player2_moves[i].uci() if i < len(player2_moves) else "N/A"
        print(f"{player1} : {move1}, {player2} : {move2}")

    save_to_file(player1_moves, player2_moves, player1, player2)  # Save moves to a file

    play_again = input("Do you want to play again? Reply with 'Y' for yes: ")
    if play_again.lower() in ["yes", "y"]:
        change_names = input("Do you want to change your names? Reply with 'Y' for yes: ")
        if change_names.lower() in ["yes", "y"]:
            player1, player2 = player_names()
        play_game(player1, player2)

print("""Available features:
    Undo
    Draw
    History
    """)

if __name__ == "__main__":
    player1, player2 = get_player_names()
    board = chess.Board()
    play_game(player1, player2)
