import numpy as np
import random as rand

AGENT_MOVEMENT_SPEED = 6
ENEMY_AC = 13

class MultiActionEnvironment():


    # initialization function, creates the environment with given size,
    #   given starting enemy health, and given starting locations
    def __init__(self, size=20, enemy_starting_health=15, agent_starting_health=15, agent_type=0, enemy_location=(0,10), agent_location=(10,10)):
        self.enemy_health = enemy_starting_health
        self.enemy_starting_health = enemy_starting_health
        self.agent_health = agent_starting_health
        self.enemy_AC = ENEMY_AC
        self.agent_AC = 16 if agent_type == 0 else 14
        self.board = np.zeros((size, size))
        self.enemy_location = enemy_location
        self.agent_location = agent_location
        self.turn = 0
        self.agent_movement = AGENT_MOVEMENT_SPEED
        self.in_melee = False
        self.acted = False
        self.agent_type = agent_type
        self.current_reward = 0
        self.dodging = False
        self.disengaged = False

    
    # step function, env takes given action from agent and adjusts the world accordingly
    def step(self, action):
        # takes in agent action, and adjusts state accordingly
        # if action is not legal, nothing happens
        # returns the next state information (including available actions and distance to enemy), the reward for that state, and whether the game has ended
        self.resolveActions(action)
        damaged = 1 if self.enemy_health <= self.enemy_starting_health/2 else 0
        observerations = [self.agent_location, self.getActions(), self.enemyDistance(), self.agent_health, damaged]
        done = False
        if self.agent_health <= 0:
            self.current_reward -= 10
            done = True
        elif self.enemy_health <= 0:
            self.current_reward += 10
            done = True
        rewards = self.current_reward
        self.current_reward = 0
        return (observerations, rewards, done)


    # get enemy action, determines the enemy's moves after player has finished.
    def enemyAction(self):
        # the enemy moves as close as it can and attempts to attack.
        speed = AGENT_MOVEMENT_SPEED
        if self.in_melee:
            self.resolveEnemyAttack()
        else:
            while speed > 0:
                currDist = self.enemyDistance()
                if currDist < 2:
                    self.in_melee = True
                    self.resolveEnemyAttack()
                    speed = 0
                dists = []
                up = (self.enemy_location[0], self.enemy_location[1]+1)
                right = (self.enemy_location[0] + 1, self.enemy_location[1])
                down = (self.enemy_location[0], self.enemy_location[1]-1)
                left = (self.enemy_location[0] - 1, self.enemy_location[1])
                actions = [up, right, down, left]
                dists.append(self.enemyDistance(self.agent_location, up))
                dists.append(self.enemyDistance(self.agent_location, right))
                dists.append(self.enemyDistance(self.agent_location, down))
                dists.append(self.enemyDistance(self.agent_location, left))
                self.enemy_location = actions[dists.index(min(dists))]
                speed -= 1
            self.endEnemyTurn()
        return

    def endEnemyTurn(self):
        self.turn = 0
        self.dodging = False
        self.disengaged = False
        self.acted = False

    # enemy attack resolves
    def resolveEnemyAttack(self):
        attackRoll = rand.randint(1,20) + 5
        disadvantageRoll = 20
        if self.dodging:
            disadvantageRoll = rand.randint(1,20) + 5
        attackRoll = min([attackRoll, disadvantageRoll])
        if attackRoll > self.agent_AC:
            damageRoll = rand.randint(1,12)+3
            self.agent_health -= damageRoll
        self.endEnemyTurn()
        return

    # resolves actions that the agent chooses, calls specific agent actions if they are chosen
    def resolveActions(self, action):
        # this is disgusting, I had no idea python didn't have a switch statement
        if action == 0:
            self.turn = 1
            self.enemyAction()
            return
        if action == 1:
            self.agent_movement -= 1
            if self.agent_location[1]<=len(self.board[self.agent_location[0]])-1:
                self.agent_location[1] += 1
                if self.enemyDistance() < 2:
                    self.in_melee = True
                else:
                    if self.in_melee and not self.disengaged:
                        self.resolveEnemyAttack()
                        self.in_melee = False
                return
            else:
                print("Reached map edge")
                self.current_reward -= 1
                self.turn = 1
                return
        if action == 2:
            self.agent_movement -= 1
            if self.agent_location[0]<=len(self.board)-1:
                self.agent_location[0] += 1
                if self.enemyDistance() < 2:
                    self.in_melee = True
                else:
                    if self.in_melee and not self.disengaged:
                        self.resolveEnemyAttack()
                        self.in_melee = False
                return
            else:
                print("Reached map edge")
                self.current_reward -= 1
                self.turn = 1
                return
        if action == 3:
            self.agent_movement -= 1
            if self.agent_location[1]>=0:
                self.agent_location[1] -= 1
                if self.enemyDistance() < 2:
                    self.in_melee = True
                else:
                    if self.in_melee and not self.disengaged:
                        self.resolveEnemyAttack()
                        self.in_melee = False
                return
            else:
                print("Reached map edge")
                self.current_reward -= 1
                self.turn = 1
                return 
        if action == 4:
            self.agent_movement -= 1
            if self.agent_location[0]>=0:
                self.agent_location[0] -= 1
                if self.enemyDistance() < 2:
                    self.in_melee = True
                else:
                    if self.in_melee and not self.disengaged:
                        self.resolveEnemyAttack()
                        self.in_melee = False
                return
            else:
                print("Reached map edge")
                self.current_reward -= 1
                self.turn = 1
                return
        if action == 5:
            self.acted = True
            self.disengaged = True
            return
        if action == 6:
            self.acted = True
            self.dodging = True
            return
        if action == 7 or action == 8:
            if self.agent_type == 0:
                return self.resolveMeleeActions(action)
            elif self.agent_type == 1:
                return self.resolveRangedActions(action)
            else:
                return "Unknown Agent Type"
        return "Unexpected Action Taken"

    # resolve ranged actions
    def resolveRangedActions(self,action):
        self.acted = True
        if action == 7:
            if self.in_melee:
                attackRoll = rand.randint(1,20) + 1
                if attackRoll > self.enemy_AC:
                    damageRoll = 1
                    self.enemy_health -= damageRoll
                    self.current_reward += damageRoll
            else:
                self.turn = 1
                self.current_reward -= 1
        if action == 8:
            # resolve attack
            attackRoll = rand.randint(1,20) + 5
            disadvantageRoll = 20
            if self.in_melee:
                disadvantageRoll = rand.randint(1,20) + 5
            attackRoll = min([attackRoll, disadvantageRoll])
            if attackRoll > self.enemy_AC:
                damageRoll = rand.randint(1,6)+3
                self.enemy_health -= damageRoll
                self.current_reward += damageRoll
        return

    # resolve melee actions
    def resolveMeleeActions(self, action):
        self.acted = True
        if action == 7:
            # resolve punch
            if self.in_melee:
                attackRoll = rand.randint(1,20) + 3
                if attackRoll > self.enemy_AC:
                    damageRoll = 3
                    self.enemy_health -= damageRoll
                    self.current_reward += damageRoll
            else:
                self.turn = 1
                self.current_reward -= 1
        if action == 8:
            # resolve attack
            if self.in_melee:
                attackRoll = rand.randint(1,20) + 5
                if attackRoll > self.enemy_AC:
                    damageRoll = rand.randint(1,8)+3
                    self.enemy_health -= damageRoll
                    self.current_reward += damageRoll
            else:
                self.turn = 1
                self.current_reward -= 1
        return

    # returns the set of available actions, given the current state of the board
    def getActions(self):
        """ 
        Ranged AC: 14  HP: 17
        Melee  AC: 16  HP: 21
        0: Pass Turn   \
        1: Move Up      |
        2: Move Right   |
        3: Move Down    | These are same for all types
        4: Move Left    |
        5: Dodge        |
        6: Disengage   / 
        7 (ranged): Punch (1d20+1, 1 damage)
        8 (ranged): Attack (1d20 + 5, 1d6+3 damage) Ranged
        7 (melee): Punch (1d20+3, 3 damage)
        8 (melee): Attack (1d20+5, 1d8+3 damage)
        """
        actions = [0]
        if self.acted and self.agent_movement == 0:
            return actions
        if self.agent_movement > 0:
            actions.extend([1,2,3,4])
        if not self.acted:
            actions.extend([5,6])
            if self.in_melee:
                actions.append(7)
                if self.agent_type == 0:
                    actions.append(8)
            if self.agent_type == 1:
                actions.append(7)
        return actions

    # returns distance between agent and enemy
    def enemyDistance(self, agentloc=self.agent_location, enemyloc=self.enemy_location):
        return ((agentloc[0] - enemyloc[0])**2 + (agentloc[1] - enemyloc[1])**2)**.5


    # print function, displays current board state
    def print(self):
        print("method not implemented")
        return


