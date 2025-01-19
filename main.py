import pygame, sys, numpy as np
from src.DQN.Agent import Agent
import torch
from src.settings import WIDTH, HEIGHT, NAV_HEIGHT
from src.classes.objects.world import World
from src.settings import get_current_mode

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + NAV_HEIGHT))
pygame.display.set_caption("PacMan")
pygame.display.set_icon(pygame.image.load("assets/pac/right/0.png"))

EPISODES = 1000
BATCH_SIZE = 32

# Classe principale. Gère le jeu
class Main:
    def __init__(self, screen):
        self.screen = screen
        self.FPS = pygame.time.Clock()
    def main(self):
        world = World(self.screen) # Créer un objet World qui sera l'objet de toutes les opérations de la partie
        world.ask_for_mode() # Demande le mode de jeu

        if get_current_mode() == "ai_training":
            self.screen.fill("black")
            world = World  # On initialise le jeu sans l'afficher
            state_size = len(world.get_state(world))  # Définir l'espace d'état
            action_size = 4  # Haut, bas, gauche, droite
            agent = Agent(state_size, action_size)

            for episode in range(EPISODES):
                state = world.get_state()
                done = False
                total_reward = 0

                while not done:
                    action = agent.act(state)
                    print(action)
                    action = agent.ai_move(state)
                    next_state, reward, done = world.step(action)
                    agent.remember(state, action, reward, next_state, done)

                    if len(agent.memory) > BATCH_SIZE:
                        agent.replay(BATCH_SIZE)

                    state = next_state
                    total_reward += reward

                    print(f"Episode {episode + 1}: Score: {total_reward}, Epsilon: {agent.epsilon:.2f}")

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