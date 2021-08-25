import random
import time


def apply_move(attacking_pokemon, defending_pokemon, move):
    """
    Apply the move to the enemy pokemon
    """
    move_power = attacking_pokemon.moveset[move].stats["power"]
    if move_power is None:
        move_power = 0
    move_accuracy = attacking_pokemon.moveset[move].stats["accuracy"]
    if move_accuracy is None:
        move_accuracy = 100
    move_type = attacking_pokemon.moveset[move].stats["type"]
    if random.random() < (move_accuracy / 100):
        defending_pokemon.health_points = defending_pokemon.health_points - move_power
        print(
            f"{attacking_pokemon} used {attacking_pokemon.moveset[move]} on "
            f"{defending_pokemon} and did {move_power} damage"
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
