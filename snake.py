import random

import pygame
import enum
import time

BG = (0, 25, 40)
WIDTH, HEIGHT = 100, 100
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Snake")


class Direction(enum.Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class Snake:

    def __init__(self, x, y):
        self.body = [[x, y], [x - 1, y - 1], [x - 2, y - 2]]
        self.direction = Direction.RIGHT

    def move(self, new_direction: Direction):
        body = self.body
        current_direction = self.direction

        if current_direction != new_direction:
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

        if len(body) == 1:
            new_body = [new_head]
            body.clear()  # Do we need clear list? Or garbage collector handle it?!
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

        if 0 <= new_tail_x <= WIDTH and 0 <= new_tail_y <= HEIGHT:
            self.body.append([new_tail_x, new_tail_y])
        else:
            print('Tail is out of the box')


class Fruit:
    INTERVAL_SEC = 10

    def __init__(self, x, y, lifespan):
        self.x = x
        self.y = y
        self.lifespan = lifespan + self.INTERVAL_SEC

    def set_position(self, x=None, y=None):
        if x is None or y is None:
            x, y = self._generate_random_position()

        if 0 <= x <= WIDTH and 0 <= y <= HEIGHT:
            self.x = x
            self.y = y
        else:
            print('Invalid position.')

    def remove_position(self):
        self.x, self.y = None, None

    def get_position(self):
        return [self.x, self.y]

    def update_lifespan(self):
        current_timestamp = time.time()
        self.lifespan = current_timestamp + self.INTERVAL_SEC

    @staticmethod
    def _generate_random_position():
        return [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]


class Gameboard:
    pass


def main():
    running = True

    snake = Snake(50, 50)
    fruit = Fruit(55, 50, time.time())
    score = 0
    fruit.update_lifespan()

    while running:
        fruit_position = fruit.get_position()

        if time.time() > fruit.lifespan:
            fruit.remove_position()
            fruit.update_lifespan()
            fruit.set_position()
            fruit_position = fruit.get_position()

        snake_head = snake.body[0]

        if snake_head == fruit_position:
            score += 1
            snake.append_tail()
            fruit.remove_position()
            fruit.update_lifespan()
            fruit.set_position()
            fruit_position = fruit.get_position()

        snake.move(snake.direction)
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

        print(f'Snake: {snake.body}')
        print(f'Fruit: {fruit_position}')
        print(f'Score: {score}')

        time.sleep(1)
    pygame.quit()


main()
