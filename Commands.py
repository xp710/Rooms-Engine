import Rooms

##############################
# Standard Gameplay Commands #
##############################

def setUpScript(scriptName: str):
    """
    Takes a string for path of script and writes the script to a string.
    :param scriptName: String for path of script
    :return: string or bool
    """
    if scriptName != False:
        with open(scriptName) as script:
            rawScript = ''
            for line in script:
                rawScript += line
            return rawScript
    else:
        return False

def findItem(x: int, y: int, name: str):
    """
    Finds an item with the given name at the given coordinates and returns it.
    :param x: x coordinate of object
    :param y: y coordinate of object
    :param name: name of object
    :return: Item object or bool
    """
    for i in Rooms.itemlist[x][y]:
        if name in i.name.lower():
            return i
    return False

def startsWithVowel(word: str):
    """
    Takes a word and tests if it starts with a vowel.
    :param word: string
    :return: bool
    """
    if word.lower()[0] in 'aeiou':
        return True
    else:
        return False

def basicLook(player: object, useEntered: bool):
    """
    The base look function the look command is built on
    :param player: player object
    :param useEntered: decides whether to use the Room.display function
    :return: None
    """
    room = Rooms.roomlist[player.x][player.y]
    if useEntered:
        room.display(not room.entered)
    else:
        room.display(True)
    exits = checkForRooms(player.x, player.y)
    for i in Rooms.itemlist[player.x][player.y]:
        if i.tags['visible'] == True:
            if startsWithVowel(i.name):
                print('There is an', i.name, 'here.')
            else:
                print('There is a', i.name, 'here.')
        elif Rooms.modes['devmode']:
            print('Invisible:', i.name)
    for e in exits:
        if exits[e]:
            print('There is an exit to the', e + '.')

def checkForRooms(x: int, y: int):
    """
    Returns in which directions there are rooms from the room at the coordinates given.
    :param x: x coord of room
    :param y: y coord of room
    :return: table of directions
    """
    room = Rooms.roomlist[x][y]
    n = (not (Rooms.roomlist[x][y + 1] == 0) and Rooms.roomlist[x][y + 1].tags['visible'] and not room.walls['n'])
    e = (not (Rooms.roomlist[x + 1][y] == 0) and Rooms.roomlist[x + 1][y].tags['visible'] and not room.walls['e'])
    s = (not (Rooms.roomlist[x][y - 1] == 0) and Rooms.roomlist[x][y - 1].tags['visible'] and not room.walls['s'])
    w = (not (Rooms.roomlist[x - 1][y] == 0) and Rooms.roomlist[x - 1][y].tags['visible'] and not room.walls['w'])
    return {'north':n, 'east':e, 'south':s, 'west':w}

def look(player: object, commands: list):
    """
    The look command
    :param player: player object
    :param commands: list of commands
    :return: None
    """
    if len(commands) == 1:
        basicLook(player, False)

    else:
        item = findItem(player.x, player.y, commands[2])
        if item != False:
            if item.tags['visible'] or Rooms.modes['devmode']:
                print(item.name)
                print(item.description)
        else:
            for i in player.inventory:
                if commands[2] in i.name:
                    print(i.name)
                    print(i.description)
                    return
            print('Item not found.')

def displayPicture(file: str):
    """
    Prints every line of a file, intended for pictures.
    :param file: string of path to file
    :return: None
    """
    with open(file) as pic:
        for line in pic:
            print(line, end='')
        print()

def picture(player: object, commands: list):
    """
    Tests if an item has a picture then displays it if it does.
    :param player: player object
    :param commands: list of commands
    :return: None
    """
    if len(commands) == 1:
        if hasattr(Rooms.roomlist[player.x][player.y], 'picture'):
            displayPicture(Rooms.roomlist[player.x][player.y].picture)
        else:
            print('This room doesn\'t have a picture')
    else:
        item = findItem(player.x, player.y, commands[1])
        if item == False:
            for i in player.inventory:
                if commands[1] in i.name.lower():
                    item = i
        if item == False:
            print('No such item!')
        else:
            if hasattr(item, 'picture'):
                displayPicture(item.picture)
            else:
                print('That item doesn\'t have a picture')



def quit(player: object, commands: list):
    """
    Ends the game loop.
    :param player: player object
    :param commands: command list
    :return: None
    """
    Rooms.playGame = False


def moveInDirection(player: object, commands: list, dx: int, dy: int):
    """
    Moves the player dx spaces in the x direction and dy spaces in the y direction.
    :param player: player object
    :param commands: command list
    :param dx: number of spaces to move right
    :param dy: number of spaces to move up
    :return: None
    """
    # current position
    cx = player.x
    cy = player.y

    # the new position for the player
    px = cx + dx
    py = cy + dy
    # check if position is in bounds and has an associated room
    if px >= 0 and py >= 0 and Rooms.roomlist[px][py] != 0:
        if Rooms.modes['devmode'] == True:
            print(Rooms.roomlist[px][py])

        # check for wall in same direction as movement
        if Rooms.roomlist[cx][cy].walls[commands[0]] == True:
            print('There is a wall in the way!')
        else:
            Rooms.roomlist[cx][cy].onExit(player, commands)
            player.x = px
            player.y = py
            basicLook(player, True)
            Rooms.roomlist[player.x][player.y].entered = True
            Rooms.roomlist[player.x][player.y].onEnter(player, commands)
    else:
        print('You can\'t move that way!')


def moveNorth(player: object, commands: list):
    """
    Moves the player north
    :param player: player object
    :param commands: command list
    :return: None
    """
    moveInDirection(player, commands, 0, 1)


def moveSouth(player: object, commands: list):
    """
    Moves the player south
    :param player: player object
    :param commands: command list
    :return: None
    """
    moveInDirection(player, commands, 0, -1)


def moveEast(player: object, commands: list):
    """
    Moves the player east
    :param player: player object
    :param commands: command list
    :return: None
    """
    moveInDirection(player, commands, 1, 0)


def moveWest(player: object, commands: list):
    """
    Moves the player west
    :param player: player object
    :param commands: command list
    :return: None
    """
    moveInDirection(player, commands, -1, 0)


def toggleMode(player: object, commands: list):
    """
    Toggles the given mode on or off. Mode must be in Rooms.modes
    :param player: player object
    :param commands: command list
    :return: None
    """
    try:
        Rooms.modes[commands[1]] = not Rooms.modes[commands[1]]
        if Rooms.modes[commands[1]] == True:
            print(commands[1], 'ON')
        else:
            print(commands[1], 'OFF')
    except:
        print('No such mode')


def take(player: object, commands: list):
    """
    Removes the given object from Rooms.itemlist and adds it to player.inventory
    :param player: player object
    :param commands: command list
    :return: None
    """
    item = findItem(player.x, player.y, commands[1])
    if item != False:
        if (item.tags['takeable']) or (Rooms.modes['devmode'] and commands[2] == 'override'):
            Rooms.itemlist[player.x][player.y].remove(item)
            player.inventory.append(item)
            print('Taken.')
            item.onTake(player, commands)
        else:
            print('You can\'t pick that up!')
    else:
        print('Item not found.')


def drop(player: object, commands: list):
    """
    Removes the given object from player.inventory and adds it to Rooms.itemlist
    :param player: player object
    :param commands: command list
    :return: None
    """
    for i in player.inventory:
        if commands[1] in i.name.lower():
            Rooms.itemlist[player.x][player.y].append(i)
            player.inventory.remove(i)
            print('Dropped.')
            i.onDrop(player, commands)
            return
    print('No such item.')


def checkInventory(player, commands):
    """
    Displays the contents of player.inventory
    :param player: player object
    :param commands: command list
    :return: None
    """
    if len(commands) == 1:
        print('Inventory:')
        for i in player.inventory:
            print(i.name)
    else:
        for i in player.inventory:
            if commands[1] in i.name.lower():
                print(i.name)
                print(i.description)
                return
        print('Item not found.')


def use(player: object, commands: list):
    """
    Runs the Item.use function if the object given is useable
    :param player: player object
    :param commands: command list
    :return: None
    """
    item = findItem(player.x, player.y, commands[1])
    if item == False:
        for i in player.inventory:
            if commands[1] in i.name:
                item = i
    if item == False:
        print('No such item.')
    elif item.tags['useable']:
        try:
            item.use(player, commands)
        except Exception as e:
            print('Can\'t run command:', e)
    else:
        print('There\'s nothing to do with it')


def help(player: object, commands: list):
    """
    Lists all the commands or gives help for the given command.
    :param player: player object
    :param commands: command list
    :return: None
    """
    if len(commands) == 1:
        print('Type \"help [command]\" for even more help!')
        print('Commands:')
        for c in Rooms.inputs:
            print(c)
    else:
        print(Rooms.inputs[commands[1]][1])


################
# Dev Commands #
################
def getPlayerPos(player: object, commands: list):
    """
    Prints the player's position.
    :param player: player object
    :param commands: command list
    :return: None
    """
    if len(commands) > 1:
        if commands[1] == 'x':
            print(player.x)
        elif commands[1] == 'y':
            print(player.y)
        else:
            print('Syntax: \"getPos\" or "getPos [x/y]')
    else:
        print('x:', player.x, 'y:', player.y)


def teleport(player: object, commands: list):
    """
    Teleports the player to the given location
    :param player: player object
    :param commands: command list
    :return: None
    """
    player.x = int(commands[1])
    player.y = int(commands[2])

def devHelp(player: object, commands: list):
    """
    Displays help for developer commands.
    :param player: player object
    :param commands: command list
    :return: None
    """
    if len(commands) == 1:
        for c in Rooms.devInputs:
            print(c)
    else:
        print(Rooms.devInputs[commands[1]][1])

def listRooms(player: object, commands: list):
    """
    Lists the rooms in Rooms.roomlist
    :param player: player object
    :param commands: command list
    :return: None
    """
    for x in range(len(Rooms.roomlist)):
        for y in range(len(Rooms.roomlist[x])):
            room = Rooms.roomlist[x][y]
            if hasattr(room, 'name'):
                print(room.name, ': ', 'x =', x, 'y =', y)

def console(player: object, commands: list):
    """
    Activates the in-game python console.
    :param player: player object
    :param commands: command list
    :return: None
    """
    print('Console activated. Type "stop" to stop.')
    pyLine = input('$ ')
    rawPython = ''
    while pyLine != 'stop':
        rawPython += pyLine+'\n'
        pyLine = input('$ ')
    exec(rawPython)
