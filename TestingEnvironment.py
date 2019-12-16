import gym
import matplotlib.pyplot as plt
import numpy as np
import random
from reinforceAgent import Reinforce
from torch import optim

BATCHSIZE = 10

def calculateReturn(rewards, discount=0.9):
    arr = [discount**reward * rewards[reward] for reward in range(len(rewards))]
    discounted = np.array(arr)
    discounted = discounted[::-1].cumsum()[::-1]
    return discounted - discounted.mean()

env = gym.make('CartPole-v0')



agent = Reinforce(env.observation_space.shape[0], env.action_space.n)

totalReward = []
bRewards = []
bActionsTaken = []
bStatesVisted = []
batchCounter = 1

for episode in range(2000):
    currState = env.reset()
    statesVisited = []
    episodeRewards = []
    actionsTaken = []
    done = False

    while not done:
        #env.render()
        nextAction = agent.chooseAction(currState)
        nextState, reward, done, info = env.step(nextAction)
        statesVisited.append(currState)
        episodeRewards.append(reward)
        actionsTaken.append(nextAction)
        currState = nextState

        # episode ends, we add data to the batch and update counter
        if done:
            bRewards.extend(calculateReturn(episodeRewards))
            bStatesVisted.extend(statesVisited)
            bActionsTaken.extend(actionsTaken)
            batchCounter += 1
            totalReward.append(sum(episodeRewards))

            # if we have reached batch size, its time for the BIG UPDATE
            if batchCounter == BATCHSIZE:

                # call agent backprop function and pass in the batch info
                agent.update(bStatesVisted, bRewards, bActionsTaken)
                # reset batch info
                bRewards = []
                bActionsTaken = []
                bStatesVisted = []
                batchCounter = 1

                print("\rEp: {} Average of last 10: {:.2f}".format(
                    episode + 1, np.mean(totalReward[-10:])), end="")
    #print(batchCounter)


window = 10
smoothed_rewards = [np.mean(totalReward[i-window:i+1]) if i > window 
                    else np.mean(totalReward[:i+1]) for i in range(len(totalReward))]

plt.figure(figsize=(12,8))
plt.plot(totalReward)
plt.plot(smoothed_rewards)
plt.ylabel('Total Rewards')
plt.xlabel('Episodes')
plt.show()

env = gym.make('CartPole-v0')
currState = env.reset()
done = False
while not done:
    env.render()
    nextAction = agent.chooseAction(currState)
    nextState, reward, done, info = env.step(nextAction)
    currState = nextState
    
env.close()