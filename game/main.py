from rooms import Dungeon, DIRECTIONS

import time


def _intro(_d: Dungeon):
    print("You find yourself in a room, no recollection of who you were before.\n")
    print(_d._current_room.describe + '\n')
    print(f"You can move : {', '.join(_d._current_room.paths)}.\n")
    print("'look around' to search the room for anything useful.")
    print("'move <cardinal>' to proceed in that direction.")

def handle_cmd(_d: Dungeon, cmd: str):
    cr = _d._current_room
    cmd = cmd.strip().lower()
#quit
    if cmd in ('q', 'quit', 'exit'):
        print("Sorry to see you leave. :(")
        quit()
#check inventory
    elif cmd in ('check bag', 'look into bag',):
        print('Items: ', _d._player.bag, '\nValue: ', _d._player.value)
        return
#examine the room for items
    elif cmd in ('look around',):
        print("You find; ")
        items = cr.items
        if items:
            print(', '.join(map(str, items)), end='.\n')
            for item in items:
                opt = input(f"Do you want to take the {item}? : ").lower().strip()
                if opt in ['y', 'yes']:
                    _d._player.take(cr._items[item.name])
                    del cr._items[item.name]
        else:
            print("Nothing of note.\n")
            print(f"You can move : {', '.join(cr.paths)}.")
# move
    elif cmd.startswith('move'):
        cmd = cmd.split()
        dir = cmd[1].title()
        if dir in DIRECTIONS and dir in cr.paths:
            _d.move(dir)
            cr = _d._current_room
            print(cr.describe)
            print(f"You can move : {', '.join(cr.paths)}.")
        else:
            print("That direction isnt valid, silly.")
        return

def loop(_debug):
    _running = True
    _d = Dungeon(_seed = 1626962216.96454)
    _intro(_d)
    if _debug:
        while _running:
            cmd = input('>>> ')
            print(eval(cmd))
    while _running:
        command = input("\nWhat do you want to do? : ")
        handle_cmd(_d, command)
        time.sleep(0.4)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        loop(bool(sys.argv[1]))
    loop(False)
