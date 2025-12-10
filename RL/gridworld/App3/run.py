# run.py
import matplotlib.pyplot as plt
import numpy as np
from environment import GridWorld
from agent import QLearningAgent
from visualization import draw_grid, draw_agent, show_final_values
from config import *

# Variable globale pour le goal manuel
manual_goal = None

def on_mouse_click(event):
    """Callback appelée quand tu cliques dans la fenêtre"""
    if event.inaxes is None or event.button != 1:  # clic gauche seulement
        return

    # Convertir les coordonnées du clic en case du grid (0..4, 0..4)
    x = int(event.xdata)
    y = int(event.ydata)

    # Empêcher de placer le goal sur le départ ou sur l’obstacle
    if (x, y) == START_STATE:
        print("Impossible de placer le goal sur la case de départ !")
        return
    if (x, y) in OBSTACLES:
        print("Impossible de placer le goal sur un obstacle !")
        return

    global manual_goal
    manual_goal = (x, y)
    print(f"\nGOAL DÉPLACÉ MANUELLEMENT → {manual_goal}")

# ===================================================================
def main():
    global manual_goal

    env = GridWorld()
    agent = QLearningAgent()

    fig, ax = plt.subplots(figsize=(8,8))
    plt.ion()
    fig.canvas.mpl_connect('button_press_event', on_mouse_click)  # ← le clic magique

    print("\nCLIQUE N'IMPORTE OÙ dans la grille pour déplacer le goal à tout moment !")
    print("   (pas sur le départ rouge ni sur l’obstacle noir)\n")

    for episode in range(1, NUM_EPISODES + 1):
        state = START_STATE

        # Choix du goal pour cet épisode
        if MANUAL_GOAL_MODE and manual_goal is not None:
            env.goal = manual_goal
        elif RANDOM_GOAL_EVERY_EPISODE:
            env.goal = np.random.choice(VALID_GOAL_POSITIONS)
        else:
            env.goal = (4, 4)

        current_goal = env.goal
        total_reward = 0

        for step in range(MAX_STEPS):
            action = agent.choose_action(state)
            next_state, reward, done = env.step(state, action)
            agent.update(state, action, reward, next_state, done)

            total_reward += reward
            state = next_state

            # ==== DESSIN ====
            draw_grid(ax)

            # Goal (vert lime)
            gx, gy = current_goal
            ax.add_patch(plt.Rectangle((gx, gy), 1, 1, color='lime', alpha=0.9, edgecolor='darkgreen', lw=3))
            ax.text(gx+0.5, gy+0.5, '+10', ha='center', va='center',
                    fontsize=16, fontweight='bold', color='darkgreen')

            draw_agent(ax, state)

            ax.set_title(f"Épisode {episode} | Goal actuel = {current_goal} | "
                        f"Récompense = {total_reward:+.1f} | ε = {agent.epsilon:.3f} | "
                        f"Clique pour déplacer le goal !",
                        fontsize=14)
            plt.pause(0.03)

            if done:
                print(f"Goal {current_goal} atteint en {step+1} étapes !")
                break

        agent.decay_epsilon()

        if episode % 50 == 0:
            print(f"Épisode {episode:3d} → Goal était en {current_goal} → Récompense = {total_reward:+.1f}")

    plt.ioff()
    print("\nEntraînement terminé ! Valeurs finales (politique apprise même avec goal mobile) :")
    show_final_values(agent.Q)

if __name__ == "__main__":
    main()