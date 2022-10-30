from doctest import master
import json
from math import floor
from random import sample
from floor import Floor
from player import Player
from room import Room
from item import Item
from datetime import datetime
from datetime import timedelta
import time
import actionfunctions


floor_list = {}
# if given pre commands like this, make sure they are right or it will cause weird errors
#received_texts = [(2, "go west"), (2, "go west"), (2, "speak 5"), (2, "go east"), (2, "go east"), (2, "go upstairs"), (2, "go upstairs"), (2, "go upstairs"),(2, "flip"),
#(2, "go downstairs"), (2, "go downstairs"), (2, "go downstairs"), (2, "go west"), (2, "go west"), (2, "speak 4"), (2, "go east"), (2, "go east")] #lighthouse
#received_texts = [(2, "go west"), (2, "go west"), (2, "speak 9"), (2, "go east"), (2, "go east"), (2, "go east"), (2, "go downstairs"), (2, "go outside"), (2, "shovel"),
#(2, "go inside"), (2, "go upstairs"), (2, "go west"), (2, "go west"), (2, "go west"), (2, "speak 11"), (2, "go east"), (2, "go east")] #lighthouse
received_texts = []
master_player_list = {}
RUNNNING = False
STARTING_FLOOR = 1
STARTING_ROOM = "Lobby"
LOG_NAME = None
MULTIPLAYER = False # experimental, but should be relatively stable

def dprint(text):
    print("[DEBUG] " + str(text))
    global LOG_NAME
    log = open(LOG_NAME,"a")
    log.write("[DEBUG] " + str(text) + '\n')
    log.flush()

def add_text(text):
    received_texts.append(text)
    print(received_texts)

def add_player(name, number):
    temp_player = {}
    temp_player['name'] = name
    temp_player['phone_number'] = number
    temp_player['starting_items'] = []
    p = Player(temp_player)
    floor_list[STARTING_FLOOR].on_entrance(p, STARTING_ROOM)
    p.update_actions()
    master_player_list[number] = p

def initialize_floors():
    dprint('Initializing floors...')
    with open('floors.json') as jsonfile:
        dump = json.load(jsonfile)
        for floor in dump:
            dprint(floor)
            temp_floor = Floor(dump[floor], floor)
            if temp_floor.class_ == "twin":
                temp_floor.twin = floor_list[dump[floor]["twin"]]
            floor_list[temp_floor.number] = temp_floor
            dprint(temp_floor.get_rooms())
    dprint('Initializing floors complete.')

def create_log():
    date = str(datetime.now())
    index = date.find(".")
    date = date[:index]
    date = date.replace(':', "-")
    global LOG_NAME
    LOG_NAME = "logs/log " + date + ".txt"
    log = open(LOG_NAME,"a")
    log.write("Game from " + date + "\n**************************BEGIN**************************")
    log.flush()


def create_elevator():
    elevator_data = {"description":"You're in the elevator. It seems to be waiting for you to say a floor number...",
                "entrances":{"west":"Elevator Hall"}, "exits":{"east":"Elevator Hall"},
                "features":{"elevatorlistener":{"description":"Listener for elevator", "hidden actions":["elevator"]}}}
    elevator = Room(elevator_data, "Elevator", 0)
    for value in floor_list.keys():
        floor_list[value].rooms['Elevator'] = elevator
    elevator.floor_list = floor_list
    return elevator

def filter_action(command):
    bad_chars = [')', '(', '"', '?'] # not sure if necessary
    command = command.strip().lower()
    if command == '':
        return None
    if command[-1] == '.':
        command = command[:-1]
    for char in bad_chars:
        command = command.replace(char, '')
    return command

def give_feedback(player, action_from_player):
    if len(action_from_player) > 0:
        action_from_player = filter_action(action_from_player)
        actions = player.get_actions()
        index = action_from_player.find(' ')
        if action_from_player.split()[0] in actions:
            if index < 0:
                player.do_action(action_from_player, "")
            else:
                player.do_action(action_from_player[:index], action_from_player[index + 1:])
        else:
            print('not a valid option, please try again') # change this to texting the player
    else:
        print('your choice was blank, please try again') # change this to texting the player

def hotelmain():
    # need to create log first to capture all activity
    create_log()
    dprint('Starting...')
    initialize_floors()
    elevator = create_elevator()
    elevator_timer = None
    dprint('Game Ready!\n')

    RUNNING = True
    while (RUNNING):
            if elevator.player_count() > 0:
                if elevator_timer and elevator_timer + timedelta(seconds = 20) < datetime.now():
                    temp = list(elevator.get_players())
                    for value in temp:
                        value.send_text("The magic elevator threw you out because you were in there for more than 20 seconds!")
                        actionfunctions.go_to(value, "east")
                        value.send_info_text()
                    elevator_timer = None
                elif not elevator_timer:
                    elevator_timer = datetime.now()
            else:
                elevator_timer = None
            for value in received_texts:
                player = master_player_list.get(value[1])
                if player and player.timeout <= datetime.now():
                    give_feedback(player, value[0])
                    if not player.notified:
                        dprint(player)
                        player.send_info_text()
                        dprint(player.name)
                    received_texts.remove(value)
    dprint(floor_list)
    '''
    while (game running):
        might need a different thread for each player
        gather possible actions from action handler, which looks at combination of room + player
        gets room description and sends to player
        displays function names ("RUN") and gives description and sends to player
        take incoming texts (cooldown for a few seconds)
        for each text, find the player and feed input (player + text) to action handler
        sees if valid command with room, if not, creates message to send to player saying no
        if valid, send to room, unless its a room move then the action handler does it (might not actually move them)

    '''
    dprint("Sucessfully finished!")

if __name__ == "__main__":
    pass#hotelmain()


"""
Things I learned:
How to make JSON/unpack it
Using __repr__ for custom string representation of instance of a class
Using get() with dictionaries to return a default value if one is not found
conditional operators (in C++, its ?, here its variable = value1 if condition else value2)
"""

"""
TO DO
decide how to show the player if an action need a parameter
maybe have lobby be starting point?
floor 6 being rock floor
need clear implementation for "infiniteness" of hotel- probably have "solid" 10 or so first floors that map exactly
to a specific floor, then 40 or so floors that can be accessed either with their number or if the input is too big, it
will be hashed to be unique and modulo'd back to a range that's workable.
Hidden actions need something to stop them from having behavior when someone speaks, but still needs to be able to
trigger when someone says the right thing.
get rid of flags
PLAN
15 rooms,
so 1 today 1 tomorrow 4 wednesday 3 thursday
infinity symbol
more obvious directions
take debug stuff out of texts, also out of go
have things recorded to txt file
elevator kick people out
"""