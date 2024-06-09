import sys
import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]   # Z
]

# Shape colors
SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Clock
clock = pygame.time.Clock()
FPS = 10

# Font
font = pygame.font.SysFont('comicsans', 30)

class Shape:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = SHAPE_COLORS[SHAPES.index(self.shape)]
        self.x = SCREEN_WIDTH // 2 // BLOCK_SIZE * BLOCK_SIZE
        self.y = 0
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)
        self.shape = self.shape[self.rotation:]

    def get_shape(self):
        return self.shape

class Tetris:
    def __init__(self):
        self.board = [[BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
        self.current_piece = Shape()
        self.next_piece = Shape()
        self.score = 0

    def draw_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                pygame.draw.rect(screen, self.board[i][j], (j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        for i in range(len(self.current_piece.shape)):
            for j in range(len(self.current_piece.shape[i])):
                if self.current_piece.shape[i][j] == 1:
                    pygame.draw.rect(screen, self.current_piece.color, (self.current_piece.x + j*BLOCK_SIZE, self.current_piece.y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    def move(self, dx, dy):
        self.current_piece.x += dx * BLOCK_SIZE
        self.current_piece.y += dy * BLOCK_SIZE

    def drop_piece(self):
        while not self.collision():
            self.current_piece.y += BLOCK_SIZE
        self.current_piece.y -= BLOCK_SIZE
        self.lock_piece()

    def collision(self):
        for i in range(len(self.current_piece.shape)):
            for j in range(len(self.current_piece.shape[i])):
                if self.current_piece.shape[i][j] == 1:
                    if self.current_piece.y + i*BLOCK_SIZE >= SCREEN_HEIGHT:
                        return True
                    if self.current_piece.x + j*BLOCK_SIZE < 0 or self.current_piece.x + j*BLOCK_SIZE >= SCREEN_WIDTH:
                        return True
                    if self.board[(self.current_piece.y // BLOCK_SIZE) + i][(self.current_piece.x // BLOCK_SIZE) + j] != BLACK:
                        return True
        return False

    def lock_piece(self):
        for i in range(len(self.current_piece.shape)):
            for j in range(len(self.current_piece.shape[i])):
                if self.current_piece.shape[i][j] == 1:
                    self.board[(self.current_piece.y // BLOCK_SIZE) + i][(self.current_piece.x // BLOCK_SIZE) + j] = self.current_piece.color
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = Shape()
        if self.collision():
            self.game_over()

    def clear_lines(self):
        lines_to_clear = []
        for i in range(len(self.board)):
            if BLACK not in self.board[i]:
                lines_to_clear.append(i)
        for i in lines_to_clear:
            del self.board[i]
            self.board.insert(0, [BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)])
            self.score += 10

    def game_over(self):
        pygame.quit()
        sys.exit()

    def draw_score(self):
        score_text = font.render("Score: " + str(self.score), 1, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))

def main():
    tetris = Tetris()
    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetris.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    tetris.move(1, 0)
                if event.key == pygame.K_DOWN:
                    tetris.move(0, 1)
                if event.key == pygame.K_UP:
                    tetris.current_piece.rotate()
                if event.key == pygame.K_SPACE:
                    tetris.drop_piece()
        
        tetris.move(0, 1)
        if tetris.collision():
            tetris.move(0, -1)
            tetris.lock_piece()

        tetris.draw_board()
        tetris.draw_score()
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
