import sys
import chess
import pygame
from config import *

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
    draw_columns()

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
def draw_columns():
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
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
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

def get_player_names():
    player1 = input("Enter Player 1's name: ")
    player2 = input("Enter Player 2's name: ")
    return player1, player2

def play_game(player1, player2):
    player1_moves = []  # Store Player 1's moves separately
    player2_moves = []  # Store Player 2's moves separately
    current_player = 0
    players = [player1, player2]
    board = chess.Board()

    while not board.is_game_over():
        print(board)
        print(f"{players[current_player]}'s turn.")
        move = (input("Enter your move (e.g., e2e4): ")).lower()


        if move in ["exit", "stop"]:
            break

        else:
            try:
                move = chess.Move.from_uci(move)
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

    play_again = input("Do you want to play again? Reply with 'Y' for yes: ")
    if play_again.lower() in ["yes", "y"]:
        change_names = input("Do you want to change your names? Reply with 'Y' for yes: ")
        if change_names.lower() in ["yes", "y"]:
            player1, player2 = get_player_names()
        play_game(player1, player2)

if __name__ == "__main__":
    player1, player2 = get_player_names()
    board = chess.Board()
    play_game(player1, player2)

# Initialize Pygame
pygame.init()

# Create the Pygame window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("AI Chess")

# Pygame font setup
pygame.font.init()
font = pygame.font.SysFont(None, 30)

while __name__ == "__main__":
    game()