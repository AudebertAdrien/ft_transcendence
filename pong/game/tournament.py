# /pong/game/tournament.py

import json
import asyncio
from django.template.loader import render_to_string
import random
from .matchmaking import match_maker
from .game import Game

class TournamentMatch(Game):
    def __init__(self, game_id, player1, player2, tournament):
        # Initialize the parent Game class with the provided parameters
        super().__init__(game_id, player1, player2, False)        
        # Store the current game instance in active games
        match_maker.active_games[game_id] = self        
        # Set the game for the players
        player1.set_game(self)
        if player2:
            player2.set_game(self)        
        # Store the tournament instance
        self.tournament = tournament

    async def end_game(self, disconnected_player=None):
        # Call the parent class's end_game method
        await super().end_game(disconnected_player)
        # Handle the end of the match in the tournament context
        await self.tournament.handle_match_end(self)


class TournamentMatchMaker:
    def __init__(self):
        self.waiting_players = []
        self.matches = []
        self.rounds = []
        self.current_round = 0
        self.tournament_state = "waiting"  # Can be "waiting", "in_progress", or "ended"

    async def add_player(self, player):
        if self.tournament_state == "waiting" and player not in self.waiting_players:
            self.waiting_players.append(player)
            print(f"User {player.user.username} joins the TOURNAMENT WAITING ROOM")
            await self.update_waiting_room()

    async def remove_player(self, player):
        if player in self.waiting_players:
            self.waiting_players.remove(player)
            await self.update_waiting_room()

    async def update_waiting_room(self):
        html = self.generate_waiting_room_html()
        for player in self.waiting_players:
            await self.send_to_player(player, {
                'type': 'update_tournament_waiting_room',
                'html': html
            })

    def generate_waiting_room_html(self):
        context = {
            'players': [player.user.username for player in self.waiting_players],
            'tournament_state': self.tournament_state,
            'players_count': len(self.waiting_players),
            'min_players_to_start': 2  # You can adjust this number as needed
        }
        return render_to_string('pong/tournament_waiting_room.html', context)

    async def start_tournament(self):
        if len(self.waiting_players) < 2:
            return False
        
        self.tournament_state = "in_progress"
        random.shuffle(self.waiting_players)
        self.current_round = 1
        self.create_matches(self.waiting_players)
        await self.update_brackets()
        await self.start_round_matches()
        return True

    def create_matches(self, players):
        matches = []
        for i in range(0, len(players), 2):
            if i + 1 < len(players):
                matches.append(TournamentMatch(len(self.matches) + 1, players[i], players[i + 1], self))
            else:
                matches.append(TournamentMatch(len(self.matches) + 1, players[i], None, self))  # Bye
        self.rounds.append(matches)
        self.matches.extend(matches)

    async def update_brackets(self):
        html = self.generate_bracket_html()
        for player in self.waiting_players:
            await self.send_to_player(player, {
                'type': 'update_brackets',
                'html': html
            })

    def generate_bracket_html(self):
        context = {
            'tournament_rounds': self.get_tournament_data()
        }
        return render_to_string('pong/tournament_brackets.html', context)

    def get_tournament_data(self):
        return [
            [
                {
                    'player1': match.player1.user.username if match.player1 else 'BYE',
                    'player2': match.player2.user.username if match.player2 else 'BYE',
                    'winner': match.game_state['player1_name'] if match.game_state['player1_score'] > match.game_state['player2_score'] else match.game_state['player2_name'] if match.ended else None,
                    'score1': match.game_state['player1_score'],
                    'score2': match.game_state['player2_score']
                }
                for match in round_matches
            ]
            for round_matches in self.rounds
        ]

    async def start_round_matches(self):
        for match in self.rounds[-1]:
            if match.player1 and match.player2:
                await match_maker.notify_players(match.player1, match.player2, match.game_id, False)
                asyncio.create_task(match.start_game())
            elif match.player1:
                # Handle bye
                match.game_state['player1_score'] = 3
                match.game_state['player2_score'] = 0
                await match.end_game()

    async def handle_match_end(self, match):
        await self.update_brackets()
        if all(m.ended for m in self.rounds[-1]):
            await self.advance_tournament()

    async def advance_tournament(self):
        winners = [match.player1 if match.game_state['player1_score'] > match.game_state['player2_score'] else match.player2 for match in self.rounds[-1] if match.player1 and match.player2]
        if len(winners) > 1:
            self.current_round += 1
            self.create_matches(winners)
            await self.update_brackets()
            await self.start_round_matches()
        else:
            await self.end_tournament(winners[0])

    async def end_tournament(self, winner):
        self.tournament_state = "ended"
        for player in self.waiting_players:
            await self.send_to_player(player, {
                'type': 'tournament_end',
                'winner': winner.user.username
            })
        self.waiting_players = []
        self.matches = []
        self.rounds = []
        self.current_round = 0

    async def send_to_player(self, player, data):
        await player.send(json.dumps(data))

# Instance of the class
tournament_match_maker = TournamentMatchMaker()