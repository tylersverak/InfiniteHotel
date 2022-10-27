import json
from math import floor
from random import sample
from floor import Floor
from player import Player
from room import Room
from item import Item
from datetime import datetime
from datetime import timedelta
from inboundsms import host

# instructions- run web server for receiving texts, then run 'ngrok http 5000' cause webserver default is 5000 and then you
# gotta put ngrok url in the API

floor_list = {}
# if given pre commands like this, make sure they are right or it will cause weird errors
#received_texts = [(2, "go west"), (2, "go west"), (2, "speak 5"), (2, "go east"), (2, "go east"), (2, "go upstairs"), (2, "go upstairs"), (2, "go upstairs"),(2, "flip"),
#(2, "go downstairs"), (2, "go downstairs"), (2, "go downstairs"), (2, "go west"), (2, "go west"), (2, "speak 4"), (2, "go east"), (2, "go east")] #lighthouse
#received_texts = [(2, "go west"), (2, "go west"), (2, "speak 9"), (2, "go east"), (2, "go east"), (2, "go east"), (2, "go downstairs"), (2, "go outside"), (2, "shovel"),
#(2, "go inside"), (2, "go upstairs"), (2, "go west"), (2, "go west"), (2, "go west"), (2, "speak 11"), (2, "go east"), (2, "go east")] #lighthouse
received_texts = [(2, "go west"), (2, "go west")]
RUNNNING = False
STARTING_FLOOR = 1
STARTING_ROOM = "Lobby"
MULTIPLAYER = False # experimental, but should be relatively stable

def dprint(text):
    pass
        #print("[DEBUG] " + str(text))

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

def create_elevator():
    elevator_data = {"description":"You're in the elevator. It seems to be waiting for you to say a command...",
                "entrances":{"west":"Elevator Hall"}, "exits":{"east":"Elevator Hall"},
                "features":{"elevatorlistener":{"description":"Listener for elevator", "hidden actions":["elevator"]}}}
    elevator = Room(elevator_data, "Elevator", 0)
    for value in floor_list.keys():
        floor_list[value].rooms['Elevator'] = elevator
    elevator.floor_list = floor_list

def get_text(phone_number):
    bad_chars = [')', '(', '"', '?'] # not sure if necessary
    for value in received_texts:
        if value[0] == phone_number:
            received_texts.remove(value)
            command = value[1].strip().lower()
            if command == '':
                return None
            if command[-1] == '.':
                command = command[:-1]
            for char in bad_chars:
                command = command.replace(char, '')
            return command
    return None

def give_feedback(player):
    feedback = get_text(player.phone_number)
    if feedback:
        if feedback == "quit" or feedback == "q": # remove when not needed for debugging
            return False
        if len(feedback) > 0:
            actions = player.get_actions()
            index = feedback.find(' ')
            if feedback.split()[0] in actions:
                if index < 0:
                    player.do_action(feedback, "")
                else:
                    player.do_action(feedback[:index], feedback[index + 1:])
            else:
                print('not a valid option, please try again') # change this to texting the player
        else:
            print('your choice was blank, please try again') # change this to texting the player
    
    return True

def main():
    dprint('Starting...')
    initialize_floors()
    create_elevator()
    master_player_set = []
    notedata = {"description":"a note left by ty", "actions":[]}
    note = Item(notedata, "Ty's Note")
    pdata= {"name":"Ty", "phone_number":2, "starting_items":[note]}
    sample_player = Player(pdata)
    floor_list[STARTING_FLOOR].on_entrance(sample_player, STARTING_ROOM)
    sample_player.update_actions()
    master_player_set.append(sample_player)
    if MULTIPLAYER:
        pdata2= {"name":"Dark Ty", "phone_number":3, "starting_items":[]}
        sample_player2 = Player(pdata2)
        floor_list[STARTING_FLOOR].on_entrance(sample_player2, STARTING_ROOM)
        sample_player2.update_actions()
        master_player_set.append(sample_player2)
    dprint('Starting server...')
    host()
    dprint('Server running on localhost!')
    dprint('Game Ready!\n')

    RUNNING = True
    while (RUNNING):
        dprint("            $$$$$$$$$$$$$$$NEW TURN$$$$$$$$$$$$$$$")
        dprint(floor_list[4].get_room("Main Deck").features[0].actions[0].enabled)
        for player in master_player_set:
            if player.timeout <= datetime.now():
                if (RUNNING and player.notified): # remove when not needed for debugging
                    received_texts.append((player.phone_number, input()))
                    print()
                if not player.notified:
                    dprint(player)
                    player.send_info_text()
                    print(player.name)
                # here you would check if a text was received, but for now we use input
                RUNNING = give_feedback(player) and RUNNING
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
    main()


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
"""