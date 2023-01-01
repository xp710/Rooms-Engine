import Commands

roomlist = []
itemlist = []
gameLoopFunctions = []
playGame = True

modes = {
    'devmode': False,
}


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = []


class Room:
    def __init__(self, name, description, walls, tags, scripts):
        self.name = name
        self.description = description
        self.walls = {
            'n': False,
            'e': False,
            's': False,
            'w': False,
        }
        self.tags = {
            'visible': True,
        }
        self.scripts = {
            'onEnter': False,
            'onExit': False
        }
        for w in walls:
            self.walls[w] = walls[w]
        for t in tags:
            self.tags[t] = tags[t]
        for s in scripts:
            self.scripts[s] = scripts[s]
        self.entered = False

    def display(self, printDesc=True):
        print('===========================')
        print(self.name)
        print('===========================')
        if printDesc:
            print(self.description)

    def onEnter(self, player, commands):
        script = Commands.setUpScript(self.scripts['onEnter'])
        if script != False:
            exec(script)

    def onExit(self, player, commands):
        script = Commands.setUpScript(self.scripts['onExit'])
        if script != False:
            exec(script)

class Item:
    def __init__(self, name, description, tags, scripts):
        self.name = name
        self.description = description
        self.tags = {
            'takeable': True,
            'visible': True,
            'useable': False,
        }
        for t in tags:
            self.tags[t] = tags[t]
        self.scripts = {
            'use': False,
            'onTake': False,
            'onDrop': False
        }
        for s in scripts:
            self.scripts[s] = scripts[s]

    def use(self, player, commands):
        script = Commands.setUpScript(self.scripts['use'])
        if script != False:
            exec(script)
        else:
            print('There\'s nothing to do with it!')

    def onTake(self, player, commands):
        script = Commands.setUpScript(self.scripts['onTake'])
        if script != False:
            exec(script)

    def onDrop(self, player, commands):
        script = Commands.setUpScript(self.scripts['onDrop'])
        if script != False:
            exec(script)

    def getPos(self):
        for x in range(len(itemlist)):
            for y in range(len(itemlist[x])):
                for i in itemlist[x][y]:
                    if i == self:
                        return [x, y]
        return False

class Key(Item):
    def __init__(self, name, description, walls, scripts):
        Item.__init__(self, name, description, {'useable': True}, scripts)
        self.walls = walls
        # The format for walls:
        # [{'x':0,'y':0,'dir':'s'},{'x':1,'y':0,'dir':'n'}]

    def use(self, player, commands):
        notInRoom = 0
        alreadyUnlocked = 0
        for w in self.walls:
            if w['x'] == player.x and w['y'] == player.y:
                if roomlist[w['x']][w['y']].walls[w['dir']]:
                    roomlist[w['x']][w['y']].walls[w['dir']] = False
                    print('Unlocked.')
                else:
                    alreadyUnlocked += 1
            else:
                notInRoom += 1
        if notInRoom > 0:
            print('This key can be used in', notInRoom, 'other rooms.')
        if alreadyUnlocked > 0:
            print('Already unlocked.')

class Teleporter(Item):
    def __init__(self, name, description, tags, destination, scripts):
        Item.__init__(self, name, description, tags, scripts)
        self.tags['useable'] = True
        self.destination = destination

    def use(self, player, commands):
        if roomlist[self.destination[0]][self.destination[1]] != 0:
            player.x = self.destination[0]
            player.y = self.destination[1]
            Commands.look(player, ['look'])
            roomlist[player.x][player.y].entered = True
            roomlist[player.x][player.y].onEnter(player, commands)
        else:
            print('Teleporter destination doesn\'t exist')


inputs = {
    'look': (Commands.look, 'Syntax:\n'
                            '"look" or "look at [item]"'),
    'use': (Commands.use, 'Syntax:\n'
                          '"use [item] [optional item-specific options]"'),
    'pic': (Commands.picture, 'Syntax:\n'
                              '"pic [(optional) item]"'),
    'quit': (Commands.quit, 'Quits the game.'),
    'n': (Commands.moveNorth, 'Moves north'),
    's': (Commands.moveSouth, 'Moves south'),
    'e': (Commands.moveEast, 'Moves east'),
    'w': (Commands.moveWest, 'Moves west'),
    'toggle': (Commands.toggleMode, 'Toggles different game modes.\n'
                                    'Syntax:\n'
                                    '"toggle [game mode]"'),
    'take': (Commands.take, 'Syntax:\n'
                            '"take [item]"'),
    'drop': (Commands.drop, 'Syntax:\n'
                            '"drop [item]"'),
    'i': (Commands.checkInventory, 'Checks your inventory.\n'
                                   'Syntax:\n'
                                   '"i" or "i [item in inventory]"'),
    'help': (Commands.help, 'Syntax:\n'
                            '"help" or "help [command]"'),
}

devInputs = {
    'getPos': (Commands.getPlayerPos, 'Syntax:\n'
                                      '"getPos" or "getPos [x/y]"'),
    'tp': (Commands.teleport, 'Syntax:\n'
                              '"tp [x] [y]"'),
    'devHelp': (Commands.devHelp, 'Syntax:\n'
                                  '"devHelp" or "devHelp [command]"'),
    'listRooms': (Commands.listRooms, 'Lists all rooms and their coords.'),
    'console': (Commands.console, 'Syntax:\n'
                                  '"console"'),
}


def getInputList(prompt, sep):
    raw = input(prompt)
    return str.split(raw, sep)


def gameLoop(player):
    while playGame:
        move = getInputList('> ', ' ')
        try:
            inputs[move[0]][0](player, move)
        except Exception as e:
            print('Enter a valid command.')
            if modes['devmode'] == True:
                print(e)
                try:
                    devInputs[move[0]][0](player, move)
                except Exception as e:
                    print('Invalid developer command.', e)
        for f in gameLoopFunctions:
            f(player, move)
