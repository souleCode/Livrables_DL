# config.py

GRID_SIZE = 5
START_STATE = (0, 0)                    # Fixe : l'agent commence toujours là
OBSTACLES = [(2, 2)]                    # Tu peux en mettre plusieurs ou aucun

# === RÉCOMPENSES ===
REWARD_GOAL = 10
REWARD_STEP = -1

# === HYPERPARAMÈTRES Q-LEARNING ===
NUM_EPISODES = 30
MAX_STEPS = 100
ALPHA = 0.1
GAMMA = 0.95
EPSILON_START = 0.9
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.995

# === NOUVEAU : GOAL CHANGE À CHAQUE ÉPISODE ===
RANDOM_GOAL_EVERY_EPISODE = True        # ← Mets False si tu veux un goal fixe

# Positions autorisées pour le goal (évite le départ et les obstacles)
VALID_GOAL_POSITIONS = [(x, y)
                        for x in range(GRID_SIZE)
                        for y in range(GRID_SIZE)
                        if (x, y) != START_STATE and (x, y) not in OBSTACLES]