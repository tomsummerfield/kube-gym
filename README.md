# KubeGym: Kubernetes Security Gym Environment

A Gymnasium environment that simulates a Kubernetes deployment under DoS attacks, designed for training defensive AI agents.

## Overview

KubeGym provides a simplified simulation of a Kubernetes deployment where:
- A **Red Agent** (environment) randomly launches DoS attacks that spike resource usage
- A **Blue Agent** (defender) must detect and mitigate these attacks through various actions

The environment monitors key metrics:
- CPU Usage
- Memory Usage
- Network Requests
- Pod Health Status

### Defensive Actions Available
The Blue Agent can take the following actions:
1. Do nothing (maintain current state)
2. Enable rate limiting (reduces network requests)
3. Scale up resources (increases CPU/Memory limits)
4. Block suspicious IPs (reduces attack effectiveness)
5. Reset deployment (emergency restore to normal state)

## Installation

```shell
cd kube_gym
pip install -e .
```

## Usage

```python
import gymnasium as gym
import kube_gym

# Create the environment
env = gym.make('KubeGym-v0')

# Reset the environment
observation, info = env.reset()

# Run one episode
for _ in range(100):
    # Your agent's logic here
    action = env.action_space.sample()  # Replace with your agent's decision
    
    # Take action in environment
    observation, reward, terminated, truncated, info = env.step(action)
    
    # Render the current state (optional)
    env.render()
    
    if terminated or truncated:
        observation, info = env.reset()
```

## Environment Details

### Observation Space
- `cpu_usage`: Float [0, 100]
- `memory_usage`: Float [0, 100]
- `network_requests`: Float [0, 1000]
- `pod_status`: Binary (0: Healthy, 1: Unhealthy)

### Action Space
Discrete(5) representing different defensive measures

### Rewards
- Positive rewards for successful attack mitigation
- Negative rewards for:
  - Taking unnecessary actions when no attack is present
  - Failing to respond to attacks
  - Using costly defensive measures

## Requirements

- Python 3.7+
- gymnasium
- numpy

## Contributing

If you would like to contribute, follow these steps:
1. Fork this repository
2. Clone your fork
3. Create a new branch for your feature
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

