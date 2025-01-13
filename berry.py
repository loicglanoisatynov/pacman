import pygame
from settings import CHAR_SIZE

# Gère les points, elle va changer car au lieu de mettre des cercle dessiné
# j'opterai pour des images directement
class Berry(pygame.sprite.Sprite):
    def __init__(self, row, col, size, is_power_up=False):

        super().__init__()
        self.power_up = is_power_up
        self.size = size
        self.color = pygame.Color("violetred") if not is_power_up else pygame.Color("gold")
        self.position = (
            (row * CHAR_SIZE) + (CHAR_SIZE // 2),
            (col * CHAR_SIZE) + (CHAR_SIZE // 2),
        )

        # Rectangle pour gérer les collisions
        self.rect = pygame.Rect(
            self.position[0] - size, 
            self.position[1] - size, 
            size * 2, 
            size * 2
        )


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.size)

    def update(self, screen):
        self.draw(screen)
