from .move import Move
from .pokemon import Pokemon


class Battle:
    def __init__(self, team_size=6):
        self.get_team(size=team_size)
        # self.choose_dificulty()

    def get_team(self, size=6):
        self.team = tuple()
        for team_index in range(size):
            pokemon_id = input(f"Choose pokemon {team_index + 1} by id or name")
            current_pokemon = Pokemon(pokemon_id)
            current_pokemon.get_moves()
            self.team += (current_pokemon,)

    def choose_dificulty(self):
        diff = input("easy", "medium", "hard", "impossible")
        return diff


New_Battle = Battle()
