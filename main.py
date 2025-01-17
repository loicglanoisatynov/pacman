import pygame, sys
from src.settings import WIDTH, HEIGHT, NAV_HEIGHT
from src.classes.objects.world import World

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + NAV_HEIGHT))
pygame.display.set_caption("PacMan")
pygame.display.set_icon(pygame.image.load("assets/pac/right/0.png"))


class Main:
    def __init__(self, screen):
        self.screen = screen
        self.FPS = pygame.time.Clock()
    def main(self):
        world = World(self.screen)
        world.ask_for_mode()
        while True:
            self.screen.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            world.update()
            pygame.display.update()
            self.FPS.tick(30)

    


if __name__ == "__main__":
    play = Main(screen)
    play.main()