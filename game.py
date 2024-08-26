import os

# Hide the Pygame support prompt
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import sys
import time
import chess
import chess.engine
import random
import pygame

from constants import *
from variables import *
from chess_assets import *

from icecream import ic

class ChessGame:
    def __init__(self):
        try:
            pygame.init() # Initialize Pygame
        except pygame.error as e:
            print(f"Error initializing Pygame: {e}")
            print("Please install pygame and try again.")
            sys.exit(1)

        # Create the Pygame window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("AI Chess")
        # Pygame font setup
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 28)

        self.get_name()
        self.player1_moves = []
        self.player2_moves = []
        self.current_player = 0
        self.players = [self.player1, self.player2]
        self.board = chess.Board()

        self.move = ""
        self.previous_move = ""
        self.check = False
        self.highlight = False

        self.stockfish_path = stockfish_path
        self.skill_level = skill_level
        self.depth = depth
        self.time_stockfish = time_stockfish
        self.time_limit = time_limit
        self.engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)

        self.mouse_x = 0
        self.mouse_y = 0

        self.directory = directory

    def play_game(self):
        while not self.board.is_game_over():
            self.game(self.board)
            self.handle_move()
            if not self.process_move():
                break
        self.end_game()

    def handle_move(self):
        if self.players[self.current_player].lower() == "random":
            self.get_random_move()
            pygame.time.delay(500)
        elif self.players[self.current_player].lower() in ["ai", "bot", "stockfish"]:
            self.get_ai_move()
            pygame.time.delay(500)
        else:
            self.handle_events()

    def get_random_move(self):
        moves = [move.uci() for move in self.board.legal_moves]
        self.move = random.choice(moves)

    def get_ai_move(self):
        attempt = 0
        while attempt < self.time_limit:
            attempt += 1
            try:
                self.engine.configure({"Skill Level": self.skill_level, "Depth": self.depth})
                play_result = self.engine.play(self.board, chess.engine.Limit(time=self.time_stockfish))
                # Extracting values
                self.move = play_result.move.uci()
                """
                TODO: show ponder as part of the hint
                TODO: use stockfish for hint
                ponder = play_result.ponder.uci()
                info = play_result.info
                """
                if play_result.draw_offered:
                    name_text = self.players[1-self.current_player]
                    if self.draw(name_text, draw_accept_text):
                        self.history()
                        self.save_to_file()
                        pygame.quit()
                        sys.exit(0)
                if play_result.resigned:
                    self.history()
                    self.save_to_file()
                    pygame.quit()
                    sys.exit(0)
                break
            except chess.engine.EngineError as e:
                print(f"Error initializing Stockfish engine: {e}")
                pygame.quit()
                sys.exit(1)
            except TimeoutError:
                self.time_stockfish += 1
            finally:
                self.engine.quit()

    def process_move(self):
        if not len(self.move) == 4:
            return True
        if self.move:
            try:
                move_c = chess.Move.from_uci(self.move)
                if move_c in self.board.legal_moves:
                    if self.board.is_castling(move_c):
                        self.perform_castling()
                    else:
                        self.board.push(move_c)
                    self.previous_move = move_c
                else:
                    move_q = chess.Move.from_uci(self.move + "q")
                    if move_q in self.board.legal_moves:
                        self.pawn_promotion()
                        self.previous_move = move_q
                
                self.store_moves()
                self.check = self.board.is_check()
                if not self.check_game_status():
                    return False
            except ValueError as e:
                print(f"Invalid move: {e}")
        return True

    def check_game_status(self):
        if self.board.is_checkmate():
            print(f"\033[91mCheckmate!\033[0m {self.players[self.current_player]} wins.")
            return False
        if self.board.is_stalemate():
            print("Stalemate! The game is a draw.")
            return False
        if self.board.is_insufficient_material():
            print("Insufficient material! The game is a draw.")
            return False
        return True

    def end_game(self):
        self.history()
        self.save_to_file()
        print("\033[93mGame over.\033[0m")
        print(f"\033[95mResult: {self.board.result()}\033[0m")
        play_again = self.input_text("Do you want to play again? (Y/N): ", (200, 100))
        if play_again.lower() in ["yes", "y"]:
            self.__init__()
            self.play_game()
        else:
            pygame.quit()
            sys.exit()

    def get_name(self):
        # Get Player names
        self.player1 = self.input_text("Enter Player 1's name: ", (200, 100))
        self.player2 = self.input_text("Enter Player 2's name: ", (200, 100))

    def input_text(self, prompt, position):
        input_active = True
        input_text = []

        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.unicode == "\r" and input_text:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif len(input_text) < 20:  # Limit the length of the name
                        input_text.append(event.unicode)
            
            self.screen.fill(BACKGROUND)
            
            # Display the input text
            current_text = ''.join(input_text)
            value = f"{prompt} {current_text}"
            text = self.font.render(value, True, BLACK)
            text_rect = text.get_rect(topleft = position)
            self.screen.blit(text, text_rect)
            pygame.display.flip()

        return current_text

    def game(self, board):
        """
        Main game loop method to update and draw the chessboard.
        """
        self.update(board)
        self.draw_chessboard(ROWS, COLUMNS)
        pygame.display.flip() # update the display

    def update(self, board):
        board_value = str(board).replace(" ", "").replace("\n", "")
        for i, j in zip(board_value, SQUARES):
            # Get the piece image from the dictionary
            chessboard[j] = PIECE_VALUE.get(i)

    def draw_chessboard(self, ROWS, COLUMNS):
        """
        Draw the chessboard on the screen.

        Parameters:
        rows (int): Number of rows on the chessboard.
        columns (int): Number of columns on the chessboard.
        """
        self.screen.fill(BACKGROUND)
        square_rect = pygame.Rect(CHESS_X - 2, CHESS_Y - 2, SQUARE_WIDTH + 4, SQUARE_WIDTH + 4)
        pygame.draw.rect(self.screen, BOARD_BORDER, square_rect, width = 2 )

        # Draw each square independently
        for row in range(ROWS):
            for column in range(COLUMNS):
                self.draw_square(row, column)

        self.draw_rows()
        self.draw_columns()
        self.draw_buttons()

    def draw_square(self, row, column):
        color = WHITE if (row + column) % 2 == 0 else GREY
        square_rect = pygame.Rect(CHESS_X + column * SQUARE_SIZE, CHESS_Y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(self.screen, color, square_rect)

        # Check chessboard configuration and blit the corresponding image
        value = row * 8 + column
        piece_key = SQUARES[value]
        piece = chessboard[piece_key]
        self.draw_piece(piece, square_rect)

    def draw_piece(self, piece, square_rect):
        """
        Function to draw pieces on the board
        """
        # Get the piece image from the dictionary
        piece_img = PIECE_IMAGE.get(piece)

        if piece_img is not None:
            # Blit the piece image
            self.screen.blit(piece_img, square_rect.topleft)

        if self.highlight:
            # Determine the clicked square
            clicked_column = (self.mouse_x - CHESS_X) // SQUARE_SIZE
            clicked_row = (self.mouse_y - CHESS_Y) // SQUARE_SIZE
            if self.move and len(self.move) == 2:
                self.highlight_square(clicked_column, clicked_row, RED)
            elif self.move:
                self.highlight_square(clicked_column, clicked_row, GOLD)

        if self.previous_move != "":
            value = self.previous_move.uci()
            move_2 = value[2:]
            self.highlight_move(move_2, BLUE_1)

        if self.check:
            for i in chessboard:
                if chessboard[i] == "king_w" and self.current_player == 0 or chessboard[i] == "king_b" and self.current_player == 1:
                    self.highlight_move(i, RED)
                    break

    def highlight_square(self, value1, value2, colour):
        """
        Highlights a square on the chessboard.
        
        Parameters:
        value1 (int): The x-coordinate of the square.
        value2 (int): The y-coordinate of the square.
        colour (tuple): The color to highlight the square with.
        """
        x = CHESS_X + (value1 * SQUARE_SIZE)
        y = CHESS_Y + (value2 * SQUARE_SIZE)

        square_rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(self.screen, colour, square_rect, width = 2 )

    def highlight_move(self, square, colour):
        """
        TODO: Make sure it is highlighting things inside the board only
        TODO: Make a function to highlight buttons when clicked
        TODO: Make a function to highlight square/button the mouse is over
        """
        if len(square) != 2:
            square = square[:2]
        value = SQUARES.index(square)
        row, column = divmod(value, 8)
        self.highlight_square(column, row, colour)

    def draw_rows(self):
        """
        Draws the chessboard rows.
        """
        self.draw_labels(RANK_NAMES, CHESS_X - 30, CHESS_Y, is_column=False)  # Left
        self.draw_labels(RANK_NAMES, CHESS_X + 430, CHESS_Y, is_column=False)  # Right

    def draw_columns(self):
        """
        Draws the chessboard columns.
        """
        self.draw_labels(FILE_NAMES, CHESS_X, CHESS_Y - 30, is_column=True)  # Top
        self.draw_labels(FILE_NAMES, CHESS_X, CHESS_Y + 430, is_column=True)  # Bottom

    def draw_labels(self, labels, x_offset, y_offset, is_column=False):
        """
        Draws labels for either rows or columns on the chessboard.

        Parameters:
        labels (list): List of labels (row or column names).
        x_offset (int): The horizontal offset for text placement.
        y_offset (int): The vertical offset for text placement.
        is_column (bool): Whether the labels are for columns (True) or rows (False).
        """
        for i, label in enumerate(labels):
            if is_column:
                x = CHESS_X + i * SQUARE_SIZE + SQUARE_SIZE // 2
                y = y_offset
            else:
                x = x_offset
                y = CHESS_Y + i * SQUARE_SIZE + SQUARE_SIZE // 2

            self.draw_text_at_location(label, x, y)

    def draw_text_at_location(self, text, x, y):
        text = self.font.render(str(text), True, TEXT_COLOR)
        text_rect = text.get_rect(center=(x, y))
        self.screen.blit(text, text_rect)

    def draw_buttons(self):
        for button_name in (BUTTONS):
            button_position = BUTTON_POSITIONS[button_name]

            button = pygame.Rect(button_position, (BUTTON_WIDTH, BUTTON_HEIGHT))
            pygame.draw.rect(self.screen, BUTTON_COLOR, button)

            font_buttons = pygame.font.SysFont(None, 24)
            text = font_buttons.render(button_name, True, TEXT_COLOR)

            text_rect = text.get_rect(center=(button_position[0] + BUTTON_MARGIN_X, button_position[1] + BUTTON_MARGIN_Y))
            self.screen.blit(text, text_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click()

    def handle_mouse_click(self):
        # Get the mouse coordinates
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        # Determine the clicked square
        clicked_column = (self.mouse_x - CHESS_X) // SQUARE_SIZE
        clicked_row = (self.mouse_y - CHESS_Y) // SQUARE_SIZE
        self.handle_square_click(clicked_column, clicked_row)

    def handle_square_click(self, column, row):
        # Check if the click is within the chessboard boundaries
        if 0 <= row < ROWS and 0 <= column < COLUMNS:
            value = int(row*8 + column)
            clicked_square = SQUARES[value]
            self.handle_valid_click(clicked_square)
            if self.move[:2] == self.move[2:]:
                self.move = self.move[:2]
            self.highlight = True
        else:
            self.handle_buttons()
            self.highlight = False
            self.move = ""

    def handle_valid_click(self, square):
        if self.move is None:
            self.move = square
        elif len(self.move) == 2:
            self.move += square
        else:
            self.move = square

    def handle_buttons(self):
        for button_name, pos in BUTTON_POSITIONS.items():
            if pos[0] <= self.mouse_x <= pos[0] + BUTTON_WIDTH and pos[1] <= self.mouse_y <= pos[1] + BUTTON_HEIGHT:
                self.button_action(button_name)

    def button_action(self, button_name):
        if button_name == "History":
            self.history()
        if button_name == "Hint":
            self.valid_moves()
        if button_name == "Undo":
            self.undo()
        if button_name == "Draw":
            if self.is_draw():
                self.history()
                self.save_to_file()
                pygame.quit()
                sys.exit(0)
        if button_name == "Stop":
            pygame.quit()
            sys.exit()

    def history(self):
        """
        Display the game history by iterating through the player moves and updating the chess board.

        This function creates a new chess board called `board_history` and initializes it with the current game state.
        It then calls the `game` method to update the display.

        The function then calculates the maximum number of moves between the two players
        and iterates through the moves using a for loop.
        """
        board_history = chess.Board()
        self.game(board_history)
        pygame.time.delay(500) # pause for 0.5 seconds
        max_moves = max(len(self.player1_moves), len(self.player2_moves))
        for i in range(max_moves):
            if i < len(self.player1_moves):
                move = self.player1_moves[i]
                self.replay_game(move, board_history)
            if i < len(self.player2_moves):
                move = self.player2_moves[i]
                self.replay_game(move, board_history)

    def replay_game(self, move, board):
        move = chess.Move.from_uci(move)
        if board.is_legal(move):
            board.push(move)
            self.game(board)
            pygame.time.delay(500)  # pause for 0.5 second

    def valid_moves(self):
        for move in self.board.legal_moves:
            self.draw_chessboard(ROWS, COLUMNS) # clear the chessboard
            start_square = move.uci()[:2] 
            end_square = move.uci()[2:]
            self.highlight_move(start_square, RED)
            self.highlight_move(end_square, GOLD)
            pygame.display.flip()
            pygame.time.delay(500) # wait

    def undo(self):
        if len(self.player1_moves) >= 1 and len(self.player2_moves) >= 1:
            if len(self.player1_moves) >= 1:
                self.board.pop()  # Undo last move on the board
                last_move_player1 = self.player1_moves.pop()  # Remove Player 1's last move
            else:
                last_move_player1 = None
                    
            if len(self.player2_moves) >= 1:
                last_move_player2 = self.player2_moves.pop()  # Remove Player 2's last move
                self.board.pop()  # Undo last move on the board
            else:
                last_move_player2 = None
            
            # TODO: Draw the text on pygame window
            if last_move_player1 is not None:
                print(f"{self.players[0]} undid their last move: {last_move_player1}")
            if last_move_player2 is not None:
                print(f"{self.players[1]} undid their last move: {last_move_player2}")

        else:
            # TODO: Show it in pygame window
            print("No moves to undo.")

    def is_draw(self):
        if len(self.player1_moves) < 2 and len(self.player2_moves) < 2:
            # TODO: Create a window for this message
            print("Draw offer rejected. Both players need to have made at least two moves.")
            return

        name_text = self.players[self.current_player]
        if not self.draw(name_text, draw_offer_text):
            return False
        
        name_text = self.players[1-self.current_player]
        if not self.draw(name_text, draw_accept_text):
            return False
        
        return True

    def draw(self, name_text, draw_text):
        self.screen.fill(BACKGROUND)
        name = self.font.render(name_text, True, BLACK)
        draw_accept = self.font.render(draw_text, True, BLACK)
        yes = self.font.render("Yes", True, BLACK)
        no = self.font.render("No", True, BLACK)

        # TODO: Add variable for dimensions below
        self.screen.blit(name, (BUTTON_WIDTH, PAWN_BUTTON_HEIGHT//2))
        self.screen.blit(draw_accept, (BUTTON_WIDTH, PAWN_BUTTON_HEIGHT))
        self.screen.blit(yes, (BUTTON_WIDTH, PAWN_BUTTON_HEIGHT+60))
        self.screen.blit(no, ((BUTTON_WIDTH*2)+10, PAWN_BUTTON_HEIGHT+60))
        pygame.display.flip()

        selected_option = None
        while selected_option is None:
            selected_option = self.handle_draw(BUTTON_WIDTH-5, BUTTON_WIDTH*2+5, PAWN_BUTTON_HEIGHT+55, 45, 40, 30)
        return selected_option

    def handle_draw(self, x1, x2, y, width1, width2, height):
        start_time = time.time()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x > x1 and mouse_x < x1+width1 and mouse_y > y and mouse_y < y+height:
                        return True
                    if mouse_x > x2 and mouse_x < x2+width2 and mouse_y > y and mouse_y < y+height:
                        return False
            if time.time() - start_time > 60:
                return False

    def save_to_file(self):
        # Ensure the directory exists
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        p1s = str(self.player1)
        p2s = str(self.player2)
        p1r = p1s.replace(" ", "_")
        p2r = p2s.replace(" ", "_")

        # Construct the full file path
        file = os.path.join(self.directory, f"{p1r}_{p2r}.txt")

        try:
            with open(file, 'a') as file:
                file.write(f"Game between {self.player1} and {self.player2}:\n")
                for move1, move2 in zip(self.player1_moves, self.player2_moves):
                    file.write(f"{self.player1}: {move1}, {self.player2}: {move2}\n")
        except IOError as e:
            print(f"Error saving to file: {e}")

    def perform_castling(self):
        if not self.move:
            return
        
        self.board.push(self.move)  # Perform castling
        if self.move == "e1g1":  # King-side castling for white
            self.board.push(chess.Move.from_uci("e1g1"))  # Move the King
            self.board.push(chess.Move.from_uci("h1f1"))  # Move the Rook

        elif self.move == "e1c1":  # Queen-side castling for white
            self.board.push(chess.Move.from_uci("e1c1"))  # Move the King
            self.board.push(chess.Move.from_uci("a1d1"))  # Move the Rook

        elif self.move == "e8g8":  # King-side castling for black
            self.board.push(chess.Move.from_uci("e8g8"))  # Move the King
            self.board.push(chess.Move.from_uci("h8f8"))  # Move the Rook

        elif self.move == "e8c8":  # Queen-side castling for black
            self.board.push(chess.Move.from_uci("e8c8"))  # Move the King
            self.board.push(chess.Move.from_uci("a8d8"))  # Move the Rook

    def store_moves(self):
        if self.current_player == 0:
            self.player1_moves.append(self.move)  # Store Player 1's move
        else:
            self.player2_moves.append(self.move)  # Store Player 2's move

        self.current_player = 1 - self.current_player  # Switch players

    def pawn_promotion(self):
        # Display pawn promotion options
        self.screen.fill(BACKGROUND)
        options_text = self.font.render("Choose a piece for pawn promotion:", True, BLACK)
        self.screen.blit(options_text, (PAWN_BUTTON_X//2, PAWN_BUTTON_Y//2))

        self.draw_promotion_buttons()  # Draw the piece images

        # Wait for player input
        selected_piece = None
        start_time = time.time()
        while selected_piece is None:
            selected_piece = self.handle_promotion()
            if time.time() - start_time > 60:
                selected_piece = "q" # selects queen to stop infinite running

        # Perform the move with the selected piece
        move = self.move + selected_piece
        self.board.push(chess.Move.from_uci(move))

    def draw_promotion_buttons(self):
        for piece_name in (["queen", "rook", "bishop", "knight"]):
            button_position = BUTTON_POSITIONS[piece_name]

            button = pygame.Rect(button_position, (PAWN_BUTTON_WIDTH, PAWN_BUTTON_HEIGHT))
            pygame.draw.rect(self.screen, BUTTON_COLOR, button)

            # Draw the piece image
            color = "_w" if self.current_player == 0 else "_b"
            piece_img = PAWN_PROMOTION_IMAGE.get(piece_name + color)
            self.screen.blit(piece_img, ((button_position[0] + (PAWN_BUTTON_WIDTH/2) - (piece_img.get_width()/2)), (button_position[1] + (PAWN_BUTTON_HEIGHT/2) - (piece_img.get_height()/2))))
        pygame.display.flip()

    def handle_promotion(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, piece_name in enumerate(["queen", "rook", "bishop", "knight"]):
                    button_position = BUTTON_POSITIONS[piece_name]
                    if button_position[0] <= mouse_x <= button_position[0] + PAWN_BUTTON_WIDTH and \
                            button_position[1] <= mouse_y <= button_position[1] + PAWN_BUTTON_HEIGHT:
                        return ["q", "r", "b", "n"][i]  # Return the selected piece
        return None

if __name__ == "__main__":
    game = ChessGame()
    game.play_game()