# run.py
import matplotlib.pyplot as plt
import numpy as np
from environment import GridWorld
from agent import QLearningAgent
from visualization import draw_grid, draw_agent, show_final_values
from config import *

def main():
    env = GridWorld()
    agent = QLearningAgent()

    fig, ax = plt.subplots(figsize=(7,7))
    plt.ion()

    for episode in range(1, NUM_EPISODES + 1):
        state = env.reset()                     # ← Nouveau goal choisi ici !
        current_goal = env.get_goal()

        total_reward = 0
        path = []

        for step in range(MAX_STEPS):
            action = agent.choose_action(state)
            next_state, reward, done = env.step(state, action)
            agent.update(state, action, reward, next_state, done)

            total_reward += reward
            state = next_state
            path.append(state)

            # === VISUALISATION ===
            draw_grid(ax)
            # On affiche le goal en cours
            gx, gy = current_goal
            ax.add_patch(plt.Rectangle((gx, gy), 1, 1, color='lime', alpha=0.9))
            ax.text(gx+0.5, gy+0.5, '+10', ha='center', va='center',
                    fontsize=14, fontweight='bold', color='darkgreen')

            draw_agent(ax, state)
            ax.set_title(f"Épisode {episode} | Goal = {current_goal} | "
                        f"Reward = {total_reward:+.1f} | ε = {agent.epsilon:.3f}")
            plt.pause(0.03)

            if done:
                print(f"Goal {current_goal} atteint en {step+1} étapes !")
                break

        agent.decay_epsilon()

        if episode % 50 == 0 or episode == 1:
            print(f"Épisode {episode:3d} → Goal était en {current_goal} → Récompense = {total_reward}")

    plt.ioff()
    print("\nEntraînement terminé ! Voici la politique apprise (même avec goal changeant)")
    show_final_values(agent.Q)

if __name__ == "__main__":
    main()