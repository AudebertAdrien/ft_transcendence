import gymnasium as gym
import numpy as np
from game import Game
from gym import Env
from gym.spaces import Discrete, Box

class PongEnv(gymnasium.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60}

    def __init__(self):
        # Set dimensions of the game window
        self.game_width = 800
        self.game_height = 400

        # Initialize the valocity and position of the ball 
        self.ball_velocity = [5, -5]
        self.ball_position = [self.game_height // 2, self.game_width // 2]

        # Initialize paddle info  and their position
        self.paddle_width = 10
        self.paddle_length = 80
        self.ball_position = [self.game_height // 2, self.game_width // 2]
        self.agent_position = [self.game_height // 2, self.game_width]

        self.action_space = Discrete(3)
        self.observation_space = Box(0, 255, (self.game_width, self.game_height, 3), uint8)

        self.action_to_direction = {
            0: np.array([-5, 0]), # move paddle up but needs to define how much pixels
            1: np.array([0, 0]), # paddle stays
            2: np.array([5, 0]), # move paddle down
        }

    def step(self, action):
        # Update the position of the ball based on the action taken
        self.ball_position += self.ball_position + self.ball_velocity

        # Update the position of the agent based on the action taken
        self.agent_position += self.agent_position[action] 

        # Check for collisions with the left and right of the game window
        if self.ball_position[1] <= 0:
            self.reset()
        elif self.ball_position[1] >= self.game_width:
            self.reset()
        pass

    def reset(self):
        self.ball_position = [self.game_height // 2, self.game_width // 2]
        pass

    def render(self):
        pass

    def close(self):
        pass



## Observing the environment

# Reset the environment to get the first observation
observation, info = env.reset()

## Interact with the environment

#Sample a random action from all valid actions
action = env.action_space.sample()
# Execute action
observation, reward, terminated, truncated, info = env.step(action)
env.render()

while not terminated and not truncated:
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)
    env.render()
    

env.close()
