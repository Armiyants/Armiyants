import pygame
import random
import time

# set up pygame window
WIDTH = 500
HEIGHT = 600
FPS = 30

# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initalise Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Maze Generator")
clock = pygame.time.Clock()

# maze variables
x = 0
y = 0
w = 20
grid = []
visited_cells = []
stack = []
solution_dict = {}


# creating grid

def create_grid(x, y, w):
    for i in range(0, 21):  # we want a maze of 20x20
        x = 20  # start position
        y = y + 20  # start a new row
        for j in range(1, 21):
            pygame.draw.line(screen, WHITE, [x, y], [x + w, y])  # top of the cell
            pygame.draw.line(screen, WHITE, [x + w, y], [x + w, y + w])  # right of the cell
            pygame.draw.line(screen, WHITE, [x + w, y + w], [x, y + w])  # bottom of the cell
            pygame.draw.line(screen, WHITE, [x, y + w], [x, y])  # left of the cell
            grid.append((x, y))
            x = x + 20


# draw a rectangle twice the width of the cell to animate the wall being removed
def push_down(x, y):
    pygame.draw.rect(screen, BLUE, (x + 1, y + 1, 19, 39), 0)
    pygame.display.update()


def push_up(x, y):
    pygame.draw.rect(screen, BLUE, (x + 1, y - w + 1, 19, 39), 0)
    pygame.display.update()


def push_left(x, y):
    pygame.draw.rect(screen, BLUE, (x - w + 1, y + 1, 39, 19), 0)
    pygame.display.update()


def push_right(x, y):
    pygame.draw.rect(screen, BLUE, (x + 1, y + 1, 39, 19), 0)
    pygame.display.update()


# draw a single width cell
def single_cell(x, y):
    # pygame.draw.rect(screen, GREEN, (x, y, 20, 20), 0)
    # pygame.display.update()
    return


def backtracking_cell(x, y):
    return
    # pygame.draw.rect(screen, BLUE, (x, y, 20, 20), 0)
    # pygame.display.update()


def solution_cell(x, y):
    pygame.draw.rect(screen, GREEN, (x+5, y+5, 10, 10), 0)
    pygame.display.update()


def carve_out_maze(x, y):
    single_cell(x, y)  # starting  maze
    stack.append((x, y))  # placing starting cell into stack
    visited_cells.append((x, y))  # adding visited cell into list
    # checking with loop if there are any not visited cells that are my neighbours
    while len(stack) > 0:
        time.sleep(.001)
        cell = []
        if (x + w, y) not in visited_cells and (x + w, y) in grid:
            cell.append("right")
        if (x - w, y) not in visited_cells and (x - w, y) in grid:
            cell.append("left")
        if (x, y + w) not in visited_cells and (x, y + w) in grid:
            cell.append("down")
        if (x, y - w) not in visited_cells and (x, y - w) in grid:
            cell.append("up")
        if len(cell) > 0:
            cell_chosen = (random.choice(cell))
            if cell_chosen == "right":
                push_right(x, y)
                solution_dict[(x + w, y)] = x, y
                x = x + w  # make this cell the current cell
                visited_cells.append((x, y))
                stack.append((x, y))
            elif cell_chosen == "left":
                push_left(x, y)
                solution_dict[(x - w, y)] = x, y
                x = x - w
                visited_cells.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "up":
                push_up(x, y)
                solution_dict[(x, y - w)] = x, y
                y = y - w
                visited_cells.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "down":
                push_down(x, y)
                solution_dict[(x, y + w)] = x, y
                y = y + w
                visited_cells.append((x, y))
                stack.append((x, y))

        # if no cell is available pop one from stack (the last element)
        else:
            x, y = stack.pop()
            single_cell(x, y)  # to show backtracking image
            time.sleep(.001)
            backtracking_cell(x, y)  # change colour to identify backtracking path


def route_back(x, y):
    solution_cell(x, y)
    while (x, y) != (20, 20):
        x, y = solution_dict[x, y]
        solution_cell(x, y)
        time.sleep(.001)


x, y = 20,20
create_grid(40, 0, 20)
carve_out_maze(x, y)
print(solution_dict)
route_back(400, 400)
print(visited_cells)

# Pygame loop

##### pygame loop #######
running = True
while running:
    # keep running at the at the right speed
    clock.tick(FPS)
    # process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
