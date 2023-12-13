import chess
import pygame
from settings import *

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

def history(player1_moves,player2_moves):
    max_moves = max(len(player1_moves), len(player2_moves))
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

def is_draw(player1_moves, player2_moves, players, current_player):
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

# Function to print game result
def print_result(player1_moves, player2_moves, player1, player2):
    max_moves = max(len(player1_moves), len(player2_moves))
    print("\nGame history:")
    for i in range(max_moves):
        move1 = player1_moves[i].uci() if i < len(player1_moves) else "N/A"
        move2 = player2_moves[i].uci() if i < len(player2_moves) else "N/A"
        print(f"{player1} : {move1}, {player2} : {move2}")

# Draw chessboard
def draw_chessboard(ROWS, COLUMNS):
    global highlight, mouse_x, mouse_y

    screen.fill(BACKGROUND)
    square_rect = pygame.Rect(chess_x - 2, chess_y - 2, SQUARE_WIDTH + 4, SQUARE_WIDTH + 4)
    pygame.draw.rect(screen, BOARD_BORDER, square_rect, width = 2 )

    # Draw each square independently
    for row in range(ROWS):
        for column in range(COLUMNS):
            color = WHITE if (row + column) % 2 == 0 else GREY
            square_rect = pygame.Rect(chess_x + column * SQUARE_SIZE, chess_y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, square_rect)

            # Check chessboard configuration and blit the corresponding image
            value = row * 8 + column
            piece_key = SQUARES[value]
            piece = chessboard[piece_key]
            draw_piece(piece, square_rect)

    draw_rows()
    draw_cloumns()

    if highlight:
        highlight_square(mouse_x, mouse_y)

# Function to draw pieces on the board
def draw_piece(piece, square_rect):
    global PIECE_IMAGE

    # Get the piece image from the dictionary
    piece_img = PIECE_IMAGE.get(piece)

    if piece_img is not None:
        # Blit the piece image
        screen.blit(piece_img, square_rect.topleft)

# Draw chessboard ROWS
def draw_rows():
    for i, row_value in enumerate(RANK_NAMES):
        text = font.render(str(row_value), True, TEXT_COLOR)
        # Left
        text_rect = text.get_rect(center=(chess_x - 30, chess_y + i * SQUARE_SIZE + SQUARE_SIZE // 2))
        screen.blit(text, text_rect)
        # Right
        text_rect = text.get_rect(center=(chess_x + 430, chess_y + i * SQUARE_SIZE + SQUARE_SIZE // 2))
        screen.blit(text, text_rect)

# Draw chessboard COLUMNS
def draw_cloumns():
    for i, col_value in enumerate(FILE_NAMES):
        # Top
        text = font.render(col_value, True, TEXT_COLOR)
        text_rect = text.get_rect(center=(chess_x + i * SQUARE_SIZE + SQUARE_SIZE // 2, chess_y - 30))
        screen.blit(text, text_rect)
        # Bottom
        text_rect = text.get_rect(center=(chess_x + i * SQUARE_SIZE + SQUARE_SIZE // 2, chess_y + 430))
        screen.blit(text, text_rect)

#handle events
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_click()

#handle mouse clicks
def handle_mouse_click():
    global highlight, mouse_x, mouse_y

    square_rect = pygame.Rect(chess_x - 2, chess_y - 2, SQUARE_WIDTH + 4, SQUARE_WIDTH + 4)
    pygame.draw.rect(screen, WHITE, square_rect, width = 2 )

    # Get the mouse coordinates
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Determine the clicked square
    clicked_column = (mouse_x - chess_x) // SQUARE_SIZE
    clicked_row = (mouse_y - chess_y) // SQUARE_SIZE

    # Check if the click is within the chessboard boundaries
    if 0 <= clicked_row < ROWS and 0 <= clicked_column < COLUMNS:
        value = clicked_row*8 + clicked_column
        clicked_square_value = SQUARES[value]
        clicked_piece = chessboard[clicked_square_value]
        print(f"Mouse clicked at Square : {clicked_square_value}")
        if clicked_piece != "NA":
            print(f"Mouse clicked on : {clicked_piece}")

        #Change the border to WHITE when clicked
        highlight = True

    else:
        print(f"Mouse clicked at ({mouse_x}, {mouse_y})")
        highlight = False

def highlight_square(mouse_x, mouse_y):
    # Determine the clicked square
    clicked_column = (mouse_x - chess_x) // SQUARE_SIZE
    clicked_row = (mouse_y - chess_y) // SQUARE_SIZE

    x = chess_x + (clicked_column * SQUARE_SIZE)
    y = chess_y + (clicked_row * SQUARE_SIZE)

    square_rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
    pygame.draw.rect(screen, GOLD, square_rect, width = 2 )

def game():
    draw_chessboard(ROWS, COLUMNS)
    handle_events()

    # Update the display
    pygame.display.flip()

def play_game(player1, player2):
    player1_moves = []  # Store Player 1's moves separately
    player2_moves = []  # Store Player 2's moves separately
    current_player = 0
    players = [player1, player2]
    board = chess.Board()

    while not board.is_game_over():
        print_board(board)
        print(f"{players[current_player]}'s turn.")
        move = input("Enter your move (e.g., e2e4): ")

        if move.lower() in ["history", "hist", "moves", "move", "m"]:
            history(player1_moves,player2_moves)
            continue

        elif move.lower() in ["hint", "hints", "h"]:
            valid_moves(board)
            continue

        elif move.lower() in ["undo", "u"]:
            undo(players,player1_moves,player2_moves,board)
            continue  # Allow the player to input a new move

        elif move.lower() in ["draw", "d"]:
            if is_draw(player1_moves, player2_moves, players, current_player):
                break
            continue

        elif move.lower() in ["exit", "stop"]:
            break

        else:
            try:
                move = chess.Move.from_uci(move.lower())
                print(f"\033[92mMove confirmed: {move.uci()}.\033[0m")  # Added move confirmation prompt
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
                        print(f"\033[91mCheck! {players[current_player]} is in check!\033[0m")
                else:
                    print("Invalid move! Try again.")
            except ValueError:
                print("Invalid move format! Use UCI format (e.g., e2e4).")


    print("\033[93mGame over.\033[0m")
    print("\033[95mResult: " + board.result() + "\033[0m")  # Enhanced game over message

    print_result(player1_moves, player2_moves, player1, player2)

    # Save moves to a file
    save_to_file(player1_moves, player2_moves, player1, player2)

    play_again = input("Do you want to play again? Reply with 'Y' for yes: ")
    if play_again.lower() in ["yes", "y"]:
        change_names = input("Do you want to change your names? Reply with 'Y' for yes: ")
        if change_names.lower() in ["yes", "y"]:
            player1, player2 = get_player_names()
        play_game(player1, player2)

player1, player2 = get_player_names()
board = chess.Board()

# Initialize Pygame
pygame.init()

# Create the Pygame window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("AI Chess")

# Pygame font setup
pygame.font.init()
font = pygame.font.SysFont(None, 30)

print("""Available features:
    Undo
    Draw
    History
    """)

while True:
    draw_chessboard(ROWS, COLUMNS)
    handle_events()

    # Update the display
    pygame.display.flip()