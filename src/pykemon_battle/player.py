import numpy as np

from .pokemon import Pokemon

TOTAL_POKEMON = 807


# TODO: Maybe break this class into two classes (Player and Team)?
class Player:
    """
    Creates a player object with a given team (or team size) and name

    Parameters
    ----------
    team : int or list, optional
        if int: get a random team of that size
        if list: use the list as the current Pokemon team
    name : str, optional
        The name of the player, by default "Ash"
    """

    def __init__(self, team=1, name="Ash"):
        self.name = name
        # TODO: Add upper bound to team size
        if isinstance(team, int) and team > 0:
            self.team = self.get_random_team(team)
        elif isinstance(team, list):
            self.check_that_team_is_valid(team)
            self.team = team
        else:
            raise TypeError("Team must be a list or an int")
        self.assign_party_positions()
        self.selected = self.team[0]

    def check_that_team_is_valid(self, team):
        """
        Check that the team is valid
        """
        if not isinstance(team, list):
            raise TypeError("team must be a list of Pokemon objects")
        for pokemon in team:
            if not isinstance(pokemon, Pokemon):
                raise TypeError("team entries must be Pokemon objects")

    def get_random_team(self, team_size):
        """
        Randomly generates a team of pokemon with a given team size
        """
        team = []
        for _ in range(team_size):
            pokemon = Pokemon(np.random.randint(1, TOTAL_POKEMON))
            pokemon.get_moves(move_selection="random")
            team.append(pokemon)
        return team

    def assign_party_positions(self):
        """
        Assigns the party positions of the team
        """
        for i, pokemon in enumerate(self.team):
            pokemon.party_position = i

    def get_team(self):
        """
        Returns the player's team of Pokemons
        """
        return self.team

    def __repr__(self):
        return f"Trainer {self.name}"
