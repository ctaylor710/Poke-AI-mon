"""
DQN Implementation

"""


import torch
import torch.nn.functional as F
from torch.optim import Adam
from models import QNetwork
import numpy as np

# TODO 2. The DQN function is to use the predicted human action and current state to return the robot action that maximize the Q value
# Since we are using both state and predicted human action for the DQN
# Thus the DQN input size should be the stateSize + predictedActionSize

class DQN(object):
    def __init__(self, state_size, HA_size, action_size):

        self.state_size = state_size + HA_size
        self.action_size = action_size
        self.gamma = 0.99
        self.tau = 1e-3
        self.LR = 1e-4  # learning rate
        self.hidden_dim = 752

        # Q-Network
        self.qnetwork_local = QNetwork(self.state_size, self.action_size, self.hidden_dim)
        self.qnetwork_target = QNetwork(self.state_size, self.action_size, self.hidden_dim)
        self.optimizer = Adam(self.qnetwork_local.parameters(), lr=self.LR)

    def Robot_action(self, state, HA):
        # take action with highest Q value
        state = state + HA
        state = torch.FloatTensor(state)
        Q_state = self.qnetwork_local(state).detach().numpy()
        return np.argmax(Q_state)

    def Robot_action_N(self, state, HA, N):
        state = state + HA
        state = torch.FloatTensor(state)
        Q_state = self.qnetwork_local(state).detach().numpy()
        actions = []; rewards = []
        for i in range(N):
            actions.append(np.argmax(Q_state))
            rewards.append(np.max(Q_state))
            Q_state = np.delete(Q_state, [np.argmax(Q_state)])

        return actions, rewards

    # train the Q-functions
    def update_parameters(self, memory, batch_size):

        # sample a batch from memory
        state, action, reward, next_state, done = memory.sample(batch_size)
        # be cautious that the state is actually going to be the state + HA
        # and the next_state is going to be the next_state + next_HA

        # convert to torch tensors
        states = torch.FloatTensor(state)
        actions = torch.FloatTensor(action).unsqueeze(1).long()
        rewards = torch.FloatTensor(reward).unsqueeze(1)
        next_states = torch.FloatTensor(next_state)
        dones = torch.FloatTensor(done).unsqueeze(1)

        # Get max predicted Q values (for next states) from target model
        Q_targets_next = self.qnetwork_target(next_states).detach().max(1)[0].unsqueeze(1)
        # Compute Q targets for current states
        Q_targets = rewards + self.gamma * Q_targets_next * (1.0 - dones)

        # Get expected Q values from local model
        # print(len(states))
        # print(len(actions))
        Q_expected = self.qnetwork_local(states).gather(1, actions)

        # Compute loss
        loss = F.mse_loss(Q_expected, Q_targets)
        # Minimize the loss
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # update target network
        self.soft_update(self.qnetwork_local, self.qnetwork_target, self.tau)

        return loss.item()

    # helper function for updating the weights of Q_target (Q')
    def soft_update(self, local_model, target_model, tau):
        # θ_target = τ*θ_local + (1 - τ)*θ_target
        for target_param, local_param in zip(target_model.parameters(), local_model.parameters()):
            target_param.data.copy_(tau*local_param.data + (1.0-tau)*target_param.data)
