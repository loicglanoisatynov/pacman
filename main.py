import pygame, sys
from src.settings import WIDTH, HEIGHT, NAV_HEIGHT
from src.classes.objects.world import World

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + NAV_HEIGHT))
pygame.display.set_caption("PacMan")
pygame.display.set_icon(pygame.image.load("assets/pac/right/0.png"))

# Classe principale. Gère le jeu
class Main:
    def __init__(self, screen):
        self.screen = screen
        self.FPS = pygame.time.Clock()
    def main(self):
        world = World(self.screen) # Créer un objet World qui sera l'objet de toutes les opérations de la partie
        world.ask_for_mode() # Demande le mode de jeu

        while True: # Boucle principale
            self.screen.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            world.update() # Met à jour le jeu
            pygame.display.update()
            self.FPS.tick(30)

# Lance le jeu
if __name__ == "__main__":
    play = Main(screen)
    play.main()