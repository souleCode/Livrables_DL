# environment.py
import random
from config import *

class GridWorld:
    def __init__(self):
        self.obstacles = set(OBSTACLES)

    def reset(self):
        """Appelé au début de chaque épisode → choisit un nouveau goal si activé"""
        if RANDOM_GOAL_EVERY_EPISODE:
            self.goal = random.choice(VALID_GOAL_POSITIONS)
        else:
            self.goal = (4, 4)  # goal fixe de secours
        return START_STATE

    def step(self, state, action):
        x, y = state
        if action == 0:   y -= 1
        elif action == 1: y += 1
        elif action == 2: x -= 1
        elif action == 3: x += 1

        new_state = (max(0, min(GRID_SIZE-1, x)),
                     max(0, min(GRID_SIZE-1, y)))

        if new_state in self.obstacles:
            return state, REWARD_STEP, False

        reward = REWARD_STEP
        done = False

        if new_state == self.goal:
            reward = REWARD_GOAL
            done = True

        return new_state, reward, done

    def get_goal(self):
        return self.goal