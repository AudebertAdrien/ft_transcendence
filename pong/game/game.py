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
            'player1_position': 150,
            'player2_position': 150,
            'ball_position': {'x': 390, 'y': 190},
            'ball_velocity': {'x': random.choice([-5, 5]), 'y': random.choice([-5, 5])},
            'player1_score': 0,
            'player2_score': 0
        }
        self.speed = 1
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
        if self.game_state['ball_position']['y'] <= 10 or self.game_state['ball_position']['y'] >= 390:
            self.game_state['ball_velocity']['y'] *= -1

        # Check for scoring
        if self.game_state['ball_position']['x'] <= 10:
            self.game_state['player2_score'] += 1
            self.reset_ball()
        elif self.game_state['ball_position']['x'] >= 790:
            self.game_state['player1_score'] += 1
            self.reset_ball()

        # Check for collisions with paddles
        if self.game_state['ball_position']['x'] <= 20 and \
            self.game_state['player1_position'] <= self.game_state['ball_position']['y'] <= self.game_state['player1_position'] + 80:
            self.update_ball_velocity()
            self.game_state['ball_velocity']['x'] *= -1
        elif self.game_state['ball_position']['x'] >= 760 and \
            self.game_state['player2_position'] <= self.game_state['ball_position']['y'] <= self.game_state['player2_position'] + 80:
            self.update_ball_velocity()
            self.game_state['ball_velocity']['x'] *= -1

    def reset_ball(self):
        self.game_state['ball_position'] = {'x': 390, 'y': 190}
        self.game_state['ball_velocity'] = {'x': random.choice([-5, 5]), 'y': random.choice([-5, 5])}
        self.speed = 1

    def update_ball_velocity(self):
        self.speed += 0.05
        if self.speed > 2:
            self.speed = 2
        else:
            print(f"Ball velocity: {self.speed}")
        self.game_state['ball_velocity']['x'] *= self.speed
        if self.game_state['ball_velocity']['x'] < -10:
            self.game_state['ball_velocity']['x'] = -10
        elif self.game_state['ball_velocity']['x'] > 10:
            self.game_state['ball_velocity']['x'] = 10
        self.game_state['ball_velocity']['y'] *= self.speed
        if self.game_state['ball_velocity']['y'] < -10:
            self.game_state['ball_velocity']['y'] = -10
        elif self.game_state['ball_velocity']['y'] > 10:
            self.game_state['ball_velocity']['y'] = 10

    async def send_game_state(self):
        message = json.dumps({
            'type': 'game_state_update',
            'game_state': self.game_state
        })
        await self.player1.send(message)
        await self.player2.send(message)

    async def handle_key_press(self, player, key):
        if player == self.player1:
            if key == 'arrowup' and self.game_state['player1_position'] >= 25:
                self.game_state['player1_position'] -= 25
            elif key == 'arrowdown' and self.game_state['player1_position'] <= 275:
                self.game_state['player1_position'] += 25
        elif player == self.player2:
            if key == 'arrowup' and self.game_state['player2_position'] >= 25:
                self.game_state['player2_position'] -= 25
            elif key == 'arrowdown' and self.game_state['player2_position'] <= 275:
                self.game_state['player2_position'] += 25

    async def end_game(self):
        if self.game_loop_task:
            self.game_loop_task.cancel()
        # Add any cleanup code here