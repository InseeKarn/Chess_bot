import pygame
import chess

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Chess Bot Viewer")

# Colors and dimensions
square_size = 100
colors = [pygame.Color(235, 236, 208), pygame.Color(119, 149, 86)]

# Load images for chess pieces
pieces = {}
for piece in ['p', 'r', 'n', 'b', 'q', 'k']:
    pieces[f'w{piece}'] = pygame.image.load(f'img/w{piece}.png')
    pieces[f'b{piece}'] = pygame.image.load(f'img/b{piece}.png')

def draw_board(screen, board):
    # Draw squares
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col * square_size, row * square_size, square_size, square_size))

    # Draw pieces
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_image = pieces[f"{piece.color and 'w' or 'b'}{piece.symbol().lower()}"]
            x = (square % 8) * square_size
            y = (7 - square // 8) * square_size  # Flip vertically to match chessboard
            screen.blit(piece_image, (x, y))

    pygame.display.flip()

def run_game(board):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the board and pieces
        draw_board(screen, board)

        pygame.display.flip()  # Update the screen
        pygame.time.delay(100)  # Delay to limit the frame rate

    pygame.quit()
