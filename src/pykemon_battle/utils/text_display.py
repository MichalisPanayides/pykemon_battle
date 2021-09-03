import os
import time

import numpy as np


def pause_text(text_speed):
    if text_speed == "normal":
        time.sleep(1.5)
    if text_speed == "fast":
        time.sleep(0.8)


def show_health_bar(pokemon_1, pokemon_2):
    """
    Function to display health points of the battling pokemon
    """
    bar_1_length = int(np.ceil(pokemon_1.health_points / 3))
    bar_2_length = int(np.ceil(pokemon_2.health_points / 3))
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


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def wait_for_input(text):
    input(text)
