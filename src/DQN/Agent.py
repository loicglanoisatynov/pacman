import numpy as np
import torch

class Agent:
    def __init__(self, state_size, action_size, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01):
        self.state_size = state_size
        self.action_size = action_size
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
    
    def select_action(self, state, policy_net):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.action_size)  # Exploration
        else:
            with torch.no_grad():
                q_values = policy_net(torch.FloatTensor(state))
                return q_values.argmax().item()  # Exploitation
