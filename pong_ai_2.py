import gymnasium as gym
import numpy as np
from game.py import Game
from gym import Env
from gym.spaces import Discrete, Box

class PongEnv(gymnasium.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60}

    def __init__(self, game):
        self.game = game
        self.action_space = Discrete(3)
        self.observation_space = Box(0, 255, (self.game_width, self.game_height, 3), uint8)

        self.action_to_direction = {
            0: np.array([-5, 0]), # move paddle up by 5 pixels
            1: np.array([0, 0]), # paddle stays
            2: np.array([5, 0]), # move paddle down by 5 pixels
        }

    def step(self, action):
        # Map the action to a direction
        direction = self.action_to_direction[action]
        # Update the game state based on the direction
        self.game.handle_key_press(self.game.player2, direction)
        # Update the position of the ball based on its velocity
        self.game.game_state['ball_position']['x'] += self.game.game_state['ball_velocity']['x']
        self.game.game_state['ball_position']['y'] += self.game.game_state['ball_velocity']['y']
        # Get the new observation
        observation = self.game.get_observation()
        # Calculate the reward
        reward = self.calculate_reward(observation)
        # Return the observation, reward, done, and info
        return observation, reward, done, {}
        
    def reset(self):
        self.ball_position = [self.game_height // 2, self.game_width // 2]
        pass

    def render(self):
        pass

    def close(self):
        pass

game = Game(game_id, player1_id, player2_id)

