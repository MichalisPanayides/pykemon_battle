from .utils.utilities import (
    get_pokemon_info,
    choose_best_moveset,
    randomly_choose_moveset,
    manually_choose_moveset,
    choose_first_four_moves_for_now,
)

from .move import Move


class Pokemon:
    """
    A pokemon is a class that represents a pokemon.
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, poke_id):
        self.json = get_pokemon_info(poke_id=poke_id)
        self.name = self.json["name"]
        self.type = list(slot["type"]["name"] for slot in self.json["types"])
        self.health_points = None
        self.active = None

        self.stats = {}
        self.volatile_status = {}
        self.volatile_battle_status = {}
        self.non_volatile_status = {}
        self.moveset = None

        self.heal()
        self.reset_stats()

        # self.get_moves()

    def reset_stats(self):
        """
        Resets the pokemon's health points to its base stat.

        Possible values for volatile status:
            "arena_trap": False,
            "bound": False,
            "confusion": False,
            "curse": False,
            "drowsy": False,
            "embargo": False,
            "encore": False,
            "flinch": False,
            "heal_block": False,
            "identified": False,
            "infactuation": False,
            "leech_seed": False,
            "nightmare": False,
            "perish_song": False,
            "taunted": False,
            "telekinisis": False,
            "torment": False,
            "type_change": False,

        Possible values for volatile battle status:
            "Aqua Ring": False,
            "Bracing": False,
            "Charging turn": False,
            "Center of attention": False,
            "Defense Curl": False,
            "Rooting": False,
            "Magic Coat": False,
            "Magnetic levitation": False,
            "Mimic": False,
            "Minimize": False,
            "Protection": False,
            "Recharging": False,
            "Semi-invulnerable turn": False,
            "Substitute": False,
            "Taking aim": False,
            "Thrashing": False,
            "Transformed": False,
        """

        attack = self.json["stats"][1]["base_stat"]
        defense = self.json["stats"][2]["base_stat"]
        special_attack = self.json["stats"][3]["base_stat"]
        special_defense = self.json["stats"][4]["base_stat"]
        speed = self.json["stats"][5]["base_stat"]

        # TODO: Implement volatile status
        self.volatile_status = {}
        # TODO: Implement volatile battle status
        self.volatile_battle_status = {}

        self.stats = {
            "attack": attack,
            "defense": defense,
            "special_attack": special_attack,
            "special_defense": special_defense,
            "speed": speed,
            "accuracy": 100,
        }

    def heal(self):
        """
        Heals the pokemon to its base stat.

        The active status is set to False if the pokemon is fainted.
        Possible values for non-volatile status:
        self.health
            paralyzed, asleep, burned, poisoned
        """
        self.health_points = self.json["stats"][0]["base_stat"]
        self.non_volatile_status = None
        self.active = True

    def get_moves(self, move_selection="Random"):
        """
        Returns a list of moves that the pokemon can use.
        """
        all_possible_moves = self.json["moves"]
        if move_selection == "1" or move_selection.lower() == "automatic":
            selected_moves = choose_best_moveset(all_possible_moves)
        elif move_selection == "2" or move_selection.lower() == "manual":
            selected_moves = manually_choose_moveset(all_possible_moves)
        elif move_selection == "3" or move_selection.lower() == "random":
            selected_moves = randomly_choose_moveset(all_possible_moves)
        else:
            selected_moves = choose_first_four_moves_for_now(all_possible_moves)

        self.moveset = (
            Move(selected_moves[0]),
            Move(selected_moves[1]),
            Move(selected_moves[2]),
            Move(selected_moves[3]),
        )

    def __repr__(self):
        return f"{self.name.capitalize()}"
