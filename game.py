import pygame
import random
from collections import deque

pygame.init()

CELL_SIZE = 48
GRID_WIDTH = 17
GRID_HEIGHT = 15
player_score = 0

screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
pygame.display.set_caption(f"Snake Game - Score: 0")

clock = pygame.time.Clock()

Segment_gap = 8

def draw_grid(screen):
    color_a = (162, 209, 73)   # light green
    color_b = (170, 215, 81)   # slighty different green
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            color = color_a if (row +col) % 2 == 0 else color_b
            pygame.draw.rect(screen, color, (x,y, CELL_SIZE, CELL_SIZE))

class Piece:
    def __init__(self, pos_x, pos_y, radius, color, speed=5):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.color = color
        self.speed = speed

        self.segments = []
        self.history = deque(maxlen=(Segment_gap *200))

    
    def move(self, keys):
        if keys[pygame.K_w]:
            self.pos_y -= self.speed
        if keys[pygame.K_s]:
            self.pos_y += self.speed
        if keys[pygame.K_a]:
            self.pos_x -= self.speed
        if keys[pygame.K_d]:
            self.pos_x += self.speed

        self.history.appendleft((self.pos_x, self.pos_y))

        for i in range(len(self.segments)):
            hist_index = (i +1) * 8
            if hist_index < len(self.history):
                self.segments[i] = self.history[hist_index]
            elif self.segments:
                pass

    def grow(self):
        if self.segments:
            self.segments.append(self.segments[-1])
        else:
            self.segments.append((self.pos_x, self.pos_y))
        
    def draw(self, screen):
        for seg_x, seg_y in self.segments:
            pygame.draw.circle(screen, self.color, (seg_x, seg_y), self.radius)
        pygame.draw.circle(screen, self.color, (self.pos_x, self.pos_y), self.radius)
        

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
        self.pos_xgrow = self.pos_x + 24
        self.pos_ygrow = self.pos_y + 24
        pygame.draw.circle(screen, self.color, (self.pos_xgrow, self.pos_ygrow), self.radius)

Piece_draw = Piece(320, 240, 25,(0, 200, 255))
Apple_spawn = Apple(25,(255, 0, 0))

runing = True
while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False

    keys = pygame.key.get_pressed()
    Piece_draw.move(keys)

    screen.fill((30,30,30))

    draw_grid(screen)
    Piece_draw.draw(screen)
    Apple_spawn.draw(screen)
    dx = Piece_draw.pos_x - Apple_spawn.pos_x
    dy = Piece_draw.pos_y - Apple_spawn.pos_y
    distance = (dx ** 2 + dy ** 2) ** 0.5
    if distance < Piece_draw.radius + Apple_spawn.radius:
        Apple_spawn.respawn()
        Piece_draw.grow()
        player_score += 1
        pygame.display.set_caption(f"Snake Game - Score: {player_score}")
    pygame.display.flip()
    clock.tick(60)

pygame.quit()