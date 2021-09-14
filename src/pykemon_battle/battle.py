import random
import re

from rich.console import Console

# from .move import Move
from .pokemon import Pokemon
from .utils import (
    enemy_turn_logic,
    player_turn_logic,
    show_health_bar,
    clear_screen,
    display_text,
    change_terminal_background,
)

console = Console(highlight=False)
TOTAL_POKEMON = 898


class Battle:
    """
    Class that contains the battle logic of the game
    """

    def __init__(self, team_size=6):
        self.get_team(team_size=team_size)
        self.enemy_team = None

    def get_team(self, team_size=6):
        """
        Build the team of the player
        """
        self.team = []
        # TODO: Implement the multiple move selections
        move_selection = "random"
        for team_index in range(team_size):
            current_pokemon = None
            while current_pokemon is None:
                pokemon_id = display_text(
                    f"Choose pokemon {team_index + 1} by id or name:",
                    user_input=True,
                    include_arrow=False,
                    animate=True,
                )
                sanitized_pokemon_id = re.search(r"\d{1,3}$", pokemon_id)
                if sanitized_pokemon_id is not None:
                    if int(sanitized_pokemon_id.group()) in range(1, TOTAL_POKEMON + 1):
                        current_pokemon = Pokemon(int(sanitized_pokemon_id.group()))
                    else:
                        display_text(
                            f"Pokemon id should be between 1-{TOTAL_POKEMON}.",
                            user_input=True,
                            animate=True,
                        )
                else:
                    try:
                        current_pokemon = Pokemon(pokemon_id)
                    except ValueError:
                        display_text("Invalid input.", user_input=True, animate=True)
                        continue
            current_pokemon.get_moves(move_selection=move_selection)
            self.team.append(current_pokemon)

    def choose_dificulty(self):
        """
        Choose the difficulty of the battle
        """
        # TODO: Implement all the difficulities
        # diff = input(
        #     "Choose the difficulty: \n1: Random \n2: Easy \n3: Hard \nAnswer : "
        # )
        difficulty = "random"
        self.build_enemy_team(difficulty=difficulty)

    def build_enemy_team(self, difficulty):
        """
        Build the enemy team
        """
        if difficulty == "random":
            self.enemy_team = []
            for _ in range(len(self.team)):
                enemy_pokemon = Pokemon(random.randint(1, 151))
                enemy_pokemon.get_moves(move_selection="random")
                self.enemy_team.append(enemy_pokemon)
        else:
            raise NotImplementedError

    def start_battle(self, terminal_change=False):
        """
        Start the battle
        """
        clear_screen()
        with console.status("", spinner="aesthetic"):
            display_text("Fetching enemy details")
            self.choose_dificulty()
        display_text(text="Your opponent is ready", user_input=True, animate=True)

        player_remaining_pokemon = self.team.copy()
        enemy_remaining_pokemon = self.enemy_team.copy()

        player_pokemon = self.team[0]
        enemy_pokemon = self.enemy_team[0]

        player_turn = player_pokemon.stats["speed"] >= enemy_pokemon.stats["speed"]

        clear_screen()
        show_health_bar(pokemon_1=player_pokemon, pokemon_2=enemy_pokemon)
        print("\n")
        while len(player_remaining_pokemon) > 0 and len(enemy_remaining_pokemon) > 0:
            if terminal_change:
                change_terminal_background(player_pokemon)
            if player_turn:
                enemy_pokemon, enemy_remaining_pokemon = player_turn_logic(
                    player_pokemon, enemy_pokemon, enemy_remaining_pokemon
                )
            else:
                player_pokemon, player_remaining_pokemon = enemy_turn_logic(
                    player_pokemon, enemy_pokemon, player_remaining_pokemon
                )
            player_turn = not player_turn
            clear_screen()
            show_health_bar(pokemon_1=player_pokemon, pokemon_2=enemy_pokemon)
            print("\n")

        if len(player_remaining_pokemon) > 0:
            display_text("You won!")
        else:
            display_text("You lost!")
