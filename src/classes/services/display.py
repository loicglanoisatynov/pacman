import pygame
from src.settings import WIDTH, HEIGHT, CHAR_SIZE
pygame.font.init()

# Gère tout l'affichage, va changer pour quelque choses de plus beau
class Display:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("ubuntumono", CHAR_SIZE)
        self.game_over_font = pygame.font.SysFont("dejavusansmono", 48)
        self.text_color = pygame.Color("crimson")
        self.life_image = self._load_image("assets/life/life.png", (CHAR_SIZE, CHAR_SIZE))

    @staticmethod
    def _load_image(path, size):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)

    def _render_text(self, text, font, color, position):
        rendered_text = font.render(text, True, color)
        self.screen.blit(rendered_text, position)

    def show_life(self, life):
        life_x = CHAR_SIZE // 2
        for _ in range(life):
            self.screen.blit(self.life_image, (life_x, HEIGHT + (CHAR_SIZE // 2)))
            life_x += CHAR_SIZE

    def show_level(self, level):
        level_x = WIDTH // 3
        self._render_text(f'Level {level}', self.font, self.text_color, (level_x, HEIGHT + (CHAR_SIZE // 2)))

    def show_score(self, score):
        score_x = (WIDTH // 3) * 2
        self._render_text(f'{score}', self.font, self.text_color, (score_x, HEIGHT + (CHAR_SIZE // 2)))

    def game_over(self):
        message_position = (WIDTH // 4, HEIGHT // 3)
        instruction_position = (WIDTH // 4, HEIGHT // 2)
        self._render_text('GAME OVER!!', self.game_over_font, pygame.Color("chartreuse"), message_position)
        self._render_text('Press "R" to Restart', self.font, pygame.Color("aqua"), instruction_position)

