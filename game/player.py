from _types import Item, Equippable

import random
import config


with open('./names.txt') as f:
    NAMES = f.readlines()
DIRECTIONS = ['North', 'East', 'South', 'West']

_default_stats = {
    'ATK': 5,
    'DEF': 5,
    'HP': 50,
    'MAX_WEIGHT': 70,
    'XP_REMAINING': 45
}

class Equipped:
    mainhand: Equippable = None
    offhand: Equippable = None
    head: Equippable = None
    hands: Equippable = None
    chest: Equippable = None
    legs: Equippable = None
    _list: list[str] = []


class Character:
    _inventory: dict[str, list[Item, Equippable]]
    _stats: dict[str, int]
    _equipment: Equipped
    def __init__(self, name: str = None, _custom: bool = False, _seed: float = None):
        random.seed(_seed or config.fixedseed)
        self.name = name or random.choice(NAMES)
        self._equipment = Equipped()
        self._inventory = {}
        if _custom:
            self._stats = {}
            self.setup_combat()
            self.setup_hp()
        else:
            self._stats = config._default_player_stats

    def _unequip(self, item: Equippable):
        setattr(self._equipment, item.slots, None)
        self._equipment._list.remove(item.name)
        for stat, value in item.stats.items():
            self._stats[stat] -= value

    def _equip(self, item: Equippable):
        setattr(self._equipment, item.slots, item)
        self._equipment._list.append(item.name)
        for stat, value in item.stats.items():
            self._stats[stat] += value

    def setup_combat(self):
        numbers = [random.randint(1, 15) for _ in range(2)]
        big, smol = max(numbers), min(numbers)
        self.rerolls = 3
        print(f"You got {big} and {smol}, which would you like to assign {big} to, or would you like to reroll? ({self.rerolls} remaining.)")
        opt = input("ATK or DEF? : ").lower().strip()
        if opt == 'reroll':
            self.rerolls -= 1
            self.setup_combat()
        if opt == 'atk':
            self._stats['ATK'] = big
            self._stats['DEF'] = smol
        if opt == 'def':
            self._stats['DEF'] = big
            self._stats['ATK'] = smol
        print(f"Alright, {opt} set to {big} and {['atk', 'def'].remove(opt)[0]} set to {smol}.")

    def setup_hp(self):
        value = random.randint(35, 60)
        print(f"You got {value} for HP, want to keep or reroll? ({self.rerolls} remaining).")
        opt = input("Keep or reroll? : ").lower().strip()
        if opt == "reroll":
            self.rerolls -= 1
            self.setup_hp()
        if opt == "keep":
            self._stats['HP'] = value
        print(f"Alright, HP set to {value}.")

    def take(self, item: Item):
        if self._inventory.get(item.name):
            self._inventory[item.name][1] += 1
            print(f"You take the {item.name}, you now have {self._inventory[item.name][1]} {item.name}s.")
        else:
            self._inventory[item.name] = [item, 1]
            print(f"You take the {item.name}.")

    def equip(self, item_name: str):
        item = self._inventory.get(item_name)
        if isinstance(item, Equippable):
            self._equip(item)
            return
        print(f"{item_name} isn't equippable.")

    def unequip(self, item_name: str):
        item = self._inventory.get(item_name)
        if item_name in self._equipment._list:
            self._unequip(item)

    @property
    def value(self) -> int:
        return sum([item.value for item in list(self._inventory.values())])

    @property
    def bag(self) -> str:
        return ', '.join(map(str, self._inventory.values()))
