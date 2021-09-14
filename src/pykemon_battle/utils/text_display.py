import os

import numpy as np
from rich.console import Console


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
    display_text(text=pokemon_1)
    display_text(text=health_bar_1)
    display_text(text=health_text_1)
    display_text(text="")
    display_text(text=pokemon_2)
    display_text(text=health_bar_2)
    display_text(text=health_text_2)


def clear_screen():
    """
    Function to clear the terminal
    """
    os.system("cls" if os.name == "nt" else "clear")


def display_text(
    text, user_input=False, style="bold white on black", include_arrow=True
):
    """
    Function to display text in the terminal
    """
    # if delete_line:
    #     sys.stdout.write("\033[K")  # Cursor up one line
    if user_input:
        custom_end = " "
    else:
        custom_end = "\n"
    py_console = Console(highlight=False, style=style)
    py_console.print(text, end=custom_end)
    if user_input:
        if include_arrow:
            out = py_console.input("▼")
        else:
            out = py_console.input("")
        py_console.print("\033[A", " " * (len(text) + 2), "\033[A")
        return out
    return None
