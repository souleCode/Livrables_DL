# agent.py
import random
import numpy as np
from config import *

class QLearningAgent:
    def __init__(self):
        self.Q = {(i,j): [0.0]*4 for i in range(GRID_SIZE) for j in range(GRID_SIZE)}
        self.epsilon = EPSILON_START

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, 3)
        return int(np.argmax(self.Q[state]))

    def update(self, s, a, r, s_next, done):
        best_next = max(self.Q[s_next])
        target = r if done else r + GAMMA * best_next
        self.Q[s][a] += ALPHA * (target - self.Q[s][a])

    def decay_epsilon(self):
        self.epsilon = max(EPSILON_MIN, self.epsilon * EPSILON_DECAY)