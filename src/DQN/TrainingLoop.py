import DQN
import torch

# Hyperparamètres
gamma = 0.99
batch_size = 64
lr = 1e-3
memory_capacity = 10000

# Initialisation
state_size = 4
# <dimension de l'état>  # Ex : 4 pour vecteurs, ou hauteur*largeur pour une image
action_size = 4
# <nombre d'actions possibles>  # Ex : 4 pour haut, bas, gauche, droite

policy_net = DQN(state_size, action_size)
target_net = DQN(state_size, action_size)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

optimizer = torch.optim.Adam(policy_net.parameters(), lr=lr)
memory = ReplayMemory(memory_capacity)
agent = Agent(state_size, action_size)

# Boucle principale
for episode in range(num_episodes):
    state = env.reset()  # Réinitialiser l'environnement
    total_reward = 0
    for t in range(max_timesteps):
        # Choisir une action
        action = agent.select_action(state, policy_net)
        
        # Effectuer l'action
        next_state, reward, done, _ = env.step(action)
        total_reward += reward
        
        # Stocker la transition
        memory.push((state, action, reward, next_state, done))
        state = next_state
        
        # Entraîner le modèle si assez de transitions
        if len(memory) > batch_size:
            transitions = memory.sample(batch_size)
            batch = list(zip(*transitions))  # Décompose en (states, actions, rewards, ...)
            
            states = torch.FloatTensor(batch[0])
            actions = torch.LongTensor(batch[1])
            rewards = torch.FloatTensor(batch[2])
            next_states = torch.FloatTensor(batch[3])
            dones = torch.FloatTensor(batch[4])
            
            # Calcul des Q-valeurs cibles
            current_q = policy_net(states).gather(1, actions.unsqueeze(1)).squeeze(1)
            next_q = target_net(next_states).max(1)[0]
            target_q = rewards + gamma * next_q * (1 - dones)
            
            # Optimisation
            loss = nn.MSELoss()(current_q, target_q)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
        # Mettre fin si terminé
        if done:
            break
    
    # Mise à jour de l'exploration
    agent.epsilon = max(agent.epsilon * agent.epsilon_decay, agent.epsilon_min)
    
    # Mettre à jour le réseau cible
    if episode % target_update == 0:
        target_net.load_state_dict(policy_net.state_dict())
    
    print(f"Épisode {episode}, Récompense Totale: {total_reward}")
