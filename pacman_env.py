import gym
import numpy as np
import pygame
from world import World
from settings import WIDTH, HEIGHT, NAV_HEIGHT

class PacmanEnv(gym.Env):
    def __init__(self, screen):
        super(PacmanEnv, self).__init__()
        self.world = World(screen)
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(5,), dtype=np.float32)
        self.action_space = gym.spaces.Discrete(4)

    def reset(self):
        self.world.restart_level()
        return self._get_state()

    def _get_state(self):
        pacman = self.world.player.sprite
        return np.array([
            pacman.rect.x, pacman.rect.y,
            len(self.world.berries), pacman.life, pacman.pac_score
        ], dtype=np.float32)

    def step(self, action):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        pacman = self.world.player.sprite
        pacman.direction = directions[action]

        self.world.update()
        reward = 0
        if len(self.world.berries) == 0:
            reward += 100
        if pacman.life <= 0:
            reward -= 100

        done = self.world.game_over or len(self.world.berries) == 0
        state = self._get_state()
        return state, reward, done, {}

    def render(self):
        self.world.update()
        pygame.display.update()
