# Unique-Action-Spaces-RL
#### By Luke Ritchie
Examining the effects different action spaces have on RL agent resulting policies. Final Project for CS585-Sequential Decision Making.

## Running the Project
runs ranged action space
> python .\testing.py

runs melee action space
> python .\TestingEnvironment.py

After they run, closing the graph will cause the latest model to run a simulated combat and print into the terminal.

## Results
Ultimately they didn't create policies like I predicted, which ended up being more interesting to me. The melee agent tended to wait for the enemy to come to it, which I believe was due to the penalties for illegal moves. Rather than risk an illegal move, it simply stayed where it was...safe.

The ranged agent had no desire to strafe away from its enemy even though it easily could have done so. My guess is the agent always had access to a steady reward stream, attacking then passing turn, which on occassion even prevented it from taking any damage if its attacks all landed. My hunch is it relied on this approach and never learned the benefit of running away. It could also be the case that on a few occassion it found that running away meant the possibility of opportunity attacks, which would be negative reward, whereas attacking with a low-likelihood of success in melee range is at least non-negative reward.

All in all...mixed success I would say. I will need to work on my implementation of the environment to make it cleaner, and double check effects like melee range and opportunity attacks etc.

## Worth noting
- The melee character will occasionally get caught in a local minimum of around -12 average reward over its lifespan. I believe this is because it learns quickly that many of its actions penalize it because it is not in range yet, and does not learn they do not penalize once it is in range. 
- Overall the reward structure needs rethinking I believe.
- The self.in_melee boolean was largely phased out in favor of self.enemyDistance()
- Technically speaking I created nothing to prevent the agents from occupying the same space. This was not intentional though I don't believe it had adverse affects.