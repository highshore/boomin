import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# ---------- Game Settings ----------
WIDTH = 600
HEIGHT = 400
FPS = 60

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE  = (50, 150, 255)
RED   = (255, 80, 80)
GRAY  = (200, 200, 200)

# Player settings
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 15
PLAYER_SPEED = 7

# Falling block settings
BLOCK_SIZE = 20
BLOCK_SPEED_MIN = 3
BLOCK_SPEED_MAX = 6

# Game limits
MAX_MISSES = 5

# ---------- Setup Window ----------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Blocks!")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 64)


# ---------- Game Objects ----------
class Player:
    def __init__(self):
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 10
        self.speed = PLAYER_SPEED

    def move(self, dx):
        self.x += dx * self.speed
        # Keep inside screen
        if self.x < 0:
            self.x = 0
        if self.x + self.width > WIDTH:
            self.x = WIDTH - self.width

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Block:
    def __init__(self):
        self.size = BLOCK_SIZE
        self.reset()

    def reset(self):
        self.x = random.randint(0, WIDTH - self.size)
        self.y = -self.size
        self.speed = random.randint(BLOCK_SPEED_MIN, BLOCK_SPEED_MAX)

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.x, self.y, self.size, self.size))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)


# ---------- Helper Functions ----------
def draw_text(text, font, color, surface, x, y):
    img = font.render(text, True, color)
    surface.blit(img, (x, y))


def main_game():
    player = Player()
    blocks = [Block() for _ in range(3)]  # Three falling blocks

    score = 0
    misses = 0
    running = True

    while running:
        clock.tick(FPS)

        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- Player input ---
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        player.move(dx)

        # --- Update blocks ---
        player_rect = player.get_rect()
        for block in blocks:
            block.update()

            # Check if block caught by player
            if block.get_rect().colliderect(player_rect):
                score += 1
                block.reset()

            # If block falls past the bottom
            if block.y > HEIGHT:
                misses += 1
                block.reset()

        # --- Check game over ---
        if misses >= MAX_MISSES:
            game_over_screen(score)
            # After game_over_screen returns, restart game
            return

        # --- Drawing ---
        screen.fill(WHITE)

        # Draw player & blocks
        player.draw(screen)
        for block in blocks:
            block.draw(screen)

        # Draw HUD (score & misses)
        draw_text(f"Score: {score}", font, BLACK, screen, 10, 10)
        draw_text(f"Misses: {misses}/{MAX_MISSES}", font, BLACK, screen, 10, 40)

        pygame.display.flip()


def game_over_screen(score):
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Press any key to play again
            if event.type == pygame.KEYDOWN:
                waiting = False

        screen.fill(GRAY)
        draw_text("GAME OVER", big_font, BLACK, screen, WIDTH // 2 - 150, HEIGHT // 2 - 80)
        draw_text(f"Final Score: {score}", font, BLACK, screen, WIDTH // 2 - 80, HEIGHT // 2)
        draw_text("Press any key to play again", font, BLACK, screen, WIDTH // 2 - 150, HEIGHT // 2 + 40)

        pygame.display.flip()


# ---------- Main Loop ----------
if __name__ == "__main__":
    while True:
        main_game()
