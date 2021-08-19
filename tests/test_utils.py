import pykemon_battle as pkm


def test_get_pokemon_info():
    pidgey_json = pkm.utils.get_pokemon_info("Pidgey")
    assert pidgey_json["name"] == "pidgey"
    assert pidgey_json["height"] == 3
    assert pidgey_json["weight"] == 18


def test_get_move_info():
    tackle_json = pkm.utils.get_move_info("tackle")
    assert tackle_json["name"] == "tackle"
    assert tackle_json["type"]["name"] == "normal"
    assert tackle_json["power"] == 40


def test_choose_best_moveset():
    pass


def test_manually_choose_moveset():
    pass


def test_randomly_choose_moveset():
    pass


def test_choose_first_four_moves_for_now():
    pass
