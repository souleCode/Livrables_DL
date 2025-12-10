

GRID_SIZE = 5                               # Taille du monde : 5×5

# Positions fixes
START_STATE = (0, 0)                        # L'agent commence toujours ici (coin bas-gauche)
OBSTACLES = [(2, 2)]                        # Liste d'obstacles (noir). Mets [] pour aucun

# Récompenses
REWARD_GOAL = 10                            # Récompense quand on atteint le goal
REWARD_STEP = -1                            # Coût par pas (encourage les chemins courts)

# Hyperparamètres Q-Learning
NUM_EPISODES = 30                           # Nombre d'épisodes d'entraînement
MAX_STEPS = 100                             # Nombre max de pas par épisode
ALPHA = 0.1                                 # Learning rate
GAMMA = 0.95                                # Facteur de discount
EPSILON_START = 0.9
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.995

# ===================================================================
# CHOIX DU COMPORTEMENT DU GOAL (tu choisis un seul mode à la fois)
# ===================================================================

# Mode 1 : Goal aléatoire à chaque épisode
RANDOM_GOAL_EVERY_EPISODE = False

# Mode 2 : Goal déplaçable à la souris pendant l'exécution
MANUAL_GOAL_MODE = True                     # ← Mets True pour activer le clic

# Mode 3 : Goal fixe (valeur par défaut si les deux ci-dessus sont False)
FIXED_GOAL = (4, 4)                         # Utilisé seulement si les deux modes sont désactivés

# Liste des cases où le goal peut apparaître (évite départ + obstacles)
VALID_GOAL_POSITIONS = [
    (x, y)
    for x in range(GRID_SIZE)
    for y in range(GRID_SIZE)
    if (x, y) != START_STATE and (x, y) not in OBSTACLES
]