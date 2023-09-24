import re
import time

import numpy as np
from rich.console import Console

from .pokemon import Pokemon
from .player import Player
from .utils import (
    show_health_bar,
    clear_screen,
    display_text,
    change_terminal_background,
    clear_background,
    display_text_for_pokemon_selection,
    display_welcome_message,
    start_terminal_slideshow,
)
from .battle import Battle

console = Console(highlight=False)
TOTAL_POKEMON = 898


def test_purposes():
    """
    Function for playtesting purposes
    """
    user = Player(team=[Pokemon(1), Pokemon(321), Pokemon(543)], name="Mixas")
    enemy = Player(team=3, name="Foe")
    for pokemon in user.team:
        pokemon.get_moves(move_selection="random")
    for pokemon in enemy.team:
        pokemon.get_moves(move_selection="random")
    return user, enemy


class Interface:
    """
    Class that contains the user interface
    """

    def __init__(self, terminal_change=False):
        self.terminal_change = terminal_change
        display_welcome_message()

        self.team_size = None
        self.team = None

        self.build_player()
        self.build_enemy(difficulty="random")

        # self.user, self.enemy = test_purposes()

        self.battle = Battle(player_1=self.user, player_2=self.enemy)

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

            if not isinstance(player_name, str) or len(player_name) <= 0:
                player_name = None

        self.choose_team_size()
        self.get_team()
        self.user = Player(team=self.team, name=player_name)

    def choose_team_size(self):
        """
        Choose the size of the team
        """
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
        if self.terminal_change:
            start_terminal_slideshow()

        with console.status("", spinner="aesthetic"):
            display_text("Fetching enemy details")
            if difficulty == "random":
                self.enemy = Player(team=len(self.user.team), name="Foe")
            else:
                # TODO: Implement all the difficulities
                raise NotImplementedError

            if self.terminal_change:
                time.sleep(2)
                clear_background()

        display_text(text="Your opponent is ready", user_input=True, animate=True)

    def choose_move(self):
        """
        Choose one of the 4 moves
        """
        is_move_selected = False
        display_text(text="Choose your move: \n")
        for count, move in enumerate(self.battle.player_1.selected.moveset):
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
                if (
                    self.battle.player_1.selected.moveset[selected_move].stats[
                        "pp_left"
                    ]
                    > 0
                ):
                    self.battle.player_1.selected.moveset[selected_move].stats[
                        "pp_left"
                    ] -= 1
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
        move_index = self.battle.attacker.moveset[move_outcome["move_index"]]
        display_text(
            text=f"{self.battle.attacker} used {move_index}",
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

    def choose_new_pokemon(self):
        """
        Actions to take when player's pokemon faints
        """
        new_pokemon_pos = display_text_for_pokemon_selection(self.battle)
        self.battle.switch_pokemon(player_turn=True, pokemon_pos=new_pokemon_pos)

        clear_screen()
        show_health_bar(
            pokemon_1=self.battle.player_1.selected,
            pokemon_2=self.battle.player_2.selected,
        )

    def interactive_battle(self):
        """
        Start the battle
        """
        # TODO: Maybe change everything to be object oriented
        # (i.e. instead of player_pokemon, use self.battle.player_1.selected)

        player_turn = (
            self.battle.player_1.selected.stats["speed"]
            >= self.battle.player_2.selected.stats["speed"]
        )

        end_battle = False
        while not end_battle:
            if not self.battle.player_1.selected.active:
                display_text(
                    text=f"{self.battle.player_1.selected} fainted!",
                    user_input=True,
                    animate=True,
                )
                self.choose_new_pokemon()
                print("\n")
                display_text(
                    text=f"Go {self.battle.player_1.selected}!",
                    user_input=True,
                    animate=True,
                )

            if not self.battle.player_2.selected.active:
                display_text(
                    text=f"{self.battle.player_2.selected} fainted!",
                    user_input=True,
                    animate=True,
                )
                new_pokemon_pos = np.random.choice(
                    [
                        poke
                        for poke in self.battle.player_2.team
                        if poke.health_points > 0
                    ]
                ).party_position
                self.battle.switch_pokemon(
                    player_turn=False, pokemon_pos=new_pokemon_pos
                )
                display_text(
                    text=f"Your opponent sent out {self.battle.player_2.selected}!",
                    user_input=True,
                    animate=True,
                )

            clear_screen()
            show_health_bar(
                pokemon_1=self.battle.player_1.selected,
                pokemon_2=self.battle.player_2.selected,
            )
            print("\n")

            if self.terminal_change:
                # TODO: Check if pokemon is in the terminal list otherwise keep black
                change_terminal_background(
                    self.battle.player_1.selected
                    if player_turn
                    else self.battle.player_2.selected
                )
            if player_turn:
                selected_move = self.choose_move()
                turn_outcome = self.battle.player_turn_logic(
                    selected_move=selected_move
                )
                self.display_move_outcome(move_outcome=turn_outcome)
            else:
                selected_move = np.random.randint(0, 4)
                turn_outcome = self.battle.enemy_turn_logic(selected_move=selected_move)
                self.display_move_outcome(move_outcome=turn_outcome)

            player_1_out_of_pokemon = (
                len([poke for poke in self.battle.player_1.team if poke.active]) <= 0
            )
            player_2_out_of_pokemon = (
                len([poke for poke in self.battle.player_2.team if poke.active]) <= 0
            )

            end_battle = player_1_out_of_pokemon or player_2_out_of_pokemon
            player_turn = not player_turn

        if player_1_out_of_pokemon and player_2_out_of_pokemon:
            display_text(
                "Somehow this is a tie! No special behaviour is implemented yet"
            )
        elif player_1_out_of_pokemon:
            display_text(
                text="You lost!",
                animate=True,
            )
        elif player_2_out_of_pokemon:
            display_text(
                text="You won!",
                animate=True,
            )
        else:
            raise ValueError("Invalid end battle condition")

        print("\n")
        if self.terminal_change:
            clear_background()
