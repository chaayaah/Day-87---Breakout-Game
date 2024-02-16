import pygame
from pygame.locals import *

pygame.init()

screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout Game', 'XXX')

font = pygame.font.SysFont('Constantia', 30)
text_col = (79, 81, 139)

BACKGROUND_COLOR = (234, 218, 184)
BLOCK_RED = (242, 85, 96)
BLOCK_GREEN = (86, 174, 87)
BLOCK_BLUE = (69, 177, 233)

paddle_color = (142, 135, 123)
paddle_outline = (100, 100, 100)

cols = 6
rows = 6
clock = pygame.time.Clock()
fps = 60
live_ball = False
game_over = 0

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

class Wall:
    def __init__(self):
        self.width = screen_width // cols
        self.height = 50

    def create_wall(self):
        self.blocks = []
        self.block_individual = []
        for row in range(rows):
            block_row = []
            for col in range(cols):
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength = 1
                block_individual = [rect, strength]
                block_row.append(block_individual)
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                if block[1] == 3:
                    block_col = BLOCK_BLUE
                elif block[1] == 2:
                    block_col = BLOCK_GREEN
                elif block[1] == 1:
                    block_col = BLOCK_RED
                pygame.draw.rect(screen, block_col, block[0])
                pygame.draw.rect(screen, BACKGROUND_COLOR, (block[0]),3)

class Paddle:
    def __init__(self):
        self.reset()

    def reset(self):
        self.height = 20
        self.width = int(screen_width / cols)
        self.x = int((screen_width/2)-(self.width/2))
        self.y = screen_height - (self.height * 2)
        self.speed = 10
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0

    def move(self):
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x = self.rect.x - self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x = self.rect.x + self.speed
            self.direction = 1
    def draw(self):
        pygame.draw.rect(screen, paddle_color, self.rect)

class GameBall:
    def __init__(self, x, y):
        self.reset(x, y)

    def reset(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.speed_max = 5
        self.game_over = 0

    def move(self):
        collision_threshold = 5

        wall_destroyed = 1
        row_count = 0
        for row in wall.blocks:
            item_count = 0
            for item in row:
                if self.rect.colliderect(item[0]):
                    if abs(self.rect.bottom - item[0].top) < collision_threshold and self.speed_y > 0:
                        self.speed_y = self.speed_y * -1
                    if abs(self.rect.top - item[0].bottom) < collision_threshold and self.speed_y < 0:
                        self.speed_y = self.speed_y * -1
                    if abs(self.rect.right - item[0].left) < collision_threshold and self.speed_x > 0:
                        self.speed_y = self.speed_y * -1
                    if abs(self.rect.left - item[0].right) < collision_threshold and self.speed_x < 0:
                        self.speed_y = self.speed_y * -1
                    if wall.blocks[row_count][item_count][1] > 1:
                        wall.blocks[row_count][item_count][1] = wall.blocks[row_count][item_count][1] - 1
                    else:
                        wall.blocks[row_count][item_count][0] = (0, 0, 0, 0)
                
                if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
                    wall_destroyed = 0
                item_count = item_count + 1
            row_count = row_count + 1
        if wall_destroyed == 1:
            self.game_over = 1

        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x = self.speed_x * -1
        if self.rect.top < 0:
            self.speed_y = self.speed_y * -1
        if self.rect.bottom > screen_height:
            self.game_over = -1

        if self.rect.colliderect(player_paddle):
            if abs(self.rect.bottom - player_paddle.rect.top) < collision_threshold and self.speed_y > 0:
                self.speed_y = self.speed_y * -1
                self.speed_x = self.speed_x + player_paddle.direction
                if self.speed_x > self.speed_max:
                    self.speed_x = self.peed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                    self.speed_x = -self.speed_max
            else:
                self.speed_x = self.speed_x * -1



        self.rect.x = self.rect.x + self.speed_x
        self.rect.y = self.rect.y + self.speed_y



        return self.game_over

    def draw(self):
        pygame.draw.circle(screen, paddle_color, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad, 3)

wall = Wall()
wall.create_wall()

player_paddle = Paddle()

ball = GameBall(player_paddle.x + (player_paddle.width//2), player_paddle.y - player_paddle.height)


is_running = True
while is_running:
    clock.tick(fps)
    screen.fill(BACKGROUND_COLOR)
    wall.draw_wall()

    player_paddle.draw()
    player_paddle.move()

    if live_ball:
        ball.draw()
        game_over = ball.move()
        if game_over != 0:
            live_ball = False

    if not live_ball:
        if game_over == 0:
            draw_text('CLICK ANYWHERE TO START', font, text_col, 100, screen_height // 2 + 100)
        elif game_over == 1:
            draw_text('YOU WON!', font, text_col, 100, screen_height // 2 + 50)
            draw_text('CLICK ANYWHERE TO START', font, text_col, 100, screen_height // 2 + 100)
        elif game_over == -1:
            draw_text('YOU LOST!', font, text_col, 100, screen_height // 2 + 50)
            draw_text('CLICK ANYWHERE TO START', font, text_col, 100, screen_height // 2 + 100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
            live_ball = True
            ball.reset(player_paddle.x + (player_paddle.width//2), player_paddle.y - player_paddle.height)
            player_paddle.reset()
            wall.create_wall()
    pygame.display.update()
pygame.quit()