import random

import pygame
import enum
import time
import curses
from typing import List

BG = (148, 148, 148)
RED = (224, 43, 40)
GREEN = (20, 133, 24)
BLUE = (77, 115, 232)
BLACK = (0, 0, 0)
GRAY = (140, 140, 140)

WIDTH, HEIGHT = 400, 400
ROW, COL = 15, 15
LINE_THICKNESS = 2
CELL_SIZE = WIDTH // ROW

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")


class Direction(enum.Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class CellType(enum.Enum):
    EMPTY = 0
    SNAKE = 1
    FRUIT = 2
    OBSTACLE = 3


class Snake:

    def __init__(self, x, y):
        self.body = [[x, y]]
        self.direction = Direction.UP

    def move(self, new_direction: Direction):
        body = self.body
        current_direction = self.direction

        if current_direction not in Direction:
            print("Direction does not exist")
            return

        head_x, head_y = body[0]

        if Direction.RIGHT.value in (current_direction.value, new_direction.value):
            head_x += 1
        elif Direction.LEFT.value in (current_direction.value, new_direction.value):
            head_x -= 1
        elif Direction.UP.value in (current_direction.value, new_direction.value):
            head_y -= 1
        else:
            head_y += 1

        new_head = [head_x, head_y]

        if self._check_collision(new_head):
            return

        if len(body) == 1:
            new_body = [new_head]
            body.clear()  # Do we need clear list? Or garbage collector handle it?!
        else:
            # Check collision
            if new_head in self.body[1:]:
                return
            else:
                body.pop()
                new_body = [new_head, *body[:]]

        self.body = new_body

    def set_direction(self, new_direction):

        if new_direction not in Direction:
            print("Invalid direction")
            return

        # Check opposite directions:
        if new_direction == Direction.DOWN and self.direction == Direction.UP:
            return
        elif new_direction == Direction.UP and self.direction == Direction.DOWN:
            return
        elif new_direction == Direction.LEFT and self.direction == Direction.RIGHT:
            return
        elif new_direction == Direction.RIGHT and self.direction == Direction.LEFT:
            return

        self.direction = new_direction

        return self.direction

    def get_direction(self):
        return self.direction

    def append_tail(self):
        current_tail_x, current_tail_y = self.body[-1]
        new_tail_x, new_tail_y = current_tail_x + 1, current_tail_y + 1

        if 0 <= new_tail_x <= ROW and 0 <= new_tail_y <= COL:
            self.body.append([new_tail_x, new_tail_y])
        else:
            print("Tail is out of the box")

    @staticmethod
    def _check_collision(next_step):
        x, y = next_step
        return x < 0 or x >= ROW or y < 0 or y >= COL


class Fruit:
    INTERVAL_SEC = 10

    def __init__(self, x, y, lifespan):
        self.x = x
        self.y = y
        self.lifespan = lifespan + self.INTERVAL_SEC

    def set_position(self, x=None, y=None):
        if x is None or y is None:
            # ToDo: avoid position which is not EMPTY
            x, y = self._generate_random_position()

        if 0 <= x <= ROW and 0 <= y <= COL:
            self.x = x
            self.y = y
        else:
            print("Invalid position.")

    def remove_position(self):
        self.x, self.y = None, None

    def get_position(self):
        return [self.x, self.y]

    def update_lifespan(self):
        current_timestamp = time.time()
        self.lifespan = current_timestamp + self.INTERVAL_SEC

    @staticmethod
    def _generate_random_position():
        return [random.randrange(0, ROW), random.randrange(0, COL)]


class Gameboard:

    def __init__(self, weight, height):
        self.weight = weight
        self.height = height
        self.board = [
            [CellType.EMPTY.value for _ in range(weight)] for _ in range(height)
        ]

    def add_item_on_board(self, item: List, cell_type: CellType):
        for coordinates in item:
            col, row = coordinates
            self.board[row][col] = cell_type.value

    def clear_board(self):
        self.board = [
            [CellType.EMPTY.value for _ in range(self.weight)]
            for _ in range(self.height)
        ]


def draw_grid(win, color):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(win, color, (x, 0), (x, HEIGHT), LINE_THICKNESS)
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(win, color, (0, y), (WIDTH, y), LINE_THICKNESS)


def draw_pixel(win, color, x, y, width, height):
    pygame.draw.rect(win, color, (x, y, width, height))


def draw_items(win, items, color, width, height):
    for coordinate in items:
        x, y = coordinate
        draw_pixel(win, color, x * width, y * height, width, height)


def main(win):
    running = True
    score = 0

    snake = Snake(5, 5)
    fruit = Fruit(5, 1, time.time())
    gameboard = Gameboard(ROW, COL)
    fruit.update_lifespan()

    while running:
        win.fill(BG)
        snake_head = snake.body[0]

        if time.time() > fruit.lifespan:
            fruit.remove_position()
            fruit.update_lifespan()
            fruit.set_position()

        if snake_head == fruit.get_position():
            score += 1

            fruit.remove_position()
            fruit.update_lifespan()
            fruit.set_position()
            gameboard.add_item_on_board([fruit.get_position()], CellType.FRUIT)
            snake.append_tail()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.set_direction(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.set_direction(Direction.RIGHT)
                elif event.key == pygame.K_DOWN:
                    snake.set_direction(Direction.DOWN)
                elif event.key == pygame.K_UP:
                    snake.set_direction(Direction.UP)

        snake.move(snake.direction)

        if snake_head == snake.body[0]:
            print("Game is over")
            break

        gameboard.add_item_on_board(snake.body, CellType.SNAKE)
        gameboard.add_item_on_board([fruit.get_position()], CellType.FRUIT)

        # Draw board
        draw_grid(win, GRAY)

        # Draw snake
        draw_items(win, snake.body, GREEN, CELL_SIZE, CELL_SIZE)

        # Draw fruit
        draw_items(win, [[fruit.x, fruit.y]], RED, CELL_SIZE, CELL_SIZE)

        pygame.display.flip()

        gameboard.clear_board()

        time.sleep(0.5)
    pygame.quit()


main(WIN)
