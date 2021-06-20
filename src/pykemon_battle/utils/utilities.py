import numpy as np
import random
import requests


def get_pokemon_info(poke_id, base_url="https://pokeapi.co/api/v2/pokemon/"):
    r = requests.get(base_url + str(poke_id).lower())
    if r.status_code == 404:
        raise ValueError(f"The Pokemon with ID ({poke_id}) could not be found")
    return r.json()


def get_move_info(move_id, base_url="https://pokeapi.co/api/v2/move/"):
    r = requests.get(base_url + str(move_id))
    if r.status_code == 404:
        raise ValueError(f"The move with ID ({move_id}) could not be found")
    return r.json()


def choose_best_moveset(all_moves):
    raise NotImplementedError("Cannot choose best moveset. Not yet implemented")


def manually_choose_moveset(all_moves):
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
    moveset = np.random.choice(all_moves, 4)
    moveset = tuple(move["move"]["name"] for move in moveset)

    return moveset


def choose_first_four_moves_for_now(all_moves):
    moveset = tuple(move["move"]["name"] for move in all_moves[:4])
    return moveset
