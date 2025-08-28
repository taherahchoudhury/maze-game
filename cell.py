import random
import pygame
import maze
import colour


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.walls = {"top": True, "left": True, "right": True, "bottom": True}
        self.visited = False

    def show(self, surface):
        w = maze.WIDTH_OF_SQUARE
        x = self.col * w
        y = self.row * w

        if self.walls["top"]:
            pygame.draw.line(surface, colour.BLACK, (x, y), (x + w, y))
        if self.walls["right"]:
            pygame.draw.line(surface, colour.BLACK, (x + w, y), (x + w, y + w))
        if self.walls["left"]:
            pygame.draw.line(surface, colour.BLACK, (x, y), (x, y + w))
        if self.walls["bottom"]:
            pygame.draw.line(surface, colour.BLACK, (x, y + w), (x + w, y + w))

    def get_random_neighbour(self, cells):

        unvisited_neighbours = []

        neighbours = self.get_neighbours(cells)
        for neighbour in neighbours:
            if not neighbour.visited:
                unvisited_neighbours.append(neighbour)

        # Return a random neighbour
        if len(unvisited_neighbours) > 0:
            return random.choice(unvisited_neighbours)
        return None

    def get_neighbours(self, cells):
        # Stores the neighbouring cells of a cell
        neighbours = []

        # the indexes for all possible neighbouring cells
        north_index = maze.get_index(self.row - 1, self.col)
        south_index = maze.get_index(self.row + 1, self.col)
        east_index = maze.get_index(self.row, self.col + 1)
        west_index = maze.get_index(self.row, self.col - 1)

        indexes = {north_index, south_index, east_index, west_index}

        for index in indexes:
            if index != -1:
                neighbour = cells[index]
                neighbours.append(neighbour)

        return neighbours

    # only setter
    def eliminate_wall(self, wall, boolean):
        self.walls[wall] = boolean
