import pygame
import random
from src.settings import WIDTH, CHAR_SIZE, GHOST_SPEED

class Ghost(pygame.sprite.Sprite):
    def __init__(self, row, col, color):
        super().__init__()
        # Position initiale
        self.start_pos = (row * CHAR_SIZE, col * CHAR_SIZE)
        self.rect = pygame.Rect(self.start_pos, (CHAR_SIZE, CHAR_SIZE))
        self.move_speed = GHOST_SPEED
        self.color = pygame.Color(color)
        
        # Directions possibles
        # Va changer
        self.directions = {
            'left': (-self.move_speed, 0),
            'right': (self.move_speed, 0),
            'up': (0, -self.move_speed),
            'down': (0, self.move_speed)
        }
        self.keys = list(self.directions.keys())
        self.direction = (0, 0)
        self.moving_dir = "up"

        # Chargement des images pour les animations
        self.img_path = f'assets/ghosts/{color}/'
        self.images = self._load_images()
        self.image = self.images[self.moving_dir]
        self.mask = pygame.mask.from_surface(self.image)

    # Charge toute les images des direction multiples
    def _load_images(self):
        return {
            direction: pygame.transform.scale(
                pygame.image.load(f'{self.img_path}{direction}.png'),
                (CHAR_SIZE, CHAR_SIZE)
            )
            for direction in self.keys
        }
    
    def increase_speed(self):
        self.move_speed += 1

    # Réinitialisation des positions
    def move_to_start_pos(self):
        self.rect.topleft = self.start_pos
        self.direction = (0, 0)
        self.moving_dir = "up"
        self.image = self.images[self.moving_dir]

    def _is_collide(self, x, y, walls_collide_list):
        tmp_rect = self.rect.move(x, y)
        return tmp_rect.collidelist(walls_collide_list) != -1

    def _get_available_moves(self, walls_collide_list):
        return [
            key for key in self.keys
            if not self._is_collide(*self.directions[key], walls_collide_list)
        ]

    # Change les directions, va être utile pour l'IA
    def _choose_direction(self, available_moves):
        if len(available_moves) > 2 or self.direction == (0, 0):
            if random.random() <= 0.6:  # 60% de proba
                self.moving_dir = random.choice(available_moves)
                self.direction = self.directions[self.moving_dir]

    # Téléportation pour les côtés de la map
    def _handle_teleport(self):
        if self.rect.right <= 0:
            self.rect.x = WIDTH
        elif self.rect.left >= WIDTH:
            self.rect.x = 0

    #Gère le changement d'image en fonction de la direction
    def _animate(self):
        self.image = self.images[self.moving_dir]

    def update(self, walls_collide_list):
        # Obtenir les mouvements disponibles | mur ou pas
        available_moves = self._get_available_moves(walls_collide_list)

        self._choose_direction(available_moves)

        if not self._is_collide(*self.direction, walls_collide_list):
            self.rect.move_ip(self.direction)
        else:
            self.direction = (0, 0)

        self._handle_teleport()

        self._animate()
