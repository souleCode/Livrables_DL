# environment.py
from config import *

class GridWorld:
    def __init__(self):
        self.obstacles = set(OBSTACLES)
        self.goal = GOAL_STATE

    def step(self, state, action):
        x, y = state

        # Mouvements
        if action == 0:   y -= 1   # down
        elif action == 1: y += 1   # up
        elif action == 2: x -= 1   # left
        elif action == 3: x += 1   # right

        # Bornes du monde
        new_state = (
            max(0, min(GRID_SIZE - 1, x)),
            max(0, min(GRID_SIZE - 1, y))
        )

        # Si on tape l'obstacle → on reste où on est
        if new_state in self.obstacles:
            return state, REWARD_STEP, False

        reward = REWARD_STEP
        done = False

        if new_state == self.goal:
            reward = REWARD_GOAL
            done = True

        return new_state, reward, done