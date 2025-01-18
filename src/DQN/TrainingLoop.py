import numpy as np
from src.DQN.Agent import Agent
from src.classes.objects.world import World
import torch

EPISODES = 1000
BATCH_SIZE = 32

def train():
    world = World(screen=None)  # On initialise le jeu sans l'afficher
    state_size = len(world.get_state())  # Définir l'espace d'état
    action_size = 4  # Haut, bas, gauche, droite
    agent = Agent(state_size, action_size)

    for episode in range(EPISODES):
        state = world.get_state()
        done = False
        total_reward = 0

        while not done:
            action = agent.act(state)
            next_state, reward, done = world.step(action)
            agent.remember(state, action, reward, next_state, done)

            if len(agent.memory) > BATCH_SIZE:
                agent.replay(BATCH_SIZE)

            state = next_state
            total_reward += reward

        print(f"Episode {episode + 1}: Score: {total_reward}, Epsilon: {agent.epsilon:.2f}")

if __name__ == "__main__":
    train()
