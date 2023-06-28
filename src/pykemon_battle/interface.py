import re
import time

import numpy as np
from rich.console import Console

from .pokemon import Pokemon
from .player import Player
from .utils import (
    # enemy_turn_logic,
    # player_turn_logic,
    show_health_bar,
    clear_screen,
    display_text,
    change_terminal_background,
    clear_background,
)
from .battle import Battle

console = Console(highlight=False)
TOTAL_POKEMON = 898


class Interface:
    """
    Class that contains the user interface
    """

    def __init__(self):
        # self.display_welcome_message()
        self.build_player()
        self.build_enemy(difficulty="random")
        self.battle = Battle(player_1=self.user, player_2=self.enemy)

    def display_welcome_message(self):
        """
        Welcome message
        """
        display_text(
            text="Welcome to Pykemon Battle",
            user_input=True,
            include_arrow=True,
            animate=True,
        )

    def build_player(self):
        """
        Build the player for the user
        """
        player_name = None
        while player_name is None:
            player_name = display_text(
                text="Choose Trainer name:",
                user_input=True,
                include_arrow=False,
                animate=True,
            )
            if type(player_name) != str or len(player_name) <= 0:
                player_name = None

        self.choose_team_size()
        self.get_team()
        self.user = Player(team=self.team, name=player_name)

    def choose_team_size(self):
        team_size = None
        while team_size is None:
            team_size = display_text(
                text="Choose team size:",
                user_input=True,
                include_arrow=False,
                animate=True,
            )
            if team_size.isdigit() and int(team_size) in range(1, 7):
                team_size = int(team_size)
            else:
                display_text(
                    text="Team size should be an integer between 1 and 6.",
                    user_input=True,
                    animate=True,
                    include_arrow=True,
                )
        self.team_size = team_size

    def get_team(self):
        """
        Build the team of the player
        """
        self.team = []
        # TODO: Implement the multiple move selections
        for team_index in range(self.team_size):
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
            current_pokemon.get_moves(move_selection="random")
            self.team.append(current_pokemon)

    def build_enemy(self, difficulty):
        """
        Build the enemy team
        """
        self.enemy_team = []
        with console.status("", spinner="aesthetic"):
            display_text("Fetching enemy details")
            # TODO: Implement all the difficulities
            if difficulty == "random":
                for _ in range(len(self.team)):
                    enemy_pokemon = Pokemon(np.random.randint(1, 152))
                    enemy_pokemon.get_moves(move_selection="random")
                    self.enemy_team.append(enemy_pokemon)
            else:
                raise NotImplementedError
            self.enemy = Player(team=self.enemy_team, name="Foe")
        display_text(text="Your opponent is ready", user_input=True, animate=True)

    def choose_move(self, player_pokemon):
        """
        Choose one of the 4 moves
        """
        is_move_selected = False
        display_text(text="Choose your move: \n")
        for count, move in enumerate(player_pokemon.moveset):
            display_text(
                text=f"{count + 1} : {move} \n \t "
                + f"{move.stats['pp_left']}/{move.stats['total_pp']}",
            )
            time.sleep(0.2)
        display_text(text="")
        while not is_move_selected:
            selected_move_string = display_text(
                text="Choose your move [1-4]: ",
                user_input=True,
                include_arrow=False,
                animate=True,
            )
            possible_selections = [str(move_no) for move_no in range(1, 5)]
            if selected_move_string in possible_selections:
                selected_move = int(selected_move_string) - 1
                if player_pokemon.moveset[selected_move].stats["pp_left"] > 0:
                    player_pokemon.moveset[selected_move].stats["pp_left"] -= 1
                    is_move_selected = True
                else:
                    display_text(
                        text="There's no PP left", user_input=True, animate=True
                    )
            else:
                display_text(text="Invalid move choice", user_input=True, animate=True)
        return selected_move

    def display_move_outcome(self, move_outcome):
        """
        After a move is selected, display the outcome of the move
        """
        display_text(
            text=f"{self.battle.attacker} used {self.battle.attacker.moveset[move_outcome['move_index']]}",
            user_input=True,
            animate=True,
        )


        if move_outcome["success"]:
            if move_outcome["modifier"] == 1:
                display_text(
                    text=f"It's effective! (Damage: {move_outcome['damage']})",
                    user_input=True,
                    animate=True,
                )
            elif move_outcome["modifier"] >= 2:
                display_text(
                    text=f"It's super effective! (Damage: {move_outcome['damage']})",
                    user_input=True,
                    animate=True,
                )
            elif 0 < move_outcome["modifier"] <= 0.5:
                display_text(
                    text=f"It's not very effective! (Damage: {move_outcome['damage']})",
                    user_input=True,
                    animate=True,
                )
            elif move_outcome["modifier"] == 0:
                display_text(
                    text=f"But it failed! (Damage: {move_outcome['damage']})",
                    user_input=True,
                    animate=True,
                )
            else:
                raise ValueError("Invalid modifier value")
        else:
            display_text(text="Attack missed!", user_input=True, animate=True)
    

    def pokemon_fainted():
        pass


    def interactive_battle(self, terminal_change=False):
        """
        Start the battle
        """
        clear_screen()

        # TODO: Need something like the next line?
        # print([i.fainted for i in self.battle.player_1.team if i.non_volatile_status == "active"])

        player_remaining_pokemon = self.team.copy()
        enemy_remaining_pokemon = self.enemy_team.copy()

        # TODO: Maybe change everything to be object oriented
        # (i.e. instead of player_pokemon, use self.battle.player_1.selected)
        player_pokemon = self.team[0]
        enemy_pokemon = self.enemy_team[0]

        player_turn = player_pokemon.stats["speed"] >= enemy_pokemon.stats["speed"]

        clear_screen()
        show_health_bar(pokemon_1=player_pokemon, pokemon_2=enemy_pokemon)
        print("\n")
        while len(player_remaining_pokemon) > 0 and len(enemy_remaining_pokemon) > 0:
            if terminal_change:
                change_terminal_background(
                    player_pokemon if player_turn else enemy_pokemon
                )
            if player_turn:
                selected_move = self.choose_move(player_pokemon)
                turn_outcome = self.battle.player_turn_logic(selected_move=selected_move)
                self.display_move_outcome(move_outcome=turn_outcome)
                # if player_pokemon.non_volatile_status == "fainted":
                #     player_remaining_pokemon.remove(player_pokemon)
                #     if len(player_remaining_pokemon) > 0:
                #         self.battle.switch_pokemon(player_turn=True, pokemon_pos=0)
            else:
                selected_move = np.random.randint(0, 4)
                turn_outcome = self.battle.enemy_turn_logic(selected_move=selected_move)
                self.display_move_outcome(move_outcome=turn_outcome)

            if self.battle.player_1.selected is None:
                new_pokemon_selected = False
                while not new_pokemon_selected:
                    new_pokemon_pos = display_text(
                        text="Choose new pokemon:",
                        user_input=True,
                        include_arrow=False,
                        animate=True,
                    )
                self.battle.switch_pokemon(player_turn=True, pokemon_pos=new_pokemon_pos)
            
            if self.battle.player_2.selected is None:
                new_pokemon_pos = np.random.choice(
                    [
                        i
                        for i in range(len(enemy_remaining_pokemon))
                        if enemy_remaining_pokemon[i].non_volatile_status == "active"
                    ]
                )
                self.battle.switch_pokemon(player_turn=False, pokemon_pos=new_pokemon_pos)
            
            player_turn = not player_turn
            clear_screen()
            show_health_bar(pokemon_1=player_pokemon, pokemon_2=enemy_pokemon)
            print("\n")

        if len(player_remaining_pokemon) > 0:
            display_text("You won!")
        else:
            display_text("You lost!")

        if terminal_change:
            clear_background()
