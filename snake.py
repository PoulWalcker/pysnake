import pygame
import enum
import time

BG = (0, 25, 40)


class Direction(enum.Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class Snake:

    def __init__(self, x, y):
        self.body = [[x, y], [x - 1, y - 1], [x - 2, y - 2]]
        self.direction = Direction.DOWN

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


class Fruit:

    def __init__(self, x, y, lifespan):
        self.x = x
        self.y = y
        self.lifespan = lifespan

    def set_position(self):
        pass

    def get_position(self):
        pass

    def update_lifespan(self):
        pass


class Gameboard:
    pass


def main():
    WIDTH, HEIGHT = 100, 100
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    running = True

    snake = Snake(50, 50)

    while running:
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
        time.sleep(1)
    pygame.quit()


main()
