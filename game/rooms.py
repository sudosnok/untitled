from typing import Optional
from _types import Item, Container
from player import Character
import config


import json
import random
import re
import time


DIRECTIONS = ['North', 'East', 'South', 'West']

_item_re = re.compile(r'(\<[\w-]+\>)')

def iter_replace(repl, target):
    new = _item_re.sub(repl, target)
    while _item_re.findall(new):
        new = _item_re.sub(repl, new)
    return new

class Room:
    _items: dict[str, Item] = {}
    _paths: list[str]
    _description: str
    _id: int

    def __init__(self, *args, **kwargs):
        self._id = kwargs.get('_id')
        self._data = _data = kwargs.pop('data')
        _temp_directions = DIRECTIONS.copy()
        paths = random.choice(_temp_directions)
        _temp_directions.remove(paths)
        extra_paths = random.choices(_temp_directions, k=random.randint(0, 3))
        paths = list(set([paths] + extra_paths))
        self._paths = paths
        self._description = random.choice(_data.get('rooms'))
        self.replace()
        self._populate_items(kwargs.pop('items'))

    def __str__(self) -> str:
        if len(self._description) >= 50:
            return f'<Room: id={self._id}; items={self.items}; {self._description[:50]}...'
        return f'<Room: id={self._id}; items={self.items}; {self._description}...'

    def __repr__(self) -> str:
        return f'Room: id={self._id}'

    def _populate_items(self, items: list[Item]):
        self._items = {i.name: i for i in items}

    def try_get_item(self, item_name: str) -> Optional[Item]:
        if (item := self._items.get(item_name)):
            return item
        return None

    @property
    def items(self) -> list[Item]:
        return list(self._items.values())

    @property
    def paths(self) -> list[str]:
        return self._paths

    @property
    def describe(self) -> str:
        return self._description

    def itemreplace(self, match: re.Match) -> str:
        ret = random.choice(self._data.get(match.group(0).strip('<>')))
        return ret

    def replace(self):
        self._description = iter_replace(self.itemreplace, self._description)


class Dungeon:
    _room_map: dict[str, Room]
    _start_room: Room
    _current_room: Room
    _previous_room: None
    _items: Container
    _player: Character

    def __init__(self, depth: int = 2, name: str = None, _custom: bool = False, _seed: float = None):
        random.seed(_seed or config.fixedseed)
        if not (0 < depth < 10):
            raise NotImplemented

        self._player = Character(name=name, _custom=_custom, _seed=_seed)
        self._items = Container(_seed=_seed)
        self._room_map = {}
        self._ctr = 0

        with open('./rooms.json') as f:
            self._data = json.load(f)

        self._current_room = self._start_room = Room(data=self._data, _id=0, items=self._items.get())
        self._ctr += 1
        for d in self._start_room.paths:
            self._room_map[d] = Room(data=self._data, _id=self._ctr, items=self._items.get())
            self._ctr += 1

    def move(self, direction: str):
        direction = direction.title()
        if direction in DIRECTIONS and direction in self._current_room._paths:
            self._previous_room = self._current_room #hold the previous room
            self._current_room = self._room_map[direction] # get the next (now current) room
            _prev_direction = DIRECTIONS[(DIRECTIONS.index(direction) + 2) % 4]
            # add half the length of the list to the idx of the direction and use mod to wrap over the top of the list
            self._room_map = {} #clear the map
            for d in self._current_room.paths: #for each direction the room can go, make a room
                self._room_map[d] = Room(data=self._data, _id=self._ctr, items=self._items.get())
                self._ctr += 1
            self._room_map[_prev_direction] = self._previous_room # dont override the previous direction
            if _prev_direction not in self._current_room._paths:
                self._current_room._paths.append(_prev_direction)
        else:
            return ValueError


