# run.py
import matplotlib.pyplot as plt
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
        state = START_STATE
        total_reward = 0

        for step in range(MAX_STEPS):
            action = agent.choose_action(state)
            next_state, reward, done = env.step(state, action)
            agent.update(state, action, reward, next_state, done)

            total_reward += reward
            state = next_state

            # Animation fluide
            draw_grid(ax)
            draw_agent(ax, state)
            ax.set_title(f"Épisode {episode} | Récompense = {total_reward} | ε = {agent.epsilon:.3f}")
            plt.pause(0.02)

            if done:
                print(f"Goal atteint en {step+1} étapes ! (épisode {episode})")
                break

        agent.decay_epsilon()

        if episode % 50 == 0:
            print(f"Épisode {episode} → Récompense totale: {total_reward}")

    plt.ioff()
    print("\nEntraînement terminé ! Affichage des valeurs finales...")
    show_final_values(agent.Q)

if __name__ == "__main__":
    main()