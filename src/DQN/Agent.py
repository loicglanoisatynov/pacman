import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
from collections import deque
from src.DQN.DQN import DQN

class Agent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.epsilon = 1.0  # Exploration (1.0 -> explore, 0.0 -> exploit)
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.gamma = 0.9  # Facteur de récompense future
        self.learning_rate = 0.001
        self.memory = deque(maxlen=2000)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Réseau neuronal DQN
        self.model = DQN(state_size, action_size).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        self.criterion = nn.MSELoss()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, self.action_size - 1)  # Exploration
        state = torch.FloatTensor(state).to(self.device)
        with torch.no_grad():
            return torch.argmax(self.model(state)).item()  # Exploitation

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return

        batch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in batch:
            state = torch.FloatTensor(state).to(self.device)
            next_state = torch.FloatTensor(next_state).to(self.device)

            target = reward
            if not done:
                target += self.gamma * torch.max(self.model(next_state)).item()

            predicted = self.model(state)[action]

            loss = self.criterion(predicted, torch.tensor(target).to(self.device))
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
