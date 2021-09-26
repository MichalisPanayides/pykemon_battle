import numpy as np

from .pokemon import Pokemon

TOTAL_POKEMON = 807


def check_that_team_is_valid(team):
    """
    Check that the team is valid
    """
    error_message = "Team must be a list of Pokemon objects"
    if type(team) is not list:
        raise TypeError(error_message)
    for pokemon in team:
        if not isinstance(pokemon, Pokemon):
            raise TypeError(error_message)


class Player:
    def __init__(self, name="Stefanos", team=1):
        self.name = name
        if isinstance(team, int):
            self.get_random_team(team)
        elif isinstance(team, list):
            check_that_team_is_valid(team)
            self.team = team
        else:
            raise TypeError("Team must be a list or an int")

    def get_random_team(self, team_size):
        """
        Randomly generates a team of pokemon
        """
        self.team = []
        for _ in range(team_size):
            pokemon = Pokemon(np.random.randint(1, TOTAL_POKEMON))
            pokemon.get_moves(move_selection="random")
            self.team.append(pokemon)

    def get_team(self):
        return self.team

    def __repr__(self):
        return f"{self.name}"


if __name__ == "__main__":
    print(Player())
