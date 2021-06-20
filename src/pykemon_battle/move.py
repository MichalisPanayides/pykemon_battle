from .utils import get_move_info


class Move:
    def __init__(self, move_name):
        self.json = get_move_info(move_name)
        self.name = self.json["name"]
        self.type = self.json["type"]["name"]
        self.power = self.json["power"]
        self.total_pp = self.json["pp"]
        self.pp_left = self.total_pp
        self.accuracy = self.json["accuracy"]
        self.priority = self.json["priority"]
        self.target = self.json["target"]["name"]

        # Should these be in? Investigate
        self.damage_class = self.json["damage_class"]["name"]
        self.effect_chance = self.json["effect_chance"]
        self.effect_changes = self.json["effect_changes"]
        self.effect_entries = self.json["effect_entries"]  # [-1]["effect"]
        self.stat_changes = self.json["stat_changes"]

    def __repr__(self):
        return f"{self.name.capitalize()}"
