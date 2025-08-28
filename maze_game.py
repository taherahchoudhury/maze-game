import pygame
import button
import colour
from maze import Maze

SCREEN_WIDTH = 650
SCREEN_HEIGHT = 440

display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.init()
display.fill(colour.GREEN)

pygame.display.set_caption("Python Maze Game")

create_maze_img1 = pygame.image.load("create-maze-button-01.png").convert_alpha()
create_maze_img2 = pygame.image.load("create-maze-button-02.png").convert_alpha()

solve_maze_img1 = pygame.image.load("solve-maze-button-01.png").convert_alpha()
solve_maze_img2 = pygame.image.load("solve-maze-button-02.png").convert_alpha()


def main():
    the_maze = Maze(display)
    the_maze.setup()

    # create button
    create_maze_btn = button.Button(450, 23, create_maze_img1, create_maze_img2, 0.18)
    solve_maze_btn = button.Button(450, 100, solve_maze_img1, solve_maze_img2, 0.18)

    running = True

    while running:
        # display.blit(SURFACE, (20, 20))
        clicked = create_maze_btn.draw(display)
        solve_maze_btn.draw(display)

        if clicked:
            the_maze.reset()
            the_maze.create_maze("depth-first-search")

        # process input (events)
        for event in pygame.event.get():
            # check for closing the window
            if event.type == pygame.QUIT:
                running = False


if __name__ == "__main__":
    main()
