import sys
import time
import chess
import pygame
from config import *
from icecream import ic

def highlight_square(value1, value2, colour):
    x = CHESS_X + (value1 * SQUARE_SIZE)
    y = CHESS_Y + (value2 * SQUARE_SIZE)
 
    square_rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
    pygame.draw.rect(screen, colour, square_rect, width = 2 )

def highlight_move(move):
        # Find the location
        value = SQUARES.index(move)

        a = value/8
        row = int(a)
        column = (a - row)*8
        highlight_square(column, row, GOLD)

        pygame.display.flip()

def valid_moves(board):
    for move in board.legal_moves:
        # clear the chessboard after every hint
        draw_chessboard(ROWS, COLUMNS)

        move = move.uci()
        move_1 = move[:2] 
        highlight_move(move_1)
        move_2 = move[2:]
        highlight_move(move_2)

        # wait a second
        time.sleep(1)

def draw_text_at_location(text, x, y):
    text = font.render(str(text), True, TEXT_COLOR)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)

# Draw chessboard ROWS
def draw_rows():
    for i, row_value in enumerate(RANK_NAMES):
        # Left
        draw_text_at_location(row_value, CHESS_X - 30, CHESS_Y + i * SQUARE_SIZE + SQUARE_SIZE // 2)
        # Right
        draw_text_at_location(row_value, CHESS_X + 430, CHESS_Y + i * SQUARE_SIZE + SQUARE_SIZE // 2)

# Draw chessboard COLUMNS
def draw_columns():
    for i, column_value in enumerate(FILE_NAMES):
        # Top
        draw_text_at_location(column_value, CHESS_X + i * SQUARE_SIZE + SQUARE_SIZE // 2, CHESS_Y - 30)
        # Bottom
        draw_text_at_location(column_value, CHESS_X + i * SQUARE_SIZE + SQUARE_SIZE // 2, CHESS_Y + 430)

# Function to draw pieces on the board
def draw_piece(piece, square_rect):
    # Get the piece image from the dictionary
    piece_img = PIECE_IMAGE.get(piece)

    if piece_img is not None:
        # Blit the piece image
        screen.blit(piece_img, square_rect.topleft)

# Draw chessboard
def draw_chessboard(ROWS, COLUMNS):
    global highlight, mouse_x, mouse_y

    screen.fill(BACKGROUND)
    square_rect = pygame.Rect(CHESS_X - 2, CHESS_Y - 2, SQUARE_WIDTH + 4, SQUARE_WIDTH + 4)
    pygame.draw.rect(screen, BOARD_BORDER, square_rect, width = 2 )

    # Draw each square independently
    for row in range(ROWS):
        for column in range(COLUMNS):
            draw_square(row, column)

    draw_rows()
    draw_columns()

    if highlight:
        # Determine the clicked square
        clicked_column = (mouse_x - CHESS_X) // SQUARE_SIZE
        clicked_row = (mouse_y - CHESS_Y) // SQUARE_SIZE

        highlight_square(clicked_column, clicked_row, GOLD)

def draw_square(row, column):
    color = WHITE if (row + column) % 2 == 0 else GREY
    square_rect = pygame.Rect(CHESS_X + column * SQUARE_SIZE, CHESS_Y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    pygame.draw.rect(screen, color, square_rect)

    # Check chessboard configuration and blit the corresponding image
    value = row * 8 + column
    piece_key = SQUARES[value]
    piece = chessboard[piece_key]
    draw_piece(piece, square_rect)

def handle_buttons(mouse_x, mouse_y):
    global player1_moves, player2_moves, board, players, current_player

    if BUTTON_HISTORY_POS[0] <= mouse_x <= BUTTON_HISTORY_POS[0] + BUTTON_WIDTH and BUTTON_HISTORY_POS[1] <= mouse_y <= BUTTON_HISTORY_POS[1] + BUTTON_HEIGHT:
        history(player1_moves,player2_moves)
        ic()

    elif BUTTON_HINT_POS[0] <= mouse_x <= BUTTON_HINT_POS[0] + BUTTON_WIDTH and BUTTON_HINT_POS[1] <= mouse_y <= BUTTON_HINT_POS[1] + BUTTON_HEIGHT:
        valid_moves(board)
        ic()

    elif BUTTON_UNDO_POS[0] <= mouse_x <= BUTTON_UNDO_POS[0] + BUTTON_WIDTH and BUTTON_UNDO_POS[1] <= mouse_y <= BUTTON_UNDO_POS[1] + BUTTON_HEIGHT:
        undo(players,player1_moves,player2_moves,board)
        ic()

    elif BUTTON_DRAW_POS[0] <= mouse_x <= BUTTON_DRAW_POS[0] + BUTTON_WIDTH and BUTTON_DRAW_POS[1] <= mouse_y <= BUTTON_DRAW_POS[1] + BUTTON_HEIGHT:
        # if is_draw(player1_moves, player2_moves, players, current_player):
        #     ic()
        ic()

    elif BUTTON_STOP_POS[0] <= mouse_x <= BUTTON_STOP_POS[0] + BUTTON_WIDTH and BUTTON_STOP_POS[1] <= mouse_y <= BUTTON_STOP_POS[1] + BUTTON_HEIGHT:
        pygame.quit()
        sys.exit()

#handle mouse clicks
def handle_mouse_click():
    global highlight, mouse_x, mouse_y, move

    # Get the mouse coordinates
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Determine the clicked square
    clicked_column = (mouse_x - CHESS_X) // SQUARE_SIZE
    clicked_row = (mouse_y - CHESS_Y) // SQUARE_SIZE

    # Check if the click is within the chessboard boundaries
    if 0 <= clicked_row < ROWS and 0 <= clicked_column < COLUMNS:
        value = int(clicked_row*8 + clicked_column)
        clicked_square_value = SQUARES[value]
        
        if len(move) != 4:
            move += clicked_square_value
        elif len(move) == 4:
            move = clicked_square_value

        #Change the border to WHITE when clicked
        highlight = True

    else:
        handle_buttons(mouse_x, mouse_y)
        highlight = False
        move = ""

    return move

def update(board):
    board_value = str(board).replace(" ", "").replace("\n", "")
    for i, j in zip(board_value, SQUARES):
        # Get the piece image from the dictionary
        chessboard[j] = PIECE_VALUE.get(i)

def draw_buttons():
    history_button = pygame.Rect(BUTTON_HISTORY_POS, (BUTTON_WIDTH, BUTTON_HEIGHT))
    hint_button = pygame.Rect(BUTTON_HINT_POS, (BUTTON_WIDTH, BUTTON_HEIGHT))
    undo_button = pygame.Rect(BUTTON_UNDO_POS, (BUTTON_WIDTH, BUTTON_HEIGHT))
    draw_button = pygame.Rect(BUTTON_DRAW_POS, (BUTTON_WIDTH, BUTTON_HEIGHT))
    stop_button = pygame.Rect(BUTTON_STOP_POS, (BUTTON_WIDTH, BUTTON_HEIGHT))

    pygame.draw.rect(screen, BUTTON_COLOR, history_button)
    pygame.draw.rect(screen, BUTTON_COLOR, hint_button)
    pygame.draw.rect(screen, BUTTON_COLOR, undo_button)
    pygame.draw.rect(screen, BUTTON_COLOR, draw_button)
    pygame.draw.rect(screen, BUTTON_COLOR, stop_button)

    font_buttons = pygame.font.SysFont(None, 24)
    text_history = font_buttons.render("History", True, TEXT_COLOR)
    text_hint = font_buttons.render("Hint", True, TEXT_COLOR)
    text_undo = font_buttons.render("Undo", True, TEXT_COLOR)
    text_draw = font_buttons.render("Draw", True, TEXT_COLOR)
    text_stop = font_buttons.render("Stop", True, TEXT_COLOR)

    screen.blit(text_history, (BUTTON_HISTORY_POS[0] + BUTTON_MARGIN_x, BUTTON_HISTORY_POS[1] + BUTTON_MARGIN_Y))
    screen.blit(text_hint, (BUTTON_HINT_POS[0] + BUTTON_MARGIN_x, BUTTON_HINT_POS[1] + BUTTON_MARGIN_Y))
    screen.blit(text_undo, (BUTTON_UNDO_POS[0] + BUTTON_MARGIN_x, BUTTON_UNDO_POS[1] + BUTTON_MARGIN_Y))
    screen.blit(text_draw, (BUTTON_DRAW_POS[0] + BUTTON_MARGIN_x, BUTTON_DRAW_POS[1] + BUTTON_MARGIN_Y))
    screen.blit(text_stop, (BUTTON_STOP_POS[0] + BUTTON_MARGIN_x, BUTTON_STOP_POS[1] + BUTTON_MARGIN_Y))
    
def game(board):
    update(board)
    draw_chessboard(ROWS, COLUMNS)
    draw_buttons()

    # Update the display
    pygame.display.flip()

def input_text(prompt, position):
    input_active = True
    input_text = []

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.unicode == "\r":
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text.append(event.unicode)

        screen.fill(BACKGROUND)

        # Display the input text
        current_text = ''.join(input_text)
        value = f"{prompt} {current_text}"
        text = font.render(value, True, BLACK)
        text_rect = text.get_rect(topleft = position)
        screen.blit(text, text_rect)
        pygame.display.flip()

    return current_text

def get_name():
    # Get Player names
    player1 = input_text("Enter Player 1's name: ", (200, 100))
    player2 = input_text("Enter Player 2's name: ", (200, 100))
    return player1, player2

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

def accept_draw():
    draw_accept = input("Do you accept the draw offer? (yes/no): ")
    if draw_accept.lower() in ["yes", "y"]:
        return True

def offer_draw():
    draw_offer = input("Do you want to offer a draw? (yes/no): ")
    if draw_offer.lower() in ["yes", "y"]:
        return True

def is_draw(player1_moves, player2_moves, players, current_player):
    if len(player1_moves) < 2 and len(player2_moves) < 2:
        print("Draw offer rejected. Both players need to have made at least two moves.")
        return

    print("\nDraw conditions are satisfied.")

    if not offer_draw():
        print(f"{players[current_player]} declined the draw offer.\n")
        return
    
    if accept_draw():
        print("The game is a draw by agreement.")
        return True
    else:
        player = 1 - current_player  # Switch player
        print(f"{players[player]} declined the draw offer.\n")

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

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            move = handle_mouse_click()
            return move

def play_game(player1, player2):
    global player1_moves, player2_moves, board, players, current_player
    player1_moves = []  # Store Player 1's moves separately
    player2_moves = []  # Store Player 2's moves separately
    current_player = 0
    players = [player1, player2]
    board = chess.Board()

    while not board.is_game_over():
        game(board)
        move = handle_events()

        if move != None:
            ic(move)

        if move == None:
            continue
        
        elif len(move) == 2:
            continue

        else:
            try:
                move = chess.Move.from_uci(move)
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
            except ValueError:
                ic()

    print("\033[93mGame over.\033[0m")
    print("\033[95mResult: " + board.result() + "\033[0m")  # Enhanced game over message

    print_result(player1_moves, player2_moves, player1, player2)

    # Save moves to a file
    save_to_file(player1_moves, player2_moves, player1, player2)

    play_again = input("Do you want to play again? Reply with 'Y' for yes: ")
    if play_again.lower() in ["yes", "y"]:
        change_names = input("Do you want to change your names? Reply with 'Y' for yes: ")
        if change_names.lower() in ["yes", "y"]:
            player1, player2 = get_name()
        play_game(player1, player2)

if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()

    # Create the Pygame window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AI Chess")

    # Pygame font setup
    pygame.font.init()
    font = pygame.font.SysFont(None, 28)

    player1, player2 = get_name()
    play_game(player1, player2)
