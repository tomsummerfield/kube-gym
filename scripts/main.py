import gym
from envs.kube_gym import KubeGymEnv

env = KubeGymEnv()
obs, info = env.reset()

for _ in range(100):
    action = env.action_space.sample()  # Your agent would make this decision
    obs, reward, terminated, truncated, info = env.step(action)
    env.render()
    
    if terminated or truncated:
        obs, info = env.reset()
