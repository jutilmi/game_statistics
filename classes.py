# tilastoseuranta/classes.py

"""Provide classes required by the app

The module contains the following classes

- 'Game' - Base class for the game event
- 'Team' - Team class representing teams participating in the game
- 'Player' - Player class representing a player in a team
- 'GameEvent' - Game event class representing an event in a game, such as pass or shoot
- 'Pass(GameEvent)' - Pass class as a subclass for game event class 
"""

import re
import json
from collections import Counter
from itertools import groupby
from time import time

class Game:
    """Game class
    """

    def __init__(self, game_details_json):
        """
        Attributes:
            game_number (int): game number id
            home_team (Team): home team of the game
            away_team (Team): away team of the game
            events (list): all events of the game
            total_game_time (int): total game time in minutes
            periods (int): number of periods in the game

        Args:
            game_details_json: game details in json formatted file
                {
                    number
                    home_team
                    home_team_details: team details in a separate json formatted file
                    {
                         name
                         main_color
                         shirt_color
                         shorts_color
                         players :
                         [
                            "number - name"
                         ]   
                    }
                    away_team
                    away_team_details: json file of away team (see home team)
                }
        """
        # Reading game details from json
        with open(game_details_json) as g:
            game_details = json.load(g)
        
        # Adding game number
        self.game_number = game_details['number']

        # Looping teams's details to add team names and players
        for team_details in [game_details['home_team_details'], game_details['away_team_details']]:
            with open(team_details) as j:
                team_json = json.load(j)
        
            if team_json['name'] == game_details['home_team']:
                self.home_team = Team(game_details['home_team'], self)
                self.home_team.add_players(team_json['players'])
        
            elif team_json['name'] == game_details['away_team']:
                self.away_team = Team(game_details['away_team'], self)
                self.away_team.add_players(team_json['players'])

        self.events = []

        self.total_game_time = game_details['total_period_time_in_minutes']
        self.periods = game_details['periods']

        self.started = False

    def passing_chains(self, pass_transfer: str) -> tuple([Counter, int]):
        """Modifies and returns pass-list to ordered Counter pass-list and
        retruns longest pass_transfer_chain.

        # TODO: Fix doctests
        Examples:
            >>> Game.passing_chains(self, "o1")
            (Counter({1: 1, 2: 1}), 2)
            >>> Game.passing_chains(["o1", "v1", "o0", "o0", "o1", "o1"], "v1")
            (Counter({1: 1}), 1)

        Args:
            pass_transfer: type of pass, e.g. "o1" i.e o-teams passes to own team
        
        Returns:
            counter-object, consisting of pass chain length vs. their quantity in the game
            longest pass chain
        """

        pass_codes = [p.code() for p in self.get_passes()]

        c = [len(list(quantity)) for chain_length, quantity in groupby(pass_codes, key=lambda x:x == pass_transfer) if chain_length]
        longest_pass_chain_length = max(c) if len(c) > 0 else 0
        return Counter(c), longest_pass_chain_length

    def get_passes(self):
        """Returns all passes (Pass instance) in time-ordered list
        """
        passes = []
        for event in self.events:
            if isinstance(event, Pass):
                passes.append(event)
        return passes
    
class Team:
    """Team class representing a home team or away team in a game.
    """

    def __init__(self, name:str, game:Game=None):
        """Initializes new Team instance

        Args:
            name: team name
            game: game where the team belongs to (default: None)

        Attributes:
            name (str): name of the team
            players (list): players in a team, empty when initialized
            game (Game): game into which the team belongs to if given in args
            ball_control_timer (int): timer in seconds for team ball control
        """
        self.name = name
        self.players = []
        if game:
            self.game = game
        self.ball_control_timer = 0

    def code(self) -> str:
        """Returns team code

        Returns:
            first letter of a team name in lower letter
        """
        return self.name[0].lower()

    def add_players(self, players:list):
        """Add players to the team from argument list and adds them to self.players

        Args:
            players: list of players typically read from json formatted team data
        """
        player_match = re.compile(r'^(?P<number>[0-9]+).{3}(?P<name>[a-zA-Z\s\-]+)$')
        for player in players:
            m = player_match.match(player)
            if m:
                new_player = Player(self, int(m.group('number')), m.group('name'))
                new_player.team = self
                self.players.append(new_player)

    def get_player(self, player_number:int):
        """Returns player whose number matches a player in a team
        
        Args:
           player_number: number of a requested player

        Return:
            player (Player) whose number matches a player in a team        
        """
        for player in self.players:
            if player.player_number == player_number:
                return player

    def get_passes(self):
        """Returns passes by the team

        Args:
            game: game object
        
        Returns:
            list of passes by the team in the game
        """
        passes = []
        for _pass_ in self.game.get_passes():
            if _pass_.passing_player.team == self:
                passes.append(_pass_)
        return passes

class Player:
    """Player class"""

    def __init__(self, team:Team, player_number:int, name:str):
        """
        Args:
            team: team into which player belongs to
            player_number: number of the player
            name: player name
        
        Attributes:
            team (Team): team of the player
            player_number (int): player number
            name (str): player name
            position (str): player position, by default None
        """
        self.team = team
        self.player_number = player_number
        self.name = name
        self.position = None

    def __str__(self) -> str:
        return f"Player: {str(self.name)}, number: {self.player_number}"

    def get_passes(self):
        """Returns passes by the player
        
        Returns:
            time-ordered list of passes by the player in the game
        """
        passes = []
        for _pass_ in self.team.get_passes():
            if _pass_.passing_player == self:
                passes.append(_pass_)
        return passes

class GameEvent:
    """Game event class as a base class for all game events"""

    def __init__(self, gametime, initialization_player:Player):
        """Initializes new game event.

        Args:
            gametime (string): gametime
            initialization_player: player who starts the event, e.g. passes a ball, shoots, etc.
        """
        self.gametime = gametime
        self.initialization_player = initialization_player

class Pass(GameEvent):
    """Pass game event"""
    
    def __init__(self, game_event:GameEvent, receiving_player:Player) -> None:
        """Initializes new Pass event.

        Args:
            game_event: basic game_event which was initialized
            receiving_player: the player to whom pass ends to
        
        Attributes:
            passing_player (Player): player who passes the ball (equal to game_event.initialization_player)
            receiving_player (Player): player who received the ball
            gametime: game time when the event was initialized
            target (int): sets target to 1 if passing player and receiving player are in the same team, otherwise 0
        """
        self.passing_player = game_event.initialization_player
        self.receiving_player = receiving_player
        self.gametime = game_event.gametime

        if self.receiving_player == 'out':
            self.target = 2
        else:
            if self.passing_player.team == self.receiving_player.team:
                self.target = 1
            else:
                self.target = 0
    
    def code(self):
        return self.passing_player.team.code() + str(self.target)

    def __str__(self):
        return self.code
