# TODO: Implement Team class (connected with todo in player.py line 8)
# TODO: Remove all pylint exceptions
class Team:
    # pylint: disable=too-few-public-methods
    """
    A class for a particular team of pokemon
    """

    def __init__(
        self,
        pokemon_1,
        pokemon_2=None,
        pokemon_3=None,
        pokemon_4=None,
        pokemon_5=None,
        pokemon_6=None,
    ):
        # pylint: disable=too-many-arguments
        self.team = [pokemon_1, pokemon_2, pokemon_3, pokemon_4, pokemon_5, pokemon_6]
