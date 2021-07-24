import random
import json

import config

class Item:
    name: str
    id: int
    value: int

    def __repr__(self) -> str:
        return f'{self.name.title()}, id={self.id}'

    def __str__(self) -> str:
        return self.name.title()

    @classmethod
    def from_dict(cls, data):
        self = cls()
        {setattr(self, name, value) for name, value in data.items()}
        return self

class Equippable(Item):
    name: str
    id: int
    value: int
    slots: str
    stats: dict[str, int]


class Container:
    _items: list[Item]
    def __init__(self, _seed: float = None):
        random.seed(_seed or config.fixedseed)
        with open('./items.json') as f:
            data = json.load(f)
        self._items = [Item.from_dict(d) for d in data]
        with open('./equipment.json') as f:
            data = json.load(f)
        self._items.extend([Equippable.from_dict(d) for d in data])
        self._items.extend([Equippable.from_dict(d) for d in data])
        random.shuffle(self._items)
    def get_one(self):
        return random.choice(self._items)
    def get(self) -> list[Item]:
        return random.choices(self._items, k=random.randint(0, 2))

    
