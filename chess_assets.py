import pygame
from constants import *

#import images
pawn_w = pygame.image.load("pieces/pawn_w.png")
knight_w = pygame.image.load("pieces/knight_w.png")
bishop_w = pygame.image.load("pieces/bishop_w.png")
rook_w = pygame.image.load("pieces/rook_w.png")
queen_w = pygame.image.load("pieces/queen_w.png")
king_w = pygame.image.load("pieces/king_w.png")
pawn_b = pygame.image.load("pieces/pawn_b.png")
knight_b = pygame.image.load("pieces/knight_b.png")
bishop_b = pygame.image.load("pieces/bishop_b.png")
rook_b = pygame.image.load("pieces/rook_b.png")
queen_b = pygame.image.load("pieces/queen_b.png")
king_b = pygame.image.load("pieces/king_b.png")

PIECE_IMAGE = {
    "pawn_w": pawn_w,
    "rook_w": rook_w,
    "knight_w": knight_w,
    "bishop_w": bishop_w,
    "queen_w": queen_w,
    "king_w": king_w,

    "pawn_b": pawn_b,
    "rook_b": rook_b,
    "knight_b": knight_b,
    "bishop_b": bishop_b,
    "queen_b": queen_b,
    "king_b": king_b,
}

PAWN_PROMOTION_IMAGE = {}

# Pieces to be scaled for pawn promotion
pieces = ["rook", "knight", "bishop", "queen"]
colors = ["w", "b"]

# Scaling the images and populating PAWN_PROMOTION_IMAGE dictionary
for piece in pieces:
    for color in colors:
        scaled_image = pygame.transform.scale(
            PIECE_IMAGE[f"{piece}_{color}"], 
            (PAWN_BUTTON_WIDTH - PAWN_IMAGE_MARGIN, PAWN_BUTTON_HEIGHT - PAWN_IMAGE_MARGIN)
        )
        PAWN_PROMOTION_IMAGE[f"{piece}_{color}"] = scaled_image

PIECE_VALUE = {
    ".": "NA",
    "P": "pawn_w",
    "R": "rook_w",
    "N": "knight_w",
    "B": "bishop_w",
    "Q": "queen_w",
    "K": "king_w",
    "p": "pawn_b",
    "r": "rook_b",
    "n": "knight_b",
    "b": "bishop_b",
    "q": "queen_b",
    "k": "king_b",
}