import Rooms

##############################
# Standard Gameplay Commands #
##############################

def setUpScript(scriptName):
    if scriptName != False:
        with open(scriptName) as script:
            rawScript = ''
            for line in script:
                rawScript += line
            return rawScript
    else:
        return False

def findItem(x, y, name):
    for i in Rooms.itemlist[x][y]:
        if name in i.name.lower():
            return i
    return False

def startsWithVowel(word):
    if word.lower()[0] in 'aeiou':
        return True
    else:
        return False

def basicLook(player, useEntered):
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

def checkForRooms(x, y):
    room = Rooms.roomlist[x][y]
    n = (not (Rooms.roomlist[x][y + 1] == 0) and Rooms.roomlist[x][y + 1].tags['visible'] and not room.walls['n'])
    e = (not (Rooms.roomlist[x + 1][y] == 0) and Rooms.roomlist[x + 1][y].tags['visible'] and not room.walls['e'])
    s = (not (Rooms.roomlist[x][y - 1] == 0) and Rooms.roomlist[x][y - 1].tags['visible'] and not room.walls['s'])
    w = (not (Rooms.roomlist[x - 1][y] == 0) and Rooms.roomlist[x - 1][y].tags['visible'] and not room.walls['w'])
    return {'north':n, 'east':e, 'south':s, 'west':w}

def look(player, commands):
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

def displayPicture(file):
    with open(file) as pic:
        for line in pic:
            print(line, end='')
        print()

def picture(player, commands):
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



def quit(player, commands):
    Rooms.playGame = False


def moveInDirection(player, commands, dx, dy):
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


def moveNorth(player, commands):
    moveInDirection(player, commands, 0, 1)


def moveSouth(player, commands):
    moveInDirection(player, commands, 0, -1)


def moveEast(player, commands):
    moveInDirection(player, commands, 1, 0)


def moveWest(player, commands):
    moveInDirection(player, commands, -1, 0)


def toggleMode(player, commands):
    try:
        Rooms.modes[commands[1]] = not Rooms.modes[commands[1]]
        if Rooms.modes[commands[1]] == True:
            print(commands[1], 'ON')
        else:
            print(commands[1], 'OFF')
    except:
        print('No such mode')


def take(player, commands):
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


def drop(player, commands):
    for i in player.inventory:
        if commands[1] in i.name.lower():
            Rooms.itemlist[player.x][player.y].append(i)
            player.inventory.remove(i)
            print('Dropped.')
            i.onDrop(player, commands)
            return
    print('No such item.')


def checkInventory(player, commands):
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


def use(player, commands):
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


def help(player, commands):
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
def getPlayerPos(player, commands):
    if len(commands) > 1:
        if commands[1] == 'x':
            print(player.x)
        elif commands[1] == 'y':
            print(player.y)
        else:
            print('Syntax: \"getPos\" or "getPos [x/y]')
    else:
        print('x:', player.x, 'y:', player.y)


def teleport(player, commands):
    player.x = int(commands[1])
    player.y = int(commands[2])

def devHelp(player, commands):
    if len(commands) == 1:
        for c in Rooms.devInputs:
            print(c)
    else:
        print(Rooms.devInputs[commands[1]][1])

def listRooms(player, commands):
    for x in range(len(Rooms.roomlist)):
        for y in range(len(Rooms.roomlist[x])):
            room = Rooms.roomlist[x][y]
            if hasattr(room, 'name'):
                print(room.name, ': ', 'x =', x, 'y =', y)

def console(player, commands):
    print('Console activated. Type "stop" to stop.')
    pyLine = input('$ ')
    rawPython = ''
    while pyLine != 'stop':
        rawPython += pyLine+'\n'
        pyLine = input('$ ')
    exec(rawPython)
