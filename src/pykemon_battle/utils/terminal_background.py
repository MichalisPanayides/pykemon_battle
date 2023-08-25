import os
import subprocess

from .constants import TERMINAL_BACKGROUND_CORRECTIONS


def change_terminal_background(pokemon):
    """
    Change the terminal background based on the pokemon's name.
    """
    if pokemon.json["id"] <= 719:
        corrected_poke_name = pokemon.name
        if pokemon.name in TERMINAL_BACKGROUND_CORRECTIONS:
            corrected_poke_name = TERMINAL_BACKGROUND_CORRECTIONS[pokemon.name]
        os.system(f"pokemon {corrected_poke_name}")


def start_terminal_slideshow(speed=0.001):
    """
    Start the terminal slideshow.
    """
    with subprocess.Popen(
        f"pokemon -d 0.25 -ne -ss {speed}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as proc:
        try:
            proc.wait(timeout=20)
        except subprocess.TimeoutExpired as exc:
            proc.kill()
            raise RuntimeError("Enemy pokemon selection timed out.") from exc


def clear_background():
    """
    Clear the terminal background.
    """
    os.system("pokemon -c")
