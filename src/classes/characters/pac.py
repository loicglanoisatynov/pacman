import pygame
from src.settings import CHAR_SIZE, PLAYER_SPEED
from src.animation import import_sprite


class Pac(pygame.sprite.Sprite):
    def __init__(self, row, col):
        super().__init__()
        # Position initiale
        self.start_pos = (row * CHAR_SIZE, col * CHAR_SIZE)
        self.rect = pygame.Rect(self.start_pos, (CHAR_SIZE, CHAR_SIZE))

        # Animation
        self.animations = {}
        self.frame_index = 0
        self.animation_speed = 0.5
        self.image = None
        self._import_character_assets()
        self.status = "idle"
        self.current_pos = (row, col)
        self.last_pos = self.current_pos

        # Attributs de Pac-Man
        self.pac_speed = PLAYER_SPEED
        self.directions = {
            'left': (-PLAYER_SPEED, 0),
            'right': (PLAYER_SPEED, 0),
            'up': (0, -PLAYER_SPEED),
            'down': (0, PLAYER_SPEED)
        }
        self.keys = {
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'up': pygame.K_UP,
            'down': pygame.K_DOWN
        }
        self.direction = (0, 0)
        self.life = 3
        self.pac_score = 0
        self.immune = False
        self.immune_time = 0
        self.walls_collide_list = []
        self.last_direction = None

    def _import_character_assets(self):
        character_path = "assets/pac/"
        actions = ["up", "down", "left", "right", "idle", "power_up"]
        self.animations = {action: import_sprite(f"{character_path}{action}") for action in actions}

    def move_to_start_pos(self):
        self.rect.topleft = self.start_pos

    def reset_stats(self):
        self.pac_score = 0
        self.life = 3
        self.immune = False
        self.immune_time = 0
        self.move_to_start_pos()
        self.direction = (0, 0)
        self.status = "idle"

    def _is_collide(self, x, y):
        tmp_rect = self.rect.move(x, y)
        return tmp_rect.collidelist(self.walls_collide_list) != -1

    def _update_animation(self):
        if not self._is_moving():
            animation = self.animations[self.status]
            self.image = pygame.transform.scale(animation[0], (CHAR_SIZE, CHAR_SIZE))
            
            return
        animation = self.animations[self.status]
        self.frame_index = (self.frame_index + self.animation_speed) % len(animation)
        self.image = pygame.transform.scale(animation[int(self.frame_index)], (CHAR_SIZE, CHAR_SIZE))

    def _update_direction(self, pressed_key):
        for key, key_value in self.keys.items():
            if pressed_key[key_value] and not self._is_collide(*self.directions[key]):
                self.direction = self.directions[key]
                self.status = "power_up" if self.immune else key
                self.last_direction = key  # Stocke la dernière direction avant de s'arrêter
                break

    
    def _rotate_idle(self):
        if self.last_direction:
            self.status = self.last_direction  # Garde la dernière direction
        else:
            self.status = "idle"


    def _is_moving(self):
        return self.direction != (0, 0)

    def animate(self, pressed_key, walls_collide_list):
        self.walls_collide_list = walls_collide_list
        
        self._rotate_idle()

        # if self._is_moving():
        self._update_animation()
        self._update_direction(pressed_key)

        if not self._is_collide(*self.direction):
            self.rect.move_ip(self.direction)
        else:
            self.direction = (0, 0)
            self._rotate_idle()  # Appliquer l'orientation de la dernière direction


    def eat_berry(self, berry):
        if berry.power_up:
            self.immune = True
            self.immune_time = 150  # Durée de l'immunité avec les super baie
            self.pac_score += 50  # Points pour une super baie
        else:
            self.pac_score += 10  # Points pour une petite baie

    def update(self): # Fonction qui permet de mettre à jour les attributs lors de l'animation
        if self.immune_time > 0:
            self.immune_time -= 1
        else:
            self.immune = False

        # Avant modification
        # La fonction get_rect() permet de mettre à jour la position de l'image
        # self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))

        # Après modification
        if not self._is_moving():
            self._rotate_idle()
        
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
