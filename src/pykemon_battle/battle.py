import math

import numpy as np
from rich.console import Console

from .player import Player
from .utils import (
    damage_function,
    constants,
)

console = Console(highlight=False)
TOTAL_POKEMON = 807


class Battle:
    """
    Class that contains the battle logic of the game
    """

    def __init__(self, player_1=None, player_2=None, team=1, enemy_team=1):
        """
        Initialise the battle object

        Parameters
        ----------
        team : int, list, optional
            If int is given this will be the size of the team,
            If list is given that is the team, by default 1
        enemy_team : int, list, optional
            If int is given this will be the size of the enemy team,
            If list is given that is the enemy team, by default None
        """
        if player_1 is None:
            self.player_1 = Player(team=team, name="Player 1")
        else:
            self.player_1 = player_1

        if player_2 is None:
            self.player_2 = Player(team=enemy_team, name="Player 2")
        else:
            self.player_2 = player_2

        self.turn = None
        self.attacker = None
        self.defender = None

    def apply_move(self, move):
        """
        Apply the selected move

        Parameters
        ----------
        move : int
            The index of the selected move (0-3)
        """
        move_attr = {}
        # Move variables
        move_attr["move_power"] = self.attacker.moveset[move].stats["power"]
        move_attr["move_type"] = self.attacker.moveset[move].stats["type"]

        # Attacker and defender variables
        move_attr["attacker_level"] = 50
        move_attr["attacker_type"] = self.attacker.type
        move_attr["attacker_attack"] = self.attacker.stats["attack"]
        move_attr["defender_defense"] = self.defender.stats["defense"]

        # Other variables
        move_attr["same_type_advantage"] = (
            move_attr["move_type"] in move_attr["attacker_type"]
        )
        type_effects = list(
            constants.TYPE_EFFECTS[move_attr["move_type"]][type_i]
            for type_i in self.defender.type
        )
        move_attr["modifier"] = math.prod(type_effects)
        move_attr["stochasticity"] = np.random.randint(217, 256)

        damage = None
        attack_successful = False
        if move_attr["move_power"] is not None:
            damage = damage_function(variables=move_attr)
            attacker_accuracy = self.attacker.moveset[move].stats["accuracy"]
            move_accuracy = attacker_accuracy if attacker_accuracy is not None else 100

            # TODO: Include pokemon's accuracy as well
            attack_successful = np.random.random() < (move_accuracy / 100)
            if attack_successful:
                self.defender.health_points = self.defender.health_points - damage
                self.defender.health_points = max(self.defender.health_points, 0)

        move_outcome_display = {
            "move_name": self.attacker.moveset[move].name,
            "move_index": move,
            "success": attack_successful,
            "modifier": move_attr["modifier"],
            "damage": damage,
        }
        return move_outcome_display

    # TODO: Merge player_turn_logic and enemy_turn_logic in one method
    def player_turn_logic(self, selected_move: int):
        """
        Logic of the player turn

        Parameters
        ----------
        selected_move : int
            The index of the move that was selected (0-3)
        """
        self.attacker = self.player_1.selected
        self.defender = self.player_2.selected
        move_outcome = self.apply_move(selected_move)
        if self.player_2.selected.health_points <= 0:
            self.player_2.selected.active = False
        return move_outcome

    def enemy_turn_logic(self, selected_move: int):
        """
        Logic of the enemy turn

        Parameters
        ----------
        selected_move : int
            The index of the move that was selected (0-3)
        """
        self.attacker = self.player_2.selected
        self.defender = self.player_1.selected
        move_outcome = self.apply_move(selected_move)
        if self.player_1.selected.health_points <= 0:
            self.player_1.selected.active = False
        return move_outcome

    def switch_pokemon(self, player_turn=True, pokemon_pos=None):
        """
        Switch the selected pokemon of a player. The current player's selected
        pokemon has to be None to be able to switch.

        Parameters
        ----------
        player : Player
            The player whose selected pokemon will be changed
        pokemon : Pokemon
            The pokemon that will be selected
        """
        current_player = self.player_1 if player_turn else self.player_2
        if pokemon_pos is not None:
            current_player.selected = current_player.team[pokemon_pos]
            if not current_player.selected.active:
                raise ValueError("This pokemon has fainted")
        else:
            # TODO: Implement a way to select the pokemon when no pokemon_pos is given
            if current_player.selected is None:
                raise ValueError("No more pokemon to battle")

    def get_active_pokemon(self, player_turn=True):
        """
        Return the active pokemon of a player
        """
        if player_turn:
            return [poke for poke in self.player_1.team if poke.health_points > 0]
        return [poke for poke in self.player_2.team if poke.health_points > 0]

    def simulate(
        self,
    ):
        """
        Simulate the battle
        """
        raise NotImplementedError

    def __repr__(self):
        return f"<Battle: {self.player_1} vs {self.player_2}>"
