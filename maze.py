import math
import pygame
import button
import colour
import cell

DIMENSIONS = (400, 400)

SURFACE = pygame.Surface(DIMENSIONS)
SURFACE.fill(colour.WHITE)

CLOCK = pygame.time.Clock()
WIDTH_OF_SQUARE = 20
FPS = 30

COLS = math.floor(DIMENSIONS[0] / WIDTH_OF_SQUARE)
ROWS = math.floor(DIMENSIONS[1] / WIDTH_OF_SQUARE)


class Maze:
    """ Main application class. """

    def __init__(self, screen):
        self.screen = screen
        update(screen)
        self.grid_of_cells = []
        self.stack_of_cells = []
        self.maze_generators = {
            "depth-first-search": self.depth_first_search,
            "hunt-and-kill": self.hunt_and_kill,
            "binary-tree": self.binary_tree
        }

    def setup(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.grid_of_cells.append(cell.Cell(row, col))

    def draw_grid(self):
        """ Show Cells """
        for this_cell in self.grid_of_cells:
            this_cell.show(SURFACE)
        update(self.screen)

    def create_maze(self, maze_generator):
        self.draw_grid()
        self.maze_generators[maze_generator]()

    def display_maze(self, current, paint):
        CLOCK.tick(FPS)
        colour_cell(current, paint)
        self.show_path(current, colour.DARK_GREEN)
        update(self.screen)

    def reset(self):
        self.grid_of_cells.clear()
        self.setup()
        SURFACE.fill(colour.WHITE)
        update(self.screen)

    def show_path(self, current, paint):
        for this_cell in self.grid_of_cells:
            if this_cell != current:
                if this_cell.visited:
                    colour_cell(this_cell, paint)
            this_cell.show(SURFACE)

    """Maze generation Algorithms"""

    def depth_first_search(self):
        """ Basic Recursive Backtracking to generate a game """
        current_cell = self.grid_of_cells[0]

        while True:
            current_cell.visited = True
            self.display_maze(current_cell, colour.PINK)
            neighbour = current_cell.get_random_neighbour(self.grid_of_cells)
            if neighbour is not None:
                self.stack_of_cells.append(current_cell)
                remove_walls(current_cell, neighbour)
                current_cell = neighbour
            elif len(self.stack_of_cells) > 0:
                current_cell = self.stack_of_cells.pop()
            else:
                self.display_maze(current_cell, colour.DARK_GREEN)
                break

    def hunt_and_kill(self):
        """ Hunt and Kill to generate a game """
        current_cell = self.grid_of_cells[0]

        while True:
            current_cell.visited = True
            self.display_maze(current_cell, colour.PINK)
            neighbour = current_cell.get_random_neighbour(self.grid_of_cells)
            if neighbour is not None:
                remove_walls(current_cell, neighbour)
                current_cell = neighbour
            else:
                neighbour = find_unvisited_cell(self.grid_of_cells)
                self.display_maze(current_cell, colour.DARK_GREEN)
                if neighbour is None:
                    break
                remove_walls(current_cell, neighbour)
                current_cell = neighbour

    def binary_tree(self):

        while True:
            current_row = 0
            for col in range(COLS):
                index = self.grid_of_cells[get_index(current_row, col)]
                current_cell = self.grid_of_cells[index]
                self.display_maze(current_cell, colour.PINK)
                neighbour = current_cell.get_random_neighbour(self.grid_of_cells)
                if neighbour is not None:
                    remove_walls(current_cell, neighbour)

    """Maze Solving Algorithms"""

    def flood_fill(self):
        pass

    def A_Star_Search(self):
        pass


def update(screen):
    pygame.draw.rect(SURFACE, colour.BLACK, (0, 0, 400, 400), 1)
    screen.blit(SURFACE, (20, 20))
    pygame.display.flip()


def colour_cell(this_cell, paint):
    w = WIDTH_OF_SQUARE
    x = this_cell.col * w
    y = this_cell.row * w
    pygame.draw.rect(SURFACE, paint, (x + 1, y + 1, w, w))


def get_index(row, col):
    if col < 0 or row < 0 or col > COLS - 1 or row > ROWS - 1:
        return -1
    return col + (row * COLS)


def remove_walls(this_cell, neighbour):
    cell_index = get_index(this_cell.row, this_cell.col)
    neighbour_index = get_index(neighbour.row, neighbour.col)

    TOP_NEIGHBOUR = COLS
    RIGHT_NEIGHBOUR = -1
    LEFT_NEIGHBOUR = 1
    BOTTOM_NEIGHBOUR = -ROWS

    if cell_index - neighbour_index == TOP_NEIGHBOUR:
        this_cell.eliminate_wall("top", False)
        neighbour.eliminate_wall("bottom", False)

    if cell_index - neighbour_index == RIGHT_NEIGHBOUR:
        this_cell.eliminate_wall("right", False)
        neighbour.eliminate_wall("left", False)

    if cell_index - neighbour_index == LEFT_NEIGHBOUR:
        this_cell.eliminate_wall("left", False)
        neighbour.eliminate_wall("right", False)

    if cell_index - neighbour_index == BOTTOM_NEIGHBOUR:
        this_cell.eliminate_wall("bottom", False)
        neighbour.eliminate_wall("top", False)


def find_unvisited_cell(cells: list):
    for this_cell in cells:
        if not this_cell.visited:
            neighbours = this_cell.get_neighbours(cells)
            for neighbour in neighbours:
                if neighbour.visited:
                    return neighbour
    return None


def clear_surface():
    SURFACE.fill(colour.WHITE)
    pygame.draw.rect(SURFACE, colour.BLACK, (0, 0, 400, 400), 2)
