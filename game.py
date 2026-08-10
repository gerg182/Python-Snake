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

Segment_gap = 11

Lost = False

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
        self.dir_x = 0
        self.dir_y = 0

        self.segments = []
        self.history = deque(maxlen=(Segment_gap *200))
        self.get_all_grid_center_points()

    def get_all_grid_center_points(self):
        self.points_y = []
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                y = row * CELL_SIZE + CELL_SIZE // 2
                self.points_y.append((y))
        
        self.points_x = []
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                x = col * CELL_SIZE + CELL_SIZE // 2
                self.points_x.append((x))
    
    def handle_key(self, keys):
        if keys == pygame.K_w and self.dir_y == 0:
            self.dir_x, self.dir_y = 0,-1
            bestsofar = float('inf')
            best_point = None
            for point in self.points_x:
                distance = abs(point - self.pos_x)
                if distance < bestsofar:
                    bestsofar = distance
                    best_point = point
                else:
                    pass
            self.pos_x = best_point
        elif keys == pygame.K_s and self.dir_y == 0:
            self.dir_x, self.dir_y = 0,1
            bestsofar = float('inf')
            best_point = None
            for point in self.points_x:
                distance = abs(point - self.pos_x)
                if distance < bestsofar:
                    bestsofar = distance
                    best_point = point
                else:
                    pass
            self.pos_x = best_point
        elif keys == pygame.K_a and self.dir_x == 0:
            self.dir_x, self.dir_y = -1,0
            bestsofar = float('inf')
            best_point = None
            for point in self.points_y:
                distance = abs(point - self.pos_y)
                if distance < bestsofar:
                    bestsofar = distance
                    best_point = point
                else:
                    pass
            self.pos_y = best_point
        elif keys == pygame.K_d and self.dir_x == 0:
            self.dir_x, self.dir_y = 1,0
            bestsofar = float('inf')
            best_point = None
            for point in self.points_y:
                distance = abs(point - self.pos_y)
                if distance < bestsofar:
                    bestsofar = distance
                    best_point = point
                else:
                    pass
            self.pos_y = best_point
        
    def move(self):
        self.loseing()
        player_rect = pygame.Rect(self.pos_x - self.radius, self.pos_y - self.radius, self.radius * 2, self.radius * 2)
        screen_rect = pygame.Rect(-48, -48, GRID_WIDTH * CELL_SIZE + 96, GRID_HEIGHT * CELL_SIZE + 96)
        if not screen_rect.contains(player_rect):
            global Lost
            Lost = True

        self.pos_x += self.dir_x * self.speed
        self.pos_y += self.dir_y * self.speed

        self.history.appendleft((self.pos_x, self.pos_y))

        for i in range(len(self.segments)):
            hist_index = (i +1) * Segment_gap
            if hist_index < len(self.history):
                self.segments[i] = self.history[hist_index]
            elif self.segments:
                pass

    def loseing(self):
            global Lost
            for seg_x, seg_y in self.segments[1:-1]:
                dx = self.pos_x - seg_x
                dy = self.pos_y - seg_y
                distance = (dx ** 2 + dy ** 2) ** 0.5
                if distance < self.radius + self.radius:
                    Lost = True

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
        self.pos_x = random.randrange(GRID_WIDTH) * CELL_SIZE + CELL_SIZE // 2
        self.pos_y = random.randrange(GRID_HEIGHT) * CELL_SIZE + CELL_SIZE // 2

    def respawn(self, occupied):
        while True:
            self.pos_x = random.randrange(GRID_WIDTH) * CELL_SIZE + CELL_SIZE // 2
            self.pos_y = random.randrange(GRID_HEIGHT) * CELL_SIZE + CELL_SIZE // 2
            if (self.pos_x, self.pos_y) not in occupied:
                break
        
    def draw(self, screen):
        self.pos_xgrow = self.pos_x
        self.pos_ygrow = self.pos_y
        pygame.draw.circle(screen, self.color, (self.pos_xgrow, self.pos_ygrow), self.radius)

Piece_draw = Piece(408, 360, 20,(0, 200, 255))
Apple_spawn = Apple(20,(255, 0, 0))

def new_game():
    global Lost, player_score, Piece_draw, Apple_spawn
    Piece_draw = Piece(408, 360, 23, (0, 200, 255))
    Apple_spawn = Apple(20,(255, 0, 0))
    player_score = 0
    Lost = False
    pygame.display.set_caption(f"Snake Game - Score: 0")

runing = True
while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
        if event.type == pygame.KEYDOWN and Lost != True:
            Piece_draw.handle_key(event.key)


    keys = pygame.key.get_pressed()

    if Lost != True:
        Piece_draw.move()

    screen.fill((30,30,30))

    draw_grid(screen)
    Piece_draw.draw(screen)
    Apple_spawn.draw(screen)
    dx = Piece_draw.pos_x - Apple_spawn.pos_x
    dy = Piece_draw.pos_y - Apple_spawn.pos_y
    distance = (dx ** 2 + dy ** 2) ** 0.5
    if distance < Piece_draw.radius + Apple_spawn.radius:
        occupied = [(Piece_draw.pos_x, Piece_draw.pos_y)] + Piece_draw.segments
        Apple_spawn.respawn(occupied)
        Piece_draw.grow()
        player_score += 1
        pygame.display.set_caption(f"Snake Game - Score: {player_score}")

    if Lost == True:
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(180)
        overlay.fill((30, 30, 30))
        screen.blit(overlay, (0, 0))
        if keys[pygame.K_r]:
            new_game()

        font = pygame.font.Font(None, 74)
        text_surface = font.render(f"Game Over - Score:{player_score}\nPress R to restart", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text_surface, text_rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()