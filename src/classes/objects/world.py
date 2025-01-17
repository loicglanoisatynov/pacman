import pygame
import time
import numpy as np
from src.settings import HEIGHT, WIDTH, NAV_HEIGHT, CHAR_SIZE, MAP, PLAYER_SPEED, CURRENT_MODE, set_current_mode, get_current_mode
from src.classes.characters.pac import Pac
from src.classes.objects.cell import Cell
from src.classes.objects.berry import Berry
from src.classes.characters.ghost import Ghost
from src.classes.services.display import Display, set_current_mode
from src.DQN.Agent import Agent



class World:
    def __init__(self, screen):
        self.font = pygame.font.SysFont("ubuntumono", CHAR_SIZE)
        self.screen = screen
        self.player = pygame.sprite.GroupSingle()
        self.ghosts = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.berries = pygame.sprite.Group()
        self.display = Display(self.screen)
        self.game_over = False
        self.reset_pos = False
        self.game_over_passed = False
        self.mode_selected = False
        self.player_score = 0
        self.game_level = 1
        self.walls_collide_list = []
        self._generate_world()
        self.agent = Agent(len(self.get_state()), 4)

    def get_state(self): 
        pacman = self.get_player().sprite
        ghosts = [(g.rect.x, g.rect.y) for g in self.get_ghosts()]
        return np.array([pacman.rect.x, pacman.rect.y] + [x for ghost in ghosts for x in ghost])
    
    def step(self, action):
        pacman = self.get_player().sprite
        actions = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        print(action)
        print(actions)

        # pacman.direction = pacman.directions[action]


        self.update()
        reward = 1 if pacman.eat_berry() else -1
        done = self.game_over

        return self.get_state(), reward, done

    def paint_world(self):
        self.screen.fill("black")
        [wall.update(self.screen) for wall in self.get_walls()]
        [berry.update(self.screen) for berry in self.get_berries()]
        [ghost.update(self.walls_collide_list) for ghost in self.get_ghosts()]
        self.ghosts.draw(self.screen)
        self.player.update()
        self.player.draw(self.screen)

    def get_world(self):
        return self
    
    def get_screen(self):
        return self.screen
    
    def get_player(self):
        return self.player
    
    def get_ghosts(self):
        return self.ghosts
    
    def get_walls(self):
        return self.walls
    
    def get_berries(self):
        return self.berries
    
    def get_display(self):
        return self.display

    def _render_text(self, text, font, color, position):
        rendered_text = font.render(text, True, color)
        self.screen.blit(rendered_text, position)
    
    # Génère la map avec le fichier settings
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

    def restart_level(self):
        self.berries.empty()
        for ghost in self.ghosts.sprites():
            ghost.move_to_start_pos()
        pacman = self.player.sprite
        pacman.reset_stats()
        self.game_level = 1
        self.game_over = False
        self.game_over_passed = False
        self.mode_selected = False
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

    def ask_for_mode(self):
        # Ouvre une fenêtre pour choisir le mode de jeu (humain, IA ou IA training)
        self._render_text('Choose a mode:', self.font, pygame.Color("aqua"), (WIDTH // 4, HEIGHT // 2))
        self._render_text('1: Human', self.font, pygame.Color("aqua"), (WIDTH // 4, HEIGHT // 2 + CHAR_SIZE))
        self._render_text('2: AI (very dumb)', self.font, pygame.Color("aqua"), (WIDTH // 4, HEIGHT // 2 + CHAR_SIZE * 2))
        self._render_text('3: AI Training (not functionnal)', self.font, pygame.Color("aqua"), (WIDTH // 4, HEIGHT // 2 + CHAR_SIZE * 3))
        
        mode_selected = False
        while not mode_selected:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    set_current_mode("human")
                    mode_selected = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    set_current_mode("ai")
                    mode_selected = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    set_current_mode("ai_training")
                    mode_selected = True
            pygame.display.update()

    # Met à jour à chaque frames
    def update(self):
        if not self.game_over:
            pressed_key = {}
            pacman = self.player.sprite
            if get_current_mode() == "human":
                pressed_key = pygame.key.get_pressed()

            elif get_current_mode() == "ai":
                direction = Agent.ai_move(self.agent, self.get_state())
                pressed_key = {direction: True}

            # print()
            # print(pressed_key)
            # print()
            # print(type(pressed_key))
            # print()


            pacman.animate(pressed_key, self.walls_collide_list)
            self._handle_teleport(pacman)
            self._handle_berry_collision(pacman)
            self._handle_ghost_collision(pacman)
        self._check_game_state()

        # Rendu des entités
        self.screen.fill("black")
        [wall.update(self.screen) for wall in self.walls.sprites()]
        [berry.update(self.screen) for berry in self.berries.sprites()]
        [ghost.update(self.walls_collide_list) for ghost in self.ghosts.sprites()]
        self.ghosts.draw(self.screen)
        self.player.update()
        self.player.draw(self.screen)

        # Tableau de bord
        if self.game_over and not self.game_over_passed:
            self.display.game_over()
            self.game_over_passed = True
            self.update()
        else:
            self._dashboard()

        if self.game_over and self.game_over_passed and not self.mode_selected:
            self.ask_for_mode()
            self.mode_selected = True
        else:
            self._dashboard()

        # Réinitialisation des positions
        if self.reset_pos and not self.game_over:
            self._reset_positions()

        # Redémarrage du jeu
        if self.game_over and self.mode_selected and self.game_over_passed:
            self.restart_level()