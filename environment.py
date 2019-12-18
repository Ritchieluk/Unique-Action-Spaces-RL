import numpy as np
import random as rand

AGENT_MOVEMENT_SPEED = 6
ENEMY_AC = 13

class MultiActionEnvironment():


    # initialization function, creates the environment with given size,
    #   given starting enemy health, and given starting locations
    def __init__(self, size=20, enemy_starting_health=15, agent_starting_health=15, agent_type=0, enemy_location=[0,10], agent_location=[10,10]):
        self.enemy_health = enemy_starting_health
        self.enemy_starting_health = enemy_starting_health
        self.agent_health = agent_starting_health
        self.agent_starting_health = agent_starting_health
        self.enemy_AC = ENEMY_AC
        self.agent_AC = 16 if agent_type == 0 else 14
        self.board = np.zeros((size, size))
        self.enemy_location = enemy_location
        self.enemy_starting_location = enemy_location
        self.agent_location = agent_location
        self.agent_starting_location = agent_location
        self.turn = 0
        self.agent_movement = AGENT_MOVEMENT_SPEED
        self.in_melee = False
        self.acted = False
        self.agent_type = agent_type
        self.current_reward = 0
        self.dodging = False
        self.disengaged = False
        self.observation_size = 14
        self.action_size = 9
        self.render = False

    def reset(self):
        self.enemy_health = self.enemy_starting_health
        self.agent_health = self.agent_starting_health
        self.enemy_location = self.enemy_starting_location
        self.agent_location = self.agent_starting_location
        self.turn = 0
        self.agent_movement = AGENT_MOVEMENT_SPEED
        self.in_melee = False
        self.acted = False
        self.current_reward = 0
        self.dodging = False
        self.disengaged = False
        damaged = 1 if self.enemy_health <= self.enemy_starting_health/2 else 0
        observerations = []
        observerations.extend(self.agent_location)
        observerations.extend(self.getActions())
        observerations.extend([self.enemyDistance(), self.agent_health, damaged])
        self.current_reward = 0
        return observerations

    
    # step function, env takes given action from agent and adjusts the world accordingly
    def step(self, action):
        # takes in agent action, and adjusts state accordingly
        # if action is not legal, nothing happens
        # returns the next state information (including available actions and distance to enemy), the reward for that state, and whether the game has ended
        self.resolveActions(action)
        damaged = 1 if self.enemy_health <= self.enemy_starting_health/2 else 0
        observerations = []
        observerations.extend(self.agent_location)
        observerations.extend(self.getActions())
        observerations.extend([self.enemyDistance(), self.agent_health, damaged])
        done = False
        if self.agent_health <= 0:
            self.current_reward -= 10
            done = True
        elif self.enemy_health <= 0:
            self.current_reward += 10
            done = True
        rewards = self.current_reward
        self.current_reward = 0
        if self.render:
            print("Agent Health: {h}    Enemy Health: {e}".format(h=self.agent_health, e=self.enemy_health))
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
        self.agent_movement = AGENT_MOVEMENT_SPEED

    # enemy attack resolves
    def resolveEnemyAttack(self):
        attackRoll = rand.randint(1,20) + 5
        disadvantageRoll = 20
        if self.dodging:
            disadvantageRoll = rand.randint(1,20) + 5
        attackRoll = min([attackRoll, disadvantageRoll])
        if self.render:
            print("Enemy Attacks, Rolls: {}".format(attackRoll))
        if attackRoll > self.agent_AC:
            damageRoll = rand.randint(1,12)+3
            if self.render:
                print("Enemy Deals {} damage".format(damageRoll))
            self.agent_health -= damageRoll
            self.current_reward -= 1
        self.endEnemyTurn()
        return

    # resolves actions that the agent chooses, calls specific agent actions if they are chosen
    def resolveActions(self, action):
        # this is disgusting, I had no idea python didn't have a switch statement
        if action == 0:
            if self.render:
                print("Passing Turn")
            self.turn = 1
            self.enemyAction()
            return
        if action == 1:
            if self.render:
                print("Moving Up")
            self.agent_movement -= 1
            if self.agent_location[1]<len(self.board[self.agent_location[0]])-1 and self.agent_movement >= 0:
                self.agent_location[1] += 1
                if self.enemyDistance() < 2:
                    self.in_melee = True
                else:
                    if self.in_melee and not self.disengaged:
                        self.resolveEnemyAttack()
                        self.in_melee = False
                return
            else:
                self.current_reward -= 1
                self.turn = 1
                return
        if action == 2:
            if self.render:
                print("Moving Right")
            self.agent_movement -= 1
            if self.agent_location[0]<len(self.board)-1 and self.agent_movement >= 0:
                self.agent_location[0] += 1
                if self.enemyDistance() < 2:
                    self.in_melee = True
                else:
                    if self.in_melee and not self.disengaged:
                        self.resolveEnemyAttack()
                        self.in_melee = False
                return
            else:
                self.current_reward -= 1
                self.turn = 1
                return
        if action == 3:
            if self.render:
                print("Moving Down")
            self.agent_movement -= 1
            if self.agent_location[1]>0 and self.agent_movement >= 0:
                self.agent_location[1] -= 1
                if self.enemyDistance() < 2:
                    self.in_melee = True
                else:
                    if self.in_melee and not self.disengaged:
                        self.resolveEnemyAttack()
                        self.in_melee = False
                return
            else:
                self.current_reward -= 1
                self.turn = 1
                return 
        if action == 4:
            if self.render:
                print("Moving Left")
            self.agent_movement -= 1
            if self.agent_location[0]>0 and self.agent_movement >= 0:
                self.agent_location[0] -= 1
                if self.enemyDistance() < 2:
                    self.in_melee = True
                else:
                    if self.in_melee and not self.disengaged:
                        self.resolveEnemyAttack()
                        self.in_melee = False
                return
            else:
                self.current_reward -= 1
                self.turn = 1
                return
        if action == 5:
            if self.render:
                print("Disengaging")
            if not self.acted:
                self.acted = True
                self.disengaged = True
            else:
                self.current_reward -= 1
                self.turn = 1
            
        if action == 6:
            if self.render:
                print("Dodging")
            if not self.acted:
                self.acted = True
                self.dodging = True
            else:
                self.current_reward -= 1
                self.turn = 1
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
        if not self.acted:
            self.acted = True
            if action == 7:
                if self.render:
                    print("Punching")
                if self.enemyDistance()<2:
                    attackRoll = rand.randint(1,20) + 1
                    if attackRoll >= self.enemy_AC:
                        damageRoll = 1
                        self.enemy_health -= damageRoll
                        self.current_reward += damageRoll
                else:
                    self.turn = 1
                    self.current_reward -= 1
            if action == 8:
                if self.render:
                    print("Attacking")
                # resolve attack
                attackRoll = rand.randint(1,20) + 5
                disadvantageRoll = 20
                if self.enemyDistance()<2:
                    disadvantageRoll = rand.randint(1,20) + 5
                attackRoll = min([attackRoll, disadvantageRoll])
                if self.render:
                    print("Rolled: {}".format(attackRoll))
                if attackRoll >= self.enemy_AC:
                    damageRoll = rand.randint(1,6)+3
                    if self.render:
                        print("Damage: {}".format(damageRoll))
                    self.enemy_health -= damageRoll
                    self.current_reward += damageRoll
        else:
            self.turn = 1
            self.current_reward -= 1
        

    # resolve melee actions
    def resolveMeleeActions(self, action):
        if not self.acted:
            self.acted = True
            if action == 7:
                if self.render:
                    print("Punching")
                # resolve punch
                if self.enemyDistance()<2:
                    attackRoll = rand.randint(1,20) + 3
                    if attackRoll >= self.enemy_AC:
                        damageRoll = 3
                        self.enemy_health -= damageRoll
                        self.current_reward += damageRoll
                else:
                    self.turn = 1
                    self.current_reward -= 1
            if action == 8:
                if self.render:
                    print("Attacking")
                # resolve attack
                if self.enemyDistance()<2:
                    attackRoll = rand.randint(1,20) + 5
                    if attackRoll >= self.enemy_AC:
                        damageRoll = rand.randint(1,12)+3
                        self.enemy_health -= damageRoll
                        self.current_reward += damageRoll
                else:
                    self.turn = 1
                    self.current_reward -= 1
        else:
            self.turn = 1
            self.current_reward -= 1

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
        if len(actions) < 9:
            for _ in range(9-len(actions)):
                actions.append(0)
        return actions

    # returns distance between agent and enemy
    def enemyDistance(self, agentloc=-1, enemyloc=-1):
        if agentloc == -1 or enemyloc == -1:
            agentloc = self.agent_location
            enemyloc = self.enemy_location 
        return ((agentloc[0] - enemyloc[0])**2 + (agentloc[1] - enemyloc[1])**2)**.5


    # print function, displays current board state
    def print(self):
        for i in range(len(self.board)):
            line = ""
            if i == 0 or i == len(self.board)-1:
                line += "+"
            else:
                line += "|"
            for j in range(len(self.board[0])):
                if i == self.agent_location[1] and j==self.agent_location[0]:
                    line+= 'A'
                elif i == self.enemy_location[1] and j==self.enemy_location[0]:
                    line+='E'
                else:
                    line+='-'
            if i == 0 or i == len(self.board)-1:
                line += "+"
            else:
                line += "|"
            print(line)


