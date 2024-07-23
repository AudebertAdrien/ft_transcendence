# /pong/game/matchmaking.py

import json
import asyncio
from .game import Game

class MatchMaker:
    def __init__(self):
        self.waiting_players = []
        self.active_games = {}
        self.matching_task = None

    async def add_player(self, player):
        if player not in self.waiting_players:
            self.waiting_players.append(player)
            print(f"User {player.user.username} joins the WAITING ROOM")
            if not self.matching_task or self.matching_task.done():
                self.matching_task = asyncio.create_task(self.match_loop())

    async def remove_player(self, player):
        if player in self.waiting_players:
            self.waiting_players.remove(player)

    async def match_loop(self):
        while True:
            if len(self.waiting_players) >= 2:
                player1 = self.waiting_players.pop(0)
                player2 = self.waiting_players.pop(0)
                print(f"MATCH FOUND: {player1.user.username} vs {player2.user.username}")
                game_id = await self.create_game(player1, player2)
            else:
                # No players to match, wait for a short time before checking again
                await asyncio.sleep(1)

    async def create_game(self, player1, player2):
        game_id = len(self.active_games) + 1
        print(f"- Creating game: {game_id}")
        new_game = Game(game_id, player1, player2)
        self.active_games[game_id] = new_game
        await self.notify_players(player1, player2, game_id)
        asyncio.create_task(new_game.start_game())
        return game_id

    async def notify_players(self, player1, player2, game_id):
        await player1.send(json.dumps({
            'type': 'game_start',
            'game_id': game_id,
            'player1': player1.user.username,
            'player2': player2.user.username
        }))
        await player2.send(json.dumps({
            'type': 'game_start',
            'game_id': game_id,
            'player1': player1.user.username,
            'player2': player2.user.username
        }))

    async def handle_key_press(self, player, key):
        for game in self.active_games.values():
            if player in [game.player1, game.player2]:
                await game.handle_key_press(player, key)
                break        

# Instance of the class
match_maker = MatchMaker()
