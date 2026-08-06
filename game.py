import pygame
import random

pygame.init()

CELL_SIZE = 20
GRID_WIDTH = 96
GRID_HEIGHT = 52
player_score = 0

screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption(f"Snake Game - Score: 0")

clock = pygame.time.Clock()

class Piece:
    def __init__(self, pos_x, pos_y, radius, color, speed=5):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.color = color
        self.speed = speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.pos_x, self.pos_y), self.radius)

    def move(self, keys):
        if keys[pygame.K_w]:
            self.pos_y -= self.speed
        if keys[pygame.K_s]:
            self.pos_y += self.speed
        if keys[pygame.K_a]:
            self.pos_x -= self.speed
        if keys[pygame.K_d]:
            self.pos_x += self.speed

class Apple:
    def __init__(self, radius, color):
        self.color = color
        self.radius = radius
        self.pos_x = random.randrange(GRID_WIDTH) * CELL_SIZE
        self.pos_y = random.randrange(GRID_HEIGHT) * CELL_SIZE

    def respawn(self):
        self.pos_x = random.randrange(GRID_WIDTH) * CELL_SIZE
        self.pos_y = random.randrange(GRID_HEIGHT) * CELL_SIZE
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.pos_x, self.pos_y), self.radius)

Piece_draw = Piece(320, 240, 50, (0, 200, 255))
Apple_spawn = Apple(25,(255, 0, 0))

runing = True
while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False

    keys = pygame.key.get_pressed()
    Piece_draw.move(keys)

    screen.fill((30,30,30))
    
    Piece_draw.draw(screen)
    Apple_spawn.draw(screen)
    dx = Piece_draw.pos_x - Apple_spawn.pos_x
    dy = Piece_draw.pos_y - Apple_spawn.pos_y
    distance = (dx ** 2 + dy ** 2) ** 0.5
    if distance < Piece_draw.radius + Apple_spawn.radius:
        Apple_spawn.respawn()
        player_score += 1
        pygame.display.set_caption(f"Snake Game - Score: {player_score}")
    pygame.display.flip()
    clock.tick(60)

pygame.quit()