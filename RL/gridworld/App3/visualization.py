# visualization.py
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from config import *
import numpy as np

def draw_grid(ax):
    ax.clear()
    ax.set_xlim(0, GRID_SIZE)
    ax.set_ylim(0, GRID_SIZE)
    ax.set_xticks(range(GRID_SIZE + 1))
    ax.set_yticks(range(GRID_SIZE + 1))
    ax.grid(True)
    ax.invert_yaxis()

    # Goal
    ax.add_patch(patches.Rectangle((4,4), 1, 1, color='lime', alpha=0.8))
    ax.text(4.5, 4.5, '+10', ha='center', va='center', fontsize=14, fontweight='bold')

    # Obstacle
    ax.add_patch(patches.Rectangle((2,2), 1, 1, color='black'))
    ax.text(2.5, 2.5, 'X', ha='center', va='center', color='white', fontsize=16, fontweight='bold')

def draw_agent(ax, state):
    ax.add_patch(patches.Circle((state[0]+0.5, state[1]+0.5), 0.3, color='red', zorder=10))

def show_final_values(Q):
    V = np.zeros((GRID_SIZE, GRID_SIZE))
    for (x,y), qvals in Q.items():
        V[y, x] = max(qvals)

    plt.figure(figsize=(6,6))
    plt.imshow(V, cmap='viridis')
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            plt.text(j, i, f"{V[i,j]:.1f}", ha='center', va='center',
                     color='white', fontweight='bold', fontsize=10)
    plt.colorbar(label='Valeur d\'état')
    plt.title('Valeurs finales apprises par Q-Learning')
    plt.show()