import gym
import numpy as np
from typing import Tuple, Dict, Any

class KubeGymEnv(gym.Env):
    """
    Simplified Kubernetes Gym Environment for DoS attack simulation.
    
    The environment simulates a single deployment with basic metrics (CPU, Memory, Network).
    - Red agent randomly launches DoS attacks that spike resource usage
    - Blue agent must detect and mitigate these attacks
    """

    def __init__(self):
        # Simplified observation space with just the essential metrics
        self.observation_space = gym.spaces.Dict({
            "cpu_usage": gym.spaces.Box(low=0, high=100, shape=(1,), dtype=np.float32),
            "memory_usage": gym.spaces.Box(low=0, high=100, shape=(1,), dtype=np.float32),
            "network_requests": gym.spaces.Box(low=0, high=1000, shape=(1,), dtype=np.float32),
            "pod_status": gym.spaces.Discrete(2),  # 0: Healthy, 1: Unhealthy
        })

        # Simplified action space for the defender (blue agent)
        self.action_space = gym.spaces.Discrete(5)
        
        # Simplified action mapping
        self.action_map = {
            0: "Do nothing",
            1: "Enable rate limiting",  # Reduces network requests
            2: "Scale up resources",    # Increases CPU/Memory limits
            3: "Block suspicious IPs",   # Reduces attack effectiveness
            4: "Reset deployment",      # Emergency action - restores to normal state
        }

        # Internal state
        self.current_step = 0
        self.max_steps = 100
        self.attack_probability = 0.1  # 10% chance of attack each step
        self.under_attack = False
        self.attack_duration = 0
        
        # Thresholds for detecting problems
        self.cpu_threshold = 80.0
        self.memory_threshold = 80.0
        self.network_threshold = 800.0

    def _get_observation(self) -> Dict[str, np.ndarray]:
        """Get current system metrics."""
        base_cpu = 30.0  # Base CPU usage
        base_memory = 40.0  # Base memory usage
        base_network = 100.0  # Base network requests

        if self.under_attack:
            # Simulate increased resource usage during attack
            cpu = base_cpu + np.random.uniform(40, 60)
            memory = base_memory + np.random.uniform(30, 50)
            network = base_network + np.random.uniform(600, 800)
        else:
            # Normal variation in resource usage
            cpu = base_cpu + np.random.uniform(-10, 10)
            memory = base_memory + np.random.uniform(-10, 10)
            network = base_network + np.random.uniform(-50, 50)

        return {
            "cpu_usage": np.array([min(100.0, max(0.0, cpu))], dtype=np.float32),
            "memory_usage": np.array([min(100.0, max(0.0, memory))], dtype=np.float32),
            "network_requests": np.array([min(1000.0, max(0.0, network))], dtype=np.float32),
            "pod_status": 1 if self.under_attack else 0
        }

    def _get_info(self) -> Dict[str, Any]:
        """Get additional information about the environment."""
        return {
            "steps": self.current_step,
            "under_attack": self.under_attack,
            "attack_duration": self.attack_duration
        }

    def reset(self) -> Tuple[Dict[str, np.ndarray], Dict[str, Any]]:
        """Reset the environment to initial state."""
        self.current_step = 0
        self.under_attack = False
        self.attack_duration = 0
        
        observation = self._get_observation()
        info = self._get_info()
        
        return observation, info

    def step(self, action: int) -> Tuple[Dict[str, np.ndarray], float, bool, bool, Dict[str, Any]]:
        """
        Take an action in the environment.
        
        Returns:
            observation: Current system metrics
            reward: Reward for the action taken
            terminated: Whether the episode is done
            truncated: Whether the episode was truncated
            info: Additional information
        """
        assert self.action_space.contains(action)
        
        # Update step counter
        self.current_step += 1
        
        # Red agent randomly decides to attack
        if not self.under_attack and np.random.random() < self.attack_probability:
            self.under_attack = True
            self.attack_duration = 0
        
        # Update attack duration
        if self.under_attack:
            self.attack_duration += 1

        # Process defender's action
        reward = self._process_action(action)
        
        # Get new observation
        observation = self._get_observation()
        
        # Check if episode is done
        done = self.current_step >= self.max_steps
        
        return observation, reward, done, False, self._get_info()

    def _process_action(self, action: int) -> float:
        """Process the defender's action and return the reward."""
        reward = 0.0
        
        # Penalty for taking any action
        reward -= 1.0
        
        if self.under_attack:
            if action == 0:  # Do nothing during attack
                reward -= 5.0
            elif action == 1:  # Rate limiting
                reward += 3.0
                if np.random.random() < 0.3:  # 30% chance to stop attack
                    self.under_attack = False
            elif action == 2:  # Scale up resources
                reward += 2.0
                if np.random.random() < 0.2:  # 20% chance to stop attack
                    self.under_attack = False
            elif action == 3:  # Block IPs
                reward += 4.0
                if np.random.random() < 0.4:  # 40% chance to stop attack
                    self.under_attack = False
            elif action == 4:  # Reset deployment
                reward += 1.0
                self.under_attack = False  # Always stops attack but with high cost
                reward -= 3.0
        else:
            if action == 0:  # Reward for doing nothing when there's no attack
                reward += 1.0
            else:  # Penalty for taking unnecessary action
                reward -= 2.0

        return reward

    def render(self):
        """Simple console rendering of the environment state."""
        obs = self._get_observation()
        print(f"\nStep: {self.current_step}")
        print(f"Under Attack: {self.under_attack}")
        print(f"CPU Usage: {obs['cpu_usage'][0]:.1f}%")
        print(f"Memory Usage: {obs['memory_usage'][0]:.1f}%")
        print(f"Network Requests: {obs['network_requests'][0]:.1f}")
        print(f"Pod Status: {'Unhealthy' if obs['pod_status'] else 'Healthy'}")
