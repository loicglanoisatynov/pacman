import random
from collections import deque
import torch
import torch.nn as nn
import torch.optim as optim
import pygame
from pacman_env import PacmanEnv
from dqn_model import DQN
from settings import WIDTH, HEIGHT, NAV_HEIGHT

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + NAV_HEIGHT))
env = PacmanEnv(screen)

# Initialisation de l'environnement du DQN
input_dim = env.observation_space.shape[0]
output_dim = env.action_space.n
model = DQN(input_dim=input_dim, output_dim=output_dim)
optimizer = optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.MSELoss()
gamma = 0.99
epsilon = 1.0
epsilon_decay = 0.995
epsilon_min = 0.1
memory = deque(maxlen=10000)
batch_size = 64

clock = pygame.time.Clock()

# Entraînement
for episode in range(2):
    state = env.reset()
    total_reward = 0
    done = False

    while not done:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Choisir une action (exploration/exploitation)
        if random.random() < epsilon:
            action = env.action_space.sample()
        else:
            with torch.no_grad():
                action = torch.argmax(model(torch.tensor(state, dtype=torch.float32))).item()

        # Effectuer une action
        next_state, reward, done, _ = env.step(action)
        memory.append((state, action, reward, next_state, done))
        state = next_state
        total_reward += reward

        # Apprentissage par mini-batch
        if len(memory) >= batch_size:
            batch = random.sample(memory, batch_size)
            states, actions, rewards, next_states, dones = zip(*batch)

            states = torch.tensor(states, dtype=torch.float32)
            actions = torch.tensor(actions, dtype=torch.long)
            rewards = torch.tensor(rewards, dtype=torch.float32)
            next_states = torch.tensor(next_states, dtype=torch.float32)
            dones = torch.tensor(dones, dtype=torch.float32)

            q_values = model(states).gather(1, actions.unsqueeze(1)).squeeze(1)
            with torch.no_grad():
                max_next_q_values = model(next_states).max(1)[0]
                target_q_values = rewards + gamma * max_next_q_values * (1 - dones)

            loss = loss_fn(q_values, target_q_values)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        # Afficher les progrès
       # env.render()
        #clock.tick(60)
        

    epsilon = max(epsilon * epsilon_decay, epsilon_min)
    print(f"Épisode {episode + 1}: Récompense totale = {total_reward}")

# Sauvegarder le modèle
torch.save(model.state_dict(), "dqn_model.pth")
