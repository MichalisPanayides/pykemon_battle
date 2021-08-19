import pykemon_battle as pkmn


def test_Pokemon():
    Weedle = pkmn.Pokemon("weedle")
    assert Weedle.name == "weedle"
    assert Weedle.type == "bug"
    assert Weedle.health_points == 40
    assert Weedle.stats["attack"] == 35
    assert Weedle.stats["defense"] == 30
    assert Weedle.stats["speed"] == 50
