import math
import random
import time

from .constants import TYPE_EFFECTS


def show_health_bar(pokemon_1, pokemon_2):
    """
    Function to display health points of the battling pokemon
    """
    bar_1_length = int(pokemon_1.health_points / 3)
    bar_2_length = int(pokemon_2.health_points / 3)
    health_text_1, health_text_2 = (
        f"HP: {pokemon_1.health_points}/{pokemon_1.json['stats'][0]['base_stat']} ",
        f"HP: {pokemon_2.health_points}/{pokemon_2.json['stats'][0]['base_stat']} ",
    )
    health_bar_1, health_bar_2 = "", ""
    for _ in range(bar_1_length):
        health_bar_1 += "#"
    for _ in range(bar_2_length):
        health_bar_2 += "#"
    print(pokemon_1)
    print(health_bar_1)
    print(health_text_1)
    print()
    print(pokemon_2)
    print(health_bar_2)
    print(health_text_2)


def choose_move(player_pokemon):
    """
    Choose one of the 4 moves
    """
    move_selected = False
    while not move_selected:
        for count, move in enumerate(player_pokemon.moveset):
            print(
                f"{count + 1} : {move} \n \t {move.stats['pp_left']}/{move.stats['total_pp']}"
            )
            time.sleep(0.3)
        print("\n")
        # TODO: Make sure player move is between 1 and 4
        selected_move = int(input("Choose your move [1-4]: "))
        selected_move -= 1
        if player_pokemon.moveset[selected_move].stats["pp_left"] > 0:
            player_pokemon.moveset[selected_move].stats["pp_left"] -= 1
            move_selected = True
        else:
            print("\n")
            print("There's no PP left")
            time.sleep(1)
    return selected_move


def damage_function(variables):
    """
    The damage that the attacking pokemon inflicts to the defending pokemon.
    The formula is as described by:
    https://www.math.miami.edu/~jam/azure/compendium/battdam.htm

    The variable dictionary has the following keys
    ----------
    level : int
        Attacker's level by default 50
    attack : int
        Attacker's attack stat
    power : int
        Power of the move
    defender_defense : int
        Defender's defense stat
    same_type : boolean
        True if move type is the same type as the attacking pokemon
    modifier : int, optional
        Modifier based on type effectveness, by default 10
    stochastic : int, optional
        A random number, by default random.randint(217, 255)
    """
    stab = 1.5 if variables["same_type_advantage"] else 1

    damage = math.floor((2 * variables["attacker_level"] / 5) + 2)
    damage *= variables["attacker_attack"] * variables["move_power"]
    damage = math.floor(damage / variables["defender_defense"])
    damage = math.floor(damage / 50)
    damage = math.floor(damage * stab)
    damage = math.floor(damage * variables["modifier"])
    damage *= variables["stochasticity"]
    damage /= 255

    return math.floor(damage)


def apply_move(attacking_pokemon, defending_pokemon, move):
    """
    Apply the move to the enemy pokemon
    """
    print(f"{attacking_pokemon} used {attacking_pokemon.moveset[move]}")
    print("\n")
    time.sleep(1)

    attack_variables = {}
    attack_variables["move_power"] = attacking_pokemon.moveset[move].stats["power"]
    attack_variables["move_type"] = attacking_pokemon.moveset[move].stats["type"]

    attack_variables["attacker_level"] = 50
    attack_variables["attacker_type"] = attacking_pokemon.type
    attack_variables["attacker_attack"] = attacking_pokemon.stats["attack"]

    attack_variables["defender_defense"] = defending_pokemon.stats["defense"]
    defender_type = defending_pokemon.type

    attack_variables["same_type_advantage"] = (
        attack_variables["move_type"] in attack_variables["attacker_type"]
    )
    type_effects = list(
        TYPE_EFFECTS[attack_variables["move_type"]][type_i] for type_i in defender_type
    )
    attack_variables["modifier"] = math.prod(type_effects)
    attack_variables["stochasticity"] = random.randint(217, 255)

    if attack_variables["move_power"] is not None:
        damage = damage_function(variables=attack_variables)
        move_accuracy = (
            attacking_pokemon.moveset[move].stats["accuracy"]
            if attacking_pokemon.moveset[move].stats["accuracy"] is not None
            else 100
        )
        if random.random() < (move_accuracy / 100):
            print(f"Damage: {damage}")
            print("\n")
            defending_pokemon.health_points = defending_pokemon.health_points - damage
            if attack_variables["modifier"] == 1:
                print("It's effective")
            elif attack_variables["modifier"] >= 2:
                print("It's supper effective!")
            elif 0 < attack_variables["modifier"] <= 0.5:
                print("It's not very effective!")
            elif attack_variables["modifier"] == 0:
                print("But it failed!")
            else:
                raise ValueError("Invalid modifier value")
        else:
            print("Attack missed!")
    else:
        print("Unfortunately this move has not been implemented yet. Sorry")
    print("\n")

    if defending_pokemon.health_points <= 0:
        time.sleep(1.5)
        show_health_bar(pokemon_1=attacking_pokemon, pokemon_2=defending_pokemon)
        print(f"{defending_pokemon} fainted")
        print("\n")
        defending_pokemon.health_points = 0
        defending_pokemon.stats = "inactive"
        defending_pokemon.fainted = True

    return defending_pokemon.health_points


def player_turn_logic(player_pokemon, enemy_pokemon, enemy_remaining_pokemon):
    """
    Logic of the player turn
    """
    print(player_pokemon, "'s turn:")
    time.sleep(1)
    selected_move = choose_move(player_pokemon)
    print("\n")
    time.sleep(1)
    apply_move(player_pokemon, enemy_pokemon, selected_move)
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
    return enemy_pokemon, enemy_remaining_pokemon


def enemy_turn_logic(player_pokemon, enemy_pokemon, player_remaining_pokemon):
    """
    Logic of the enemy turn
    """
    print(enemy_pokemon, "'s turn:")
    time.sleep(1)
    enemy_move = random.randint(0, len(enemy_pokemon.moveset) - 1)
    print("\n")
    apply_move(enemy_pokemon, player_pokemon, enemy_move)
    time.sleep(1)
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
    return player_pokemon, player_remaining_pokemon
