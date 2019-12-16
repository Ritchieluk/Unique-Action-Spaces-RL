import numpy as np

AGENT_MOVEMENT_SPEED = 6

class MultiActionEnvironment():


    # initialization function, creates the environment with given size,
    #   given starting enemy health, and given starting locations
    def __init__(self, size=20, enemy_starting_health=15, agent_starting_health=15, agent_type=0, enemy_location=(0,10), agent_location=(10,10)):
        self.enemy_health = enemy_starting_health
        self.agent_health = agent_starting_health
        self.board = np.zeros((size, size))
        self.enemy_location = enemy_location
        self.agent_location = agent_location
        self.turn = 0
        self.agent_movement = AGENT_MOVEMENT_SPEED
        self.in_melee = False
        self.agent_type = agent_type

    
    # step function, env takes given action from agent and adjusts the world accordingly
    def step(self, action):
        # takes in agent action, and adjusts state accordingly
        # if action is not legal, nothing happens
        # returns the next state information (including available actions), the reward for that state, and whether the game has ended
        return


    # get enemy action, determines the enemy's moves after player has finished.
    def enemyAction(self):
        # the enemy moves as close as it can and attempts to attack.
        return


    # resolves actions that the agent chooses, calls specific agent actions if they are chosen
    def resolveActions(self, action):
        return

    # resolve ranged actions
    def resolveRangedActions(self,action):
        return
    # resolve melee actions
    def resolveMeleeActions(self, action):
        return
    # returns the set of actions for a ranged type, given the current state of the board
    def getRangedActions(self):
        """ 
        AC: 14
        HP: 17
        0: Don't Move  \
        1: Move Up      |
        2: Move Right   |
        3: Move Down    | These are same for all types
        4: Move Left    |
        5: Dodge        |
        6: Disengage   / 
        7: Punch (1d20+1, 1 damage)
        8: Attack (1d20 + 5, 1d6+3 damage)
        """
        return
    
    # returns the set of actions for a melee type, given the current state of the board
    def getMeleeActions(self):
        """ 
        AC: 16
        HP: 21
        0: Don't Move  \
        1: Move Up      |
        2: Move Right   |
        3: Move Down    | These are same for all types
        4: Move Left    |
        5: Dodge        |
        6: Disengage   / 
        7: Punch (1d20 + 3, 3 damage)
        8: Attack (1d20 + 5, 1d8+3 damage)
        """
        return

    # print function, displays current board state
    def print(self):
        print("method not implemented")
        return


