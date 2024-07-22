# /pong/game/game.py

import json
import asyncio
import random

class Game:
    def __init__(self, game_id, player1, player2):
        self.game_id = game_id
        self.player1 = player1
        self.player2 = player2
        self.game_state = {
            'player1_name': player1.user.username,
            'player2_name': player2.user.username,
            'player1_position': 200,  # middle of the game field
            'player2_position': 200,
            'ball_position': {'x': 400, 'y': 300},  # middle of the game field
            'ball_velocity': {'x': random.choice([-5, 5]), 'y': random.choice([-5, 5])},
            'player1_score': 0,
            'player2_score': 0
        }
        self.game_loop_task = None

    async def start_game(self):
        print(f"- Game {self.game_id} START")
        self.game_loop_task = asyncio.create_task(self.game_loop())

    async def game_loop(self):
        while True:
            self.update_game_state()
            await self.send_game_state()
            await asyncio.sleep(1/60)  # 60 FPS

    def update_game_state(self):
        # Update ball position
        self.game_state['ball_position']['x'] += self.game_state['ball_velocity']['x']
        self.game_state['ball_position']['y'] += self.game_state['ball_velocity']['y']

        # Check for collisions with top and bottom walls
        if self.game_state['ball_position']['y'] <= 0 or self.game_state['ball_position']['y'] >= 600:
            self.game_state['ball_velocity']['y'] *= -1

        # Check for scoring
        if self.game_state['ball_position']['x'] <= 0:
            self.game_state['player2_score'] += 1
            self.reset_ball()
        elif self.game_state['ball_position']['x'] >= 800:
            self.game_state['player1_score'] += 1
            self.reset_ball()

        # Check for collisions with paddles
        if self.game_state['ball_position']['x'] <= 20 and \
           self.game_state['player1_position'] - 50 <= self.game_state['ball_position']['y'] <= self.game_state['player1_position'] + 50:
            self.game_state['ball_velocity']['x'] *= -1
        elif self.game_state['ball_position']['x'] >= 780 and \
             self.game_state['player2_position'] - 50 <= self.game_state['ball_position']['y'] <= self.game_state['player2_position'] + 50:
            self.game_state['ball_velocity']['x'] *= -1

    def reset_ball(self):
        self.game_state['ball_position'] = {'x': 400, 'y': 300}
        self.game_state['ball_velocity'] = {'x': random.choice([-5, 5]), 'y': random.choice([-5, 5])}

    async def send_game_state(self):
        message = json.dumps({
            'type': 'game_state_update',
            'game_state': self.game_state
        })
        await self.player1.send(message)
        await self.player2.send(message)

    async def handle_key_press(self, player, key):
        if player == self.player1:
            if key == 'arrowup' and self.game_state['player1_position'] > 0:
                self.game_state['player1_position'] -= 10
            elif key == 'arrowdown' and self.game_state['player1_position'] < 550:
                self.game_state['player1_position'] += 10
        elif player == self.player2:
            if key == 'arrowup' and self.game_state['player2_position'] > 0:
                self.game_state['player2_position'] -= 10
            elif key == 'arrowdown' and self.game_state['player2_position'] < 550:
                self.game_state['player2_position'] += 10

    async def end_game(self):
        if self.game_loop_task:
            self.game_loop_task.cancel()
        # Add any cleanup code here