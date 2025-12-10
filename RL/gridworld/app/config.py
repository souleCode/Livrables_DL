# config.py

GRID_SIZE = 5
START_STATE = (0, 0)       # coin en bas à gauche
GOAL_STATE = (2, 2)        # coin en haut à droite
OBSTACLES = [(2, 1)]       # UN SEUL obstacle

ACTIONS = ['down', 'up', 'left', 'right']  # 0,1,2,3

# Hyperparamètres
NUM_EPISODES = 30
MAX_STEPS = 100
ALPHA = 0.1
GAMMA = 0.90
EPSILON_START = 0.9
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.995

# Récompenses
REWARD_GOAL = 10
REWARD_STEP = -1