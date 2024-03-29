import numpy as np
import requests
import requests_cache

requests_cache.install_cache("pykemon_cache", backend="sqlite", expire_after=600)


def get_pokemon_info(poke_id, base_url="https://pokeapi.co/api/v2/pokemon/"):
    """
    Returns a dictionary of the pokemon's name, types, and abilities
    """
    req = requests.get(base_url + str(poke_id).lower(), timeout=15)
    if req.status_code == 404:
        raise ValueError(f"The Pokemon with ID ({poke_id}) could not be found")
    return req.json()


def get_move_info(move_id, base_url="https://pokeapi.co/api/v2/move/"):
    """
    Returns a dictionary of the move's name, type, and damage
    """
    req = requests.get(base_url + str(move_id), timeout=15)
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
    # TODO: Add replace=False
    moveset = np.random.choice(all_moves, 4)
    moveset = tuple(move["move"]["name"] for move in moveset)

    return moveset


def choose_first_four_moves_for_now(all_moves):
    """
    Returns a tuple of four moves
    """
    moveset = tuple(move["move"]["name"] for move in all_moves[:4])
    return moveset


# def check_that_team_is_valid(team):
#     """
#     Check that the team is valid
#     """
#     if type(team) is not list:
#         raise TypeError("team must be a list of Pokemon objects")
#     for pokemon in team:
#         if not isinstance(pokemon, Pokemon):
#             raise TypeError("team entries must be Pokemon objects")


# def get_random_team(team_size):
#     """
#     Randomly generates a team of pokemon with a given team size
#     """
#     team = []
#     for _ in range(team_size):
#         pokemon = Pokemon(np.random.randint(1, TOTAL_POKEMON))
#         pokemon.get_moves(move_selection="random")
#         team.append(pokemon)
#     return team
