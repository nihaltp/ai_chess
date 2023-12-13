import sys
import pygame
from config import *

# Initialize Pygame
pygame.init()

# Create the Pygame window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("AI Chess")

# Pygame font setup
pygame.font.init()
font = pygame.font.SysFont(None, 30)

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
        print(f"Mouse clicked at Square : {clicked_square_value}")
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

while __name__ == "__main__":
    game()
