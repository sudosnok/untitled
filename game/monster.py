from bisect import bisect_left
import random

import config
from _types import Item, Container

c = Container(_seed=config.fixedseed)

class Monster:
    def __init__(self, stats: dict[str, int] = None, _seed: float = None, _loot: list[Item] = None):
        random.seed(_seed or config.fixedseed)
        self._stats = stats or config._default_monster_stats
        self._loot = self._get_loot(_loot)
        self._dead = False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__.lower()}: stats={self._stats}"

    def _get_loot(self, _loot: list[Item] = None):
        if not _loot:
            rnum = random.randint(0, 100)
            if rnum < self._stats['LOOTVAL']:
                self._loot = c.get_one()
                return
        self._loot = _loot

    def _get_state(self) -> str:
        if not self.dead:
            hp_perc = int((self._stats['HP']/self._stats['MAX_HP'])* 100)
            breakpoints = (20, 40, 60, 80)
            results: tuple[str] = config.monster_states
            i = bisect_left(breakpoints, hp_perc)
            return results[i]
        return "Dead and cold."

    def take_damage(self, damage: int):
        if self._stats['HP'] > damage:
            print(f"{self.__class__.__name__.lower()} took {damage} damage!")
            self._stats['HP'] -= damage
            print(self._get_state)
            return
        print(f"{self.__class__.__name__.lower()} has died!")
        self.dead = True

class Zombie(Monster):
    def __init__(self, *args, **kwargs):
        super().__init__(stats=config._default_zombie_stats, *args, **kwargs)

class Witch(Monster):
    def __init__(self, *args, **kwargs):
        super().__init__(stats=config._default_witch_stats, *args, **kwargs)
