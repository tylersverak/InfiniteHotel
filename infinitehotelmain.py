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


floor_list = {} # dictionary to keep track of all the floors in the hotel as a number:Floor pair
received_texts = [] # when a text is received, it's added to the list as a tuple of (number, message)
master_player_list = {} # dictionary to keep track of all players as a phone number (string):Player pair
RUNNNING = False
STARTING_FLOOR = 1 # starting floor number and room for new players
STARTING_ROOM = "Lobby"
LOG_NAME = None # variable for log file output
DEBUG = False

# takes a string and prints it to the local console and writes it to the currrent log file
def dprint(text):
    if DEBUG:
        print("[DEBUG] " + str(text))
    global LOG_NAME
    log = open(LOG_NAME,"a")
    log.write("[DEBUG] " + str(text) + '\n')
    log.flush()

# add a text message to the list of received text messages
def add_text(text):
    received_texts.append(text)
    print(received_texts)

# adds a player to the game. takes a string 'name' and string 'phone number' and adds a new Player object to dictionary of players
def add_player(name, number):
    temp_player = {}
    temp_player['name'] = name
    temp_player['phone_number'] = number
    temp_player['starting_items'] = []
    p = Player(temp_player)
    floor_list[STARTING_FLOOR].on_entrance(p, STARTING_ROOM)
    p.update_actions()
    master_player_list[number] = p

# creates all the floors from floors.json
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

# creates log file name and log file
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

# creates special elevator room, which exists on every floor and allows the player to move between floors
def create_elevator():
    elevator_data = {"description":"You're in the elevator. It seems to be waiting for you to say a floor number...",
                "entrances":{"west":"Elevator Hall"}, "exits":{"east":"Elevator Hall"},
                "features":{"elevatorlistener":{"description":"Listener for elevator", "hidden actions":["elevator"]}}}
    elevator = Room(elevator_data, "Elevator", 0)
    for value in floor_list.keys():
        floor_list[value].rooms['Elevator'] = elevator
    elevator.floor_list = floor_list
    return elevator

# takes the command part of the text message from incoming texts and cleans it up
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

# given a Player and requested action from the player, executes the option if allowed, otherwise informs
# player the choice could not be executed
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
            player.send_text('not a valid option, please try again') 
    else:
        player.send_text('your choice was blank, please try again')

# main function
def hotelmain(cmd_line_player):
    create_log() # need to create log first to capture all activity
    dprint('Starting...')
    initialize_floors()
    elevator = create_elevator()
    elevator_timer = None # timer used to remove player from elevator if they take too long, as only one player
                          # can be in the elevator at a time
    dprint('Game Ready!\n')

    if cmd_line_player:
        add_player("ty","1")
    dprint('Game Ready!\n')

    RUNNING = True
    while (RUNNING):
            # kicks player out of the elevator if they are in there more than 20 seconds
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
            # iterates through received texts and handles them, if the action is executed it notifies the players what new options they have
            for value in received_texts:
                player = master_player_list.get(value[1])
                if player and player.timeout <= datetime.now():
                    give_feedback(player, value[0])
                    if not player.notified:
                        dprint(player)
                        player.send_info_text()
                        dprint(player.name)
                    received_texts.remove(value)
            if cmd_line_player:
                cmd_input=input()
                if cmd_input.lower()=="q" or cmd_input.lower()=="quit":
                    return
                received_texts.append((cmd_input,"1"))
                print()
    dprint(floor_list)
    dprint("Sucessfully finished!")


"""
Things I learned:
How to make JSON/unpack it
Using __repr__ for custom string representation of instance of a class
Using get() with dictionaries to return a default value if one is not found
conditional operators (in C++, its ?, here its variable = value1 if condition else value2)
how to host a web server
advanced use of Twilio API
"""

"""
TO DO
get rid of flags
"""