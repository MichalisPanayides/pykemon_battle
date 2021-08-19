import random
import time

# from .move import Move
from .pokemon import Pokemon


class Battle:
    """
    Class that contains the battle logic of the game
    """

    def __init__(self, team_size=6):
        self.get_team(team_size=team_size)

    def get_team(self, team_size=6):
        """
        Build the team of the player
        """
        self.team = []
        # TODO: Implement the multiple move selections
        # move_selection = input(
        #     "Your team's moveset will be selected: "
        #     "\n1: Automatic"
        #     "\n2: Manual"
        #     "\n3: Random"
        #     "\nAnswer : "
        # )
        move_selection = "random"
        for team_index in range(team_size):
            current_pokemon = None
            while current_pokemon is None:
                pokemon_id = input(f"Choose pokemon {team_index + 1} by id or name: ")
                try:
                    current_pokemon = Pokemon(pokemon_id)
                except ValueError:
                    print("Invalid input")
                    continue
            current_pokemon.get_moves(move_selection=move_selection)
            self.team.append(current_pokemon)

    def choose_dificulty(self):
        """
        Choose the difficulty of the battle
        """
        # TODO: Implent all the difficulities
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
                enemy_pokemon = Pokemon(random.randint(1, 386))
                enemy_pokemon.get_moves(move_selection="random")
                self.enemy_team.append(enemy_pokemon)
        else:
            raise NotImplementedError

    def apply_move(self, attacking_pokemon, defending_pokemon, move):
        """
        Apply the move to the enemy pokemon
        """
        move_damage = attacking_pokemon.moveset[move].stats["power"]
        if move_damage is None:
            move_damage = 0
        move_accuracy = attacking_pokemon.moveset[move].stats["accuracy"]
        if move_accuracy is None:
            move_accuracy = 100
        move_type = attacking_pokemon.moveset[move].stats["type"]
        if random.random() < (move_accuracy / 100):
            defending_pokemon.health_points = (
                defending_pokemon.health_points - move_damage
            )
            print(
                f"{attacking_pokemon} used {attacking_pokemon.moveset[move]} on {defending_pokemon} and did {move_damage} damage"
            )
        else:
            print(
                f"{attacking_pokemon} used {attacking_pokemon.moveset[move]} on {defending_pokemon} but it missed"
            )

        if defending_pokemon.health_points <= 0:
            time.sleep(1.5)
            print("\n")
            print(f"{defending_pokemon} fainted")
            defending_pokemon.health_points = 0
            defending_pokemon.fainted = True

        return defending_pokemon.health_points

    def start_battle(self):
        """
        Start the battle
        """
        print("Fetching enemy details")
        self.choose_dificulty()
        print("Your opponent is ready")
        time.sleep(1)

        print("Trainers. Prepare your teams:")
        time.sleep(2)
        print("3")
        time.sleep(0.8)
        print("2")
        time.sleep(0.8)
        print("1")
        time.sleep(1)
        print("FIGHT")
        time.sleep(1)

        player_remaining_pokemon = self.team.copy()
        enemy_remaining_pokemon = self.enemy_team.copy()

        player_pokemon = self.team[0]
        enemy_pokemon = self.enemy_team[0]

        if player_pokemon.stats["speed"] >= enemy_pokemon.stats["speed"]:
            player_turn = True
        else:
            player_turn = False

        while len(player_remaining_pokemon) > 0 and len(enemy_remaining_pokemon) > 0:
            print("\n")
            print(player_pokemon, " HP: ", player_pokemon.health_points)
            print(enemy_pokemon, " HP: ", enemy_pokemon.health_points)
            time.sleep(2)
            print("\n")
            if player_turn:
                print(player_pokemon, "'s turn:")
                time.sleep(1)
                for move in range(len(player_pokemon.moveset)):
                    print(move + 1, ": ", player_pokemon.moveset[move].name)
                print("\n")
                # TODO: Make sure player move is between 1 and 4
                player_move = int(input("Choose your move [1-4]: "))
                player_move -= 1
                print("\n")
                time.sleep(1)
                self.apply_move(player_pokemon, enemy_pokemon, player_move)
                time.sleep(2)
                print("\n")
                if enemy_pokemon.health_points <= 0:
                    enemy_remaining_pokemon.remove(enemy_pokemon)
                    if len(enemy_remaining_pokemon) > 0:
                        enemy_pokemon = enemy_remaining_pokemon[0]
                        print(f"Enemy chooses {enemy_pokemon}")
                        time.sleep(1)
                        print("\n")
                        print(player_pokemon, " VS ", enemy_pokemon)
                        time.sleep(1)
                    else:
                        enemy_pokemon = None
            else:
                print(enemy_pokemon, "'s turn:")
                time.sleep(1)
                enemy_move = random.randint(0, len(enemy_pokemon.moveset) - 1)
                print("\n")
                self.apply_move(enemy_pokemon, player_pokemon, enemy_move)
                print("\n")
                if player_pokemon.health_points <= 0:
                    player_remaining_pokemon.remove(player_pokemon)
                    if len(player_remaining_pokemon) > 0:
                        print("Which pokemon do you choose?")
                        time.sleep(0.7)
                        for i, poke in enumerate(player_remaining_pokemon):
                            print(i + 1, ": ", poke)
                            time.sleep(0.3)
                        poke_choice = int(input("Choose a pokemon: "))
                        poke_choice -= 1
                        player_pokemon = player_remaining_pokemon[poke_choice]
                        print(player_pokemon, " VS ", enemy_pokemon)
                        time.sleep(1)
                    else:
                        player_pokemon = None
            player_turn = not player_turn

        if len(player_remaining_pokemon) > 0:
            print("You won!")
        else:
            print("You lost!")
