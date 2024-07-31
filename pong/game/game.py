# /pong/game/game.py

import json
import asyncio
import random

class Game:
    def __init__(self, game_id, player1, player2):
        self.game_id = game_id
        self.player1 = player1
        self.player2 = player2
        self.botgame = player2 is None
        self.game_state = {
            'player1_name': player1.user.username,
            'player2_name': player2.user.username if player2 else 'BOT',
            'player1_position': 150,
            'player2_position': 150,
            'ball_position': {'x': 390, 'y': 190},
            'ball_velocity': {'x': random.choice([-5, 5]), 'y': random.choice([-5, 5])},
            'player1_score': 0,
            'player2_score': 0
        }
        self.speed = 1
        self.game_loop_task = None
        self.ended = False

    async def start_game(self):
        print(f"- Game #{self.game_id} STARTED")
        self.game_loop_task = asyncio.create_task(self.game_loop())

    async def game_loop(self):
        while True:
            if self.botgame:
                await self.update_bot_position()
            self.update_game_state()
            await self.send_game_state()
            await asyncio.sleep(1/60)  # Around 60 FPS

    async def update_bot_position(self):
        target_y = self.game_state['ball_position']['y']
        if self.game_state['player2_position'] < target_y < self.game_state['player2_position'] + 80:
            pass
        elif self.game_state['player2_position'] < target_y:
            self.game_state['player2_position'] = min(self.game_state['player2_position'] + (5 * self.speed), 300)
        elif self.game_state['player2_position'] + 80 > target_y:
            self.game_state['player2_position'] = max(self.game_state['player2_position'] - (5 * self.speed), 0)

    def update_game_state(self):
        # Update ball position
        self.game_state['ball_position']['x'] += self.game_state['ball_velocity']['x']
        self.game_state['ball_position']['y'] += self.game_state['ball_velocity']['y']
        # Check for collisions with top and bottom walls
        if self.game_state['ball_position']['y'] <= 10 or self.game_state['ball_position']['y'] >= 390:
            self.game_state['ball_velocity']['y'] *= -1
        # Check for collisions with paddles
        if self.game_state['ball_position']['x'] <= 20 and \
            self.game_state['player1_position'] - 10 <= self.game_state['ball_position']['y'] <= self.game_state['player1_position'] + 90:
            if self.game_state['ball_velocity']['x'] < 0:
                self.game_state['ball_velocity']['x'] *= -1
            self.update_ball_velocity()
        elif self.game_state['ball_position']['x'] >= 760 and \
            self.game_state['player2_position'] - 10 <= self.game_state['ball_position']['y'] <= self.game_state['player2_position'] + 90:
            if self.game_state['ball_velocity']['x'] > 0:
                self.game_state['ball_velocity']['x'] *= -1
            self.update_ball_velocity()
        # Check for scoring
        if self.game_state['ball_position']['x'] <= 10:
            self.game_state['player2_score'] += 1
            self.reset_ball()
        elif self.game_state['ball_position']['x'] >= 790:
            self.game_state['player1_score'] += 1
            self.reset_ball()

    def reset_ball(self):
        self.game_state['ball_position'] = {'x': 390, 'y': 190}
        self.game_state['ball_velocity'] = {'x': random.choice([-5, 5]), 'y': random.choice([-5, 5])}
        self.speed = 1

    def update_ball_velocity(self):
        self.speed += 0.05
        if self.speed > 2:
            self.speed = 2
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
        if self.ended:
            return
        message = json.dumps({
            'type': 'game_state_update',
            'game_state': self.game_state
        })
        await self.player1.send(message)
        if not self.botgame:
            await self.player2.send(message)

    async def handle_key_press(self, player, key):
        if self.ended:
            return
        if player == self.player1:
            if key == 'arrowup':
                self.game_state['player1_position'] = max(self.game_state['player1_position'] - 25, 0)
            elif key == 'arrowdown':
                self.game_state['player1_position'] = min(self.game_state['player1_position'] + 25, 300)
        elif not self.botgame and player == self.player2:
            if key == 'arrowup':
                self.game_state['player2_position'] = max(self.game_state['player2_position'] - 25, 0)
            elif key == 'arrowdown':
                self.game_state['player2_position'] = min(self.game_state['player2_position'] + 25, 300)

    async def end_game(self, disconnected_player=None):
        if not self.ended:
            self.ended = True
            if self.game_loop_task:
                self.game_loop_task.cancel()            
            print(f"- Game #{self.game_id} ENDED")
            # Notify that one player left the game      
            if disconnected_player:
                remaining_player = self.player2 if disconnected_player == self.player1 else self.player1
                disconnected_name = disconnected_player.user.username
                message = json.dumps({
                    'type': 'player_disconnected',
                    'player': disconnected_name
                })
                if not self.botgame:
                    await remaining_player.send(message)            
            # Notify both players that the game has ended
            end_message = json.dumps({
                'type': 'game_ended',
                'game_id': self.game_id
            })
            await self.player1.send(end_message)
            if not self.botgame:
                await self.player2.send(end_message)
            #endfortheouche(p1, p2, s_p1, s_p2, winner, bt_p1, bt_p2, dur, is_tournoi, name_tournament)
