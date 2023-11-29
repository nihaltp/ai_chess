import sys
import pygame

# Initialize Pygame
pygame.init()

# Constants
width, height = 600, 500
square_width = 400
rows, columns = 8, 8
square_size = square_width // columns

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Create the Pygame window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("AI Chess")

# Where to start the chess board
chess_x = 100
chess_y = 50

# Draw the chessboard# Create a 2D list to represent the chessboard with values
chessboard = [[0] * columns for _ in range(rows)]

chessboard_rows = [8,7,6,5,4,3,2,1]
chessboard_columns = ["a","b","c","d","e","f","g","h"]

# Assign unique values to each square
for row in range(rows):
    for column in range(columns):
        chessboard[row][column] = chessboard_rows[row], chessboard_columns[column]

# Draw chessboard
def draw_chessboard(rows, columns):
    # Draw each square independently
    for row in range(rows):
        for column in range(columns):
            color = white if (row + column) % 2 == 0 else black
            square_rect = pygame.Rect(chess_x + column * square_size, chess_y + row * square_size, square_size, square_size)
            pygame.draw.rect(screen, color, square_rect)

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
    # Get the mouse coordinates
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Determine the clicked square
    clicked_column = (mouse_x - chess_x) // square_size
    clicked_row = (mouse_y - chess_y) // square_size

    # Check if the click is within the chessboard boundaries
    if 0 <= clicked_row < rows and 0 <= clicked_column < columns:
        clicked_square_value = chessboard[clicked_row][clicked_column]
        print(f"Mouse clicked at Square : {clicked_square_value}")
    else:
        print(f"Mouse clicked at ({mouse_x}, {mouse_y})")

while True:
    draw_chessboard(rows, columns)
    handle_events()

    # Update the display
    pygame.display.flip()