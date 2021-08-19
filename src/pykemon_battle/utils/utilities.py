import random
import time

import numpy as np
import requests


def get_pokemon_info(poke_id, base_url="https://pokeapi.co/api/v2/pokemon/"):
    """
    Returns a dictionary of the pokemon's name, types, and abilities
    """
    req = requests.get(base_url + str(poke_id).lower())
    if req.status_code == 404:
        raise ValueError(f"The Pokemon with ID ({poke_id}) could not be found")
    return req.json()


def get_move_info(move_id, base_url="https://pokeapi.co/api/v2/move/"):
    """
    Returns a dictionary of the move's name, type, and damage
    """
    req = requests.get(base_url + str(move_id))
    if req.status_code == 404:
        raise ValueError(f"The move with ID ({move_id}) could not be found")
    return req.json()


def choose_best_moveset(all_moves):
    """
    Returns a tuple of the best moveset
    """
    raise NotImplementedError("Cannot choose best moveset. Not yet implemented")


def manually_choose_moveset(all_moves):
    """
    Allows the user to choose their moveset
    """
    all_moves_names = [move_i["move"]["name"] for move_i in all_moves]
    print("Here is a list of all available moves for this Pokemon: ")
    print(all_moves_names)
    moveset = tuple()
    while len(moveset) < 4:
        move = input(f"Move {len(moveset) + 1} : ")
        if move in all_moves_names and move not in moveset:
            moveset += (move,)

    return moveset


def randomly_choose_moveset(all_moves):
    """
    Returns a tuple of four moves
    """
    moveset = np.random.choice(all_moves, 4)
    moveset = tuple(move["move"]["name"] for move in moveset)

    return moveset


def choose_first_four_moves_for_now(all_moves):
    """
    Returns a tuple of four moves
    """
    moveset = tuple(move["move"]["name"] for move in all_moves[:4])
    return moveset


def apply_move(attacking_pokemon, defending_pokemon, move):
    """
    Apply the move to the enemy pokemon
    """
    move_damage = attacking_pokemon.moveset[move].stats["power"]
    if move_damage is None:
        move_damage = 0
    move_accuracy = attacking_pokemon.moveset[move].stats["accuracy"]
    if move_accuracy is None:
        move_accuracy = 100
    # move_type = attacking_pokemon.moveset[move].stats["type"]
    if random.random() < (move_accuracy / 100):
        defending_pokemon.health_points = defending_pokemon.health_points - move_damage

        print(
            f"{attacking_pokemon} used {attacking_pokemon.moveset[move]} on "
            f"{defending_pokemon} and did {move_damage} damage"
        )
    else:
        print(
            f"{attacking_pokemon} used {attacking_pokemon.moveset[move]} on "
            f"{defending_pokemon} but it missed"
        )

    if defending_pokemon.health_points <= 0:
        time.sleep(1.5)
        print("\n")
        print(f"{defending_pokemon} fainted")
        defending_pokemon.health_points = 0
        defending_pokemon.fainted = True

    return defending_pokemon.health_points


def player_turn_logic(player_pokemon, enemy_pokemon, enemy_remaining_pokemon):
    """
    Logic of the player turn
    """
    print(player_pokemon, "'s turn:")
    time.sleep(1)
    for count, move in enumerate(player_pokemon.moveset):
        print(count + 1, ": ", move)
        time.sleep(0.3)
    print("\n")
    # TODO: Make sure player move is between 1 and 4
    player_move = int(input("Choose your move [1-4]: "))
    player_move -= 1
    print("\n")
    time.sleep(1)
    apply_move(player_pokemon, enemy_pokemon, player_move)
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
