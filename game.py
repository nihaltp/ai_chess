import os
import sys
import time
import chess
import chess.engine
import random
import pygame
from config import *
from icecream import ic

def highlight_square(value1, value2, colour):
    x = CHESS_X + (value1 * SQUARE_SIZE)
    y = CHESS_Y + (value2 * SQUARE_SIZE)

    square_rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
    pygame.draw.rect(screen, colour, square_rect, width = 2 )

def highlight_move(move,colour):
    if len(move) != 2:
        move = move[:2]
    value = SQUARES.index(move)
    row, column = divmod(value, 8)
    highlight_square(column, row, colour)
    pygame.display.flip()

def valid_moves(board):
    for move in board.legal_moves:
        # clear the chessboard after every hint
        draw_chessboard(ROWS, COLUMNS)

        move = move.uci()
        move_1 = move[:2] 
        highlight_move(move_1, RED)
        move_2 = move[2:]
        highlight_move(move_2, GOLD)

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
    global highlight, mouse_x, mouse_y, previous_move

    screen.fill(BACKGROUND)
    square_rect = pygame.Rect(CHESS_X - 2, CHESS_Y - 2, SQUARE_WIDTH + 4, SQUARE_WIDTH + 4)
    pygame.draw.rect(screen, BOARD_BORDER, square_rect, width = 2 )

    # Draw each square independently
    for row in range(ROWS):
        for column in range(COLUMNS):
            draw_square(row, column)

    draw_rows()
    draw_columns()
    draw_buttons()

    if highlight:
        # Determine the clicked square
        clicked_column = (mouse_x - CHESS_X) // SQUARE_SIZE
        clicked_row = (mouse_y - CHESS_Y) // SQUARE_SIZE

        if len(move) == 2:
            highlight_square(clicked_column, clicked_row, RED)
        else:
            highlight_square(clicked_column, clicked_row, GOLD)

    if previous_move != "":
        value = previous_move.uci()
        move_2 = value[2:]
        highlight_move(move_2, BLUE_1)

    if check:
        for i in chessboard:
            if chessboard[i] == "king_w" and current_player == 0 or chessboard[i] == "king_b" and current_player == 1:
                highlight_move(i, RED)
                break

def draw_square(row, column):
    color = WHITE if (row + column) % 2 == 0 else GREY
    square_rect = pygame.Rect(CHESS_X + column * SQUARE_SIZE, CHESS_Y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    pygame.draw.rect(screen, color, square_rect)

    # Check chessboard configuration and blit the corresponding image
    value = row * 8 + column
    piece_key = SQUARES[value]
    piece = chessboard[piece_key]
    draw_piece(piece, square_rect)

def button_action(button_name):
    global player1_moves, player2_moves, board, players, current_player

    if button_name == "History":
        history(player1_moves,player2_moves)
    elif button_name == "Hint":
        valid_moves(board)
    elif button_name == "Undo":
        undo(players,player1_moves,player2_moves,board)
    elif button_name == "Draw":
        if is_draw(player1_moves, player2_moves, players, current_player):
            print_result(player1_moves, player2_moves, player1, player2)
            save_to_file(player1_moves, player2_moves, player1, player2)
            pygame.quit()
            sys.exit()
    elif button_name == "Stop":
        pygame.quit()
        sys.exit()

def handle_buttons(mouse_x, mouse_y):
    for button_name, pos in BUTTON_POSITIONS.items():
        if pos[0] <= mouse_x <= pos[0] + BUTTON_WIDTH and pos[1] <= mouse_y <= pos[1] + BUTTON_HEIGHT:
            button_action(button_name)

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
    for button_name in (BUTTONS):
        button_position = BUTTON_POSITIONS[button_name]

        button = pygame.Rect(button_position, (BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(screen, BUTTON_COLOR, button)

        font_buttons = pygame.font.SysFont(None, 24)
        text = font_buttons.render(button_name, True, TEXT_COLOR)

        text_rect = text.get_rect(center=(button_position[0] + BUTTON_MARGIN_X, button_position[1] + BUTTON_MARGIN_Y))
        screen.blit(text, text_rect)

def game(board):
    update(board)
    draw_chessboard(ROWS, COLUMNS)

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
    board_history = chess.Board()
    game(board_history)
    ic(player1_moves)
    ic(player2_moves)
    max_moves = max(len(player1_moves), len(player2_moves))
    for i in range(max_moves):
        if i < len(player1_moves):
            time.sleep(0.5)
            board_history.push(player1_moves[i])
            game(board_history)
        if i < len(player2_moves):
            time.sleep(0.5)
            board_history.push(player2_moves[i])
            game(board_history)

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
            print(f"{players[0]} undid their last move: {last_move_player1}")
        if last_move_player2 is not None:
            print(f"{players[1]} undid their last move: {last_move_player2}")

    else:
        print("No moves to undo.")

def handle_draw(x1, x2, y, width1, width2, height):
    rect_x = pygame.Rect(x1, y, width1, height)
    rect_y = pygame.Rect(x2, y, width2, height)
    pygame.draw.rect(screen, BLACK, rect_x, width = 2 )
    pygame.draw.rect(screen, WHITE, rect_y, width = 2 )
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x > x1 and mouse_x < x1+width1 and mouse_y > y and mouse_y < y+height:
                return True
            if mouse_x > x2 and mouse_x < x2+width2 and mouse_y > y and mouse_y < y+height:
                return False

def draw(name_text, draw_text):
    screen.fill(BACKGROUND)
    name = font.render(name_text, True, BLACK)
    draw_accept = font.render(draw_text, True, BLACK)
    yes = font.render("Yes", True, BLACK)
    no = font.render("No", True, BLACK)

    # TODO: Add variable for dimensions below
    screen.blit(name, (BUTTON_WIDTH, PAWN_BUTTON_HEIGHT//2))
    screen.blit(draw_accept, (BUTTON_WIDTH, PAWN_BUTTON_HEIGHT))
    screen.blit(yes, (BUTTON_WIDTH, PAWN_BUTTON_HEIGHT+60))
    screen.blit(no, ((BUTTON_WIDTH*2)+10, PAWN_BUTTON_HEIGHT+60))
    pygame.display.flip()

    selected_option = None
    while selected_option is None:
        selected_option = handle_draw(BUTTON_WIDTH-5, BUTTON_WIDTH*2+5, PAWN_BUTTON_HEIGHT+55, 45, 40, 30)
    return selected_option

def is_draw(player1_moves, player2_moves, players, current_player):
    if len(player1_moves) < 2 and len(player2_moves) < 2:
        print("Draw offer rejected. Both players need to have made at least two moves.")
        return

    name_text = players[current_player]
    if not draw(name_text, draw_offer_text):
        return False
    
    name_text = players[1-current_player]
    if not draw(name_text, draw_accept_text):
        return False
    
    return True


# Function to save moves to a text file
def save_to_file(player1_moves, player2_moves, player1, player2):
    # Ensure the directory directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    p1s = str(player1)
    p2s = str(player2)
    p1r = p1s.replace(" ", "_")
    p2r = p2s.replace(" ", "_")

    # Construct the full file path
    file = os.path.join(directory, f"{p1r}_{p2r}.txt")

    with open(file, 'a') as file:
        file.write(f"Game between {player1} and {player2}:\n")
        for move1, move2 in zip(player1_moves, player2_moves):
            file.write(f"{player1}: {move1}, {player2}: {move2}\n")

# Function to print game result
def print_result(player1_moves, player2_moves, player1, player2):
    max_moves = max(len(player1_moves), len(player2_moves))
    print("\nGame history:")
    for i in range(max_moves):
        move1 = player1_moves[i] if i < len(player1_moves) else "N/A"
        move2 = player2_moves[i] if i < len(player2_moves) else "N/A"
        print(f"{player1} : {move1}, {player2} : {move2}")

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            move = handle_mouse_click()
            return move

def perform_castling(board, move):
    board.push(move)  # Perform castling
    if move == "e1g1":  # King-side castling for white
        board.push(chess.Move.from_uci("e1g1"))  # Move the King
        board.push(chess.Move.from_uci("h1f1"))  # Move the Rook

    elif move == "e1c1":  # Queen-side castling for white
        board.push(chess.Move.from_uci("e1c1"))  # Move the King
        board.push(chess.Move.from_uci("a1d1"))  # Move the Rook

    elif move == "e8g8":  # King-side castling for black
        board.push(chess.Move.from_uci("e8g8"))  # Move the King
        board.push(chess.Move.from_uci("h8f8"))  # Move the Rook

    elif move == "e8c8":  # Queen-side castling for black
        board.push(chess.Move.from_uci("e8c8"))  # Move the King
        board.push(chess.Move.from_uci("a8d8"))  # Move the Rook

def store_moves(player1_moves, player2_moves, current_player, move):
    if current_player == 0:
        player1_moves.append(move)  # Store Player 1's move
    else:
        player2_moves.append(move)  # Store Player 2's move

    current_player = 1 - current_player  # Switch players
    return current_player

# Draw buttons for pawn promotion
def draw_promotion_buttons():
    for piece_name in (["queen", "rook", "bishop", "knight"]):
        button_position = BUTTON_POSITIONS[piece_name]

        button = pygame.Rect(button_position, (PAWN_BUTTON_WIDTH, PAWN_BUTTON_HEIGHT))
        pygame.draw.rect(screen, BUTTON_COLOR, button)

        # Draw the piece image
        color = "_w" if current_player == 0 else "_b"
        piece_img = PAWN_PROMOTION_IMAGE.get(piece_name + color)
        screen.blit(piece_img, ((button_position[0] + (PAWN_BUTTON_WIDTH/2) - (piece_img.get_width()/2)), (button_position[1] + (PAWN_BUTTON_HEIGHT/2) - (piece_img.get_height()/2))))
        pygame.display.flip()

def handle_promotion():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i, piece_name in enumerate(["queen", "rook", "bishop", "knight"]):
                button_position = BUTTON_POSITIONS[piece_name]
                if button_position[0] <= mouse_x <= button_position[0] + PAWN_BUTTON_WIDTH and \
                        button_position[1] <= mouse_y <= button_position[1] + PAWN_BUTTON_HEIGHT:
                    return ["q", "r", "b", "n"][i]  # Return the selected piece
    return None

def pawn_promotion(board, move):
    global screen, font

    # Display pawn promotion options
    screen.fill(BACKGROUND)
    options_text = font.render("Choose a piece for pawn promotion:", True, BLACK)
    screen.blit(options_text, (PAWN_BUTTON_X//2, PAWN_BUTTON_Y//2))

    draw_promotion_buttons()  # Draw the piece images

    # Wait for player input
    selected_piece = None
    while selected_piece is None:
        selected_piece = handle_promotion()

    # Perform the move with the selected piece
    move = move + selected_piece
    board.push(chess.Move.from_uci(move))

    return move

def play_game():
    global screen, font, player1, player2, player1_moves, player2_moves, board, players, current_player, previous_move, check, time_stockfish

    pygame.init() # Initialize Pygame

    # Create the Pygame window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AI Chess")

    # Pygame font setup
    pygame.font.init()
    font = pygame.font.SysFont(None, 28)

    player1, player2 = get_name()

    player1_moves = []  # Store Player 1's moves separately
    player2_moves = []  # Spore Player 2's moves separately
    current_player = 0
    players = [player1, player2]
    board = chess.Board()

    while not board.is_game_over():
        game(board)

        if players[current_player].lower() == "random":
            moves = []
            for value in board.legal_moves:
                moves.append(value.uci())
            move = random.choice(moves)
            time.sleep(0.5)

        elif players[current_player].lower() in ["ai", "bot", "stockfish"]:
            attempt = 0
            while attempt < time_limit:
                attempt+=1
                try:
                    with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
                        engine.configure({"Skill Level": skill_level, "Depth": depth})
                        play_result = engine.play(board, chess.engine.Limit(time=time_stockfish))

                        # Extracting values
                        move = play_result.move.uci()
                        # ponder = play_result.ponder.uci()
                        # info = play_result.info
                        # draw_offered = play_result.draw_offered
                        # resigned = play_result.resigned
                        ic(move)
                        break

                except TimeoutError:
                    ic()
                    time_stockfish += 1
            time.sleep(0.5)

        else:
            move = handle_events()
            if move is not None:
                ic(move)

        try:
            if move is not None:
                move_c = chess.Move.from_uci(move)
                if move_c in board.legal_moves:
                    if board.is_castling(move_c):  # Check for castling
                        perform_castling(board, move_c)

                    else:
                        board.push(move_c)  # For normal moves
                    previous_move = move_c
                    current_player = store_moves(player1_moves, player2_moves, current_player, move_c)
                    
                else:
                    move_q = chess.Move.from_uci(move + "q")
                    if move_q in board.legal_moves:
                        move = pawn_promotion(board, move)
                        previous_move = move_q
                        current_player = store_moves(player1_moves, player2_moves, current_player, move)

                if board.is_checkmate():
                    print(f"\033[91mCheckmate!\033[0m {players[current_player]} wins.")
                    break
                elif board.is_stalemate():
                    print("Stalemate! The game is a draw.")
                    break
                elif board.is_insufficient_material():
                    print("Insufficient material! The game is a draw.")
                    break
                elif board.is_check():
                    check = True
                elif not board.is_check():
                    check = False

        except ValueError:
            ic()

    pygame.quit()

    print_result(player1_moves, player2_moves, player1, player2)
    save_to_file(player1_moves, player2_moves, player1, player2)

    print("\033[93mGame over.\033[0m")
    print("\033[95mResult: " + board.result() + "\033[0m")  # Enhanced game over message

    play_again = input("Do you want to play again? Reply with 'Y' for yes: ")
    if play_again.lower() in ["yes", "y"]:
        play_game()

if __name__ == "__main__":
    play_game()
