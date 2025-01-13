import pygame
import time
from settings import HEIGHT, WIDTH, NAV_HEIGHT, CHAR_SIZE, MAP, PLAYER_SPEED
from pac import Pac
from cell import Cell
from berry import Berry
from ghost import Ghost
from display import Display

class World:
    def __init__(self, screen):
        self.screen = screen
        self.player = pygame.sprite.GroupSingle()
        self.ghosts = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.berries = pygame.sprite.Group()
        self.display = Display(self.screen)
        self.game_over = False
        self.reset_pos = False
        self.player_score = 0
        self.game_level = 1
        self.walls_collide_list = []
        self._generate_world()

    # Gènère la map avec le fichier settings
    def _generate_world(self):
        for y_index, col in enumerate(MAP):
            for x_index, char in enumerate(col):
                position = (x_index, y_index)
                self._create_entity(char, position)
        self.walls_collide_list = [wall.rect for wall in self.walls.sprites()]

    def _create_entity(self, char, position):
        x_index, y_index = position
        if char == "1":  # Murs
            self.walls.add(Cell(x_index, y_index, CHAR_SIZE, CHAR_SIZE))
        elif char == " ":  # Petites baies
            self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 4))
        elif char == "B":  # Super baies
            self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 2, is_power_up=True))
        elif char in "spro":  # Fantômes
            color = {"s": "skyblue", "p": "pink", "o": "orange", "r": "red"}[char]
            self.ghosts.add(Ghost(x_index, y_index, color))
        elif char == "P":  # Pac-Man
            self.player.add(Pac(x_index, y_index))

    def generate_new_level(self):
        for y_index, col in enumerate(MAP):
            for x_index, char in enumerate(col):
                if char == " ":
                    self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 4))
                elif char == "B":
                    self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 2, is_power_up=True))
        time.sleep(2)

    def restart_level(self):
        self.berries.empty()
        for ghost in self.ghosts.sprites():
            ghost.move_to_start_pos()
        pacman = self.player.sprite
        pacman.reset_stats()
        self.game_level = 1
        self.game_over = False
        self.generate_new_level()

    def _dashboard(self):
        nav = pygame.Rect(0, HEIGHT, WIDTH, NAV_HEIGHT)
        pygame.draw.rect(self.screen, pygame.Color("cornsilk4"), nav)
        pacman = self.player.sprite
        self.display.show_life(pacman.life)
        self.display.show_level(self.game_level)
        self.display.show_score(pacman.pac_score)

    def _check_game_state(self):
        pacman = self.player.sprite
        if pacman.life <= 0:
            self.game_over = True
        elif len(self.berries) == 0 and pacman.life > 0:
            self._advance_level()

    def _advance_level(self):
        self.game_level += 1
        for ghost in self.ghosts.sprites():
            ghost.increase_speed(self.game_level)
            ghost.move_to_start_pos()
        pacman = self.player.sprite
        pacman.move_to_start_pos()
        pacman.reset_direction()
        self.generate_new_level()

    def _handle_teleport(self, pacman):
        if pacman.rect.right <= 0:
            pacman.rect.x = WIDTH
        elif pacman.rect.left >= WIDTH:
            pacman.rect.x = 0

    def _handle_berry_collision(self, pacman):
        for berry in self.berries.sprites():
            if pacman.rect.colliderect(berry.rect):
                pacman.eat_berry(berry)
                berry.kill()

    def _handle_ghost_collision(self, pacman):
        for ghost in self.ghosts.sprites():
            if pacman.rect.colliderect(ghost.rect):
                if pacman.immune:
                    ghost.move_to_start_pos()
                    pacman.pac_score += 100
                else:
                    time.sleep(2)
                    pacman.life -= 1
                    self.reset_pos = True
                    break

    def _reset_positions(self):
        for ghost in self.ghosts.sprites():
            ghost.move_to_start_pos()
        pacman = self.player.sprite
        pacman.move_to_start_pos()
        pacman.move_to_start_pos()
        self.reset_pos = False

    # Met à jour à chaque frames
    def update(self):
        if not self.game_over:
            pacman = self.player.sprite
            pressed_key = pygame.key.get_pressed()
            pacman.animate(pressed_key, self.walls_collide_list)
            self._handle_teleport(pacman)
            self._handle_berry_collision(pacman)
            self._handle_ghost_collision(pacman)

        self._check_game_state()

        # Rendu des entités
        [wall.update(self.screen) for wall in self.walls.sprites()]
        [berry.update(self.screen) for berry in self.berries.sprites()]
        [ghost.update(self.walls_collide_list) for ghost in self.ghosts.sprites()]
        self.ghosts.draw(self.screen)
        self.player.update()
        self.player.draw(self.screen)

        # Tableau de bord
        if self.game_over:
            self.display.game_over()
        else:
            self._dashboard()

        # Réinitialisation des positions
        if self.reset_pos and not self.game_over:
            self._reset_positions()

        # Redémarrage du jeu
        if self.game_over and pygame.key.get_pressed()[pygame.K_r]:
            self.restart_level()
