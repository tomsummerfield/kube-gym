from src.envs.kube_gym import KubeGymEnv

def main(episodes: int = 10):
    env = KubeGymEnv()

    for episode in range(episodes):
        observation, info = env.reset()  # Need to capture initial observation and info
        print(f"\nStarting Episode {episode + 1}")

        terminated = False
        truncated = False

        while not (terminated or truncated):
            action = env.action_space.sample()
            observation, reward, terminated, truncated, info = env.step(action)
            print(f"Observation: {observation},\n"
                  f"Action: {env.action_map[action]},\n"  # Use action_map for readable action
                  f"Reward: {reward:.2f},\n"
                  f"Terminated: {terminated},\n" 
                  f"Truncated: {truncated},\n"
                  f"Info: {info}")
            
            env.render()  # Add visualization of environment state


if __name__ == "__main__":
    main()