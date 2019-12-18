import numpy as np
import torch
from torch import nn, optim

LEARNINGRATE = 0.01
NODES = 32

class Reinforce():

    # initialization, takes in statespace size, and action space
    def __init__(self, envStateSize, envActionSpace, learningRate=LEARNINGRATE, nodes=NODES):
        self.inputs = envStateSize
        self.outputs = envActionSpace # we can infer the size of the action space from envActionSpace
        self.actions = np.arange(envActionSpace)
        # we initialize the network. 
        self.network = nn.Sequential(
            nn.Linear(self.inputs, nodes),
            nn.ReLU(),
            nn.Linear(nodes, nodes),
            nn.ReLU(),
            nn.Linear(nodes, self.outputs),
            nn.Softmax(dim=-1)
        )
        # we initialize the optimizer
        self.optimizer = optim.Adam(self.network.parameters(), 
                           lr=learningRate)

    # returns the best action to take in a given state.
    def chooseAction(self, state):
        prob = self.network(torch.FloatTensor(state)).detach().numpy() # took me a while to realize i needed to detach it.
        action = np.random.choice(self.actions, p=prob)
        return action

    # updates the network given a set of states, actions taken, and rewards gained
    def update(self, states, rewards, actions):
        # clear out the optimizer
        self.optimizer.zero_grad()
        sTensor = torch.FloatTensor(states)
        rTensor = torch.FloatTensor(rewards)
        # Actions are used as indices, must be LongTensor
        aTensor = torch.LongTensor(actions)
        
        prediction = lambda state: self.network(torch.FloatTensor(state))
        # Policy Gradient Theorem (kinda)
        logProb = torch.log(prediction(sTensor))
        #selected_logprobs = rTensor * \ logProb[np.arange(len(aTensor)), aTensor]
        loss = -(rTensor * logProb[np.arange(len(aTensor)), aTensor]).mean()
        
        # Calculate gradients
        loss.backward()
        # Apply gradients
        self.optimizer.step()



