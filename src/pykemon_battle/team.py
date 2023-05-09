class Team:
    def __init__(
        self,
        pokemon_1,
        pokemon_2=None,
        pokemon_3=None,
        pokemon_4=None,
        pokemon_5=None,
        pokemon_6=None,
    ):
        """
        A class for a particular team of pokemon
        """
        self.team = [pokemon_1, pokemon_2, pokemon_3, pokemon_4, pokemon_5, pokemon_6]
