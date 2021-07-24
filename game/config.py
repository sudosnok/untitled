import bisect

fixedseed = 1626962216.96454
_default_player_stats = {
    'ATK': 5,
    'DEF': 5,
    'HP': 50,
    'MAX_WEIGHT': 70,
    'XP_REMAINING': 45
}
_default_monster_stats = {
    "ATK": 5,
    "DEF": 5,
    "HP": 15,
    "MAX_HP": 15,
    "LOOTVAL": 10
}
_default_zombie_stats = {
    "ATK": 7,
    "DEF": 2,
    "HP": 10,
    "MAX_HP": 10,
    "LOOTVAL": 15
}
_default_witch_stats = {
    "ATK": 6,
    "DEF": 4,
    "HP": 13,
    "MAX_HP": 13,
    "LOOTVAL": 20
}

monster_states = (
    "On deaths door, just sneeze on them",
    "Very injured, not far left to go",
    "Pretty rouged up but still fighting.",
    "A little hurt, but isn't going to die any time soon.",
    "Very healthy, maybe you should deal some damage to it!",
)
