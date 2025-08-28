import pygame


class Button:
    def __init__(self, x, y, image1, image2, scale):
        width = image1.get_width()
        height = image1.get_height()
        self.image = pygame.transform.scale(image1, (int(width * scale), int(height * scale)))
        self.hover_image = pygame.transform.scale(image2, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            surface.blit(self.hover_image, (self.rect.x, self.rect.y))
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y))

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        pygame.display.flip()

        return action
