import gym
import matplotlib.pyplot as plt
import numpy as np
import random
from reinforceAgent import Reinforce
from torch import optim
from environment import MultiActionEnvironment

BATCHSIZE = 10

def calculateReturn(rewards, discount=0.9):
    arr = [discount**reward * rewards[reward] for reward in range(len(rewards))]
    discounted = np.array(arr)
    discounted = discounted[::-1].cumsum()[::-1]
    return discounted - discounted.mean()

# Melee Character
#env = MultiActionEnvironment(size=20, enemy_starting_health=13, agent_starting_health=21, agent_type=0, enemy_location=[0,10], agent_location=[10,10])
# Ranged Character
env = MultiActionEnvironment(size=20, enemy_starting_health=13, agent_starting_health=18, agent_type=1, enemy_location=[0,10], agent_location=[10,10])


agent = Reinforce(env.observation_size, env.action_size)

totalReward = []
bRewards = []
bActionsTaken = []
bStatesVisted = []
batchCounter = 1

for episode in range(500):
    currState = env.reset()
    statesVisited = []
    episodeRewards = []
    actionsTaken = []
    done = False

    while not done:
        #env.render()
        nextAction = agent.chooseAction(currState)
        nextState, reward, done = env.step(nextAction)
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


currState = env.reset()
done = False
while not done:
    env.render = True
    env.print()
    nextAction = agent.chooseAction(currState)
    nextState, reward, done = env.step(nextAction)
    currState = nextState