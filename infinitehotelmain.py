import json
from floor import Floor
from player import Player
from room import Room
from item import Item

floor_list = {}
#received_texts = [(2, "goto east"), (2, "goto east"), (2, "speak laszewo"), (2, "goto east"), (2, "inspect record player"), (2, "listen")]
received_texts = []
RUNNNING = False
STARTING_FLOOR = 1
STARTING_ROOM = "Elevator"

def dprint(text):
        print("[DEBUG] " + str(text))

def initialize_floors():
    dprint('Initializing floors...')
    with open('floors.json') as jsonfile:
        dump = json.load(jsonfile)
        for floor in dump:
            dprint(floor)
            temp_floor = Floor(dump[floor], floor)
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
    for value in received_texts:
        if value[0] == phone_number:
            received_texts.remove(value)
            command = value[1].strip().lower()
            if command == '':
                return None
            if command[-1] == '.':
                command = command[:-1]
            return command
    return None

def main():
    dprint('Starting...')
    initialize_floors()
    create_elevator()
    master_player_set = set()
    notedata = {"description":"a note left by ty", "actions":[]}
    note = Item(notedata, "Ty's Note")
    pdata= {"name":"Ty", "phone_number":2, "starting_items":[note]}
    sample_player = Player(pdata)
    floor_list[STARTING_FLOOR].on_entrance(sample_player, STARTING_ROOM)
    sample_player.update_actions()
    master_player_set.add(sample_player)
    dprint('Game Ready!\n')

    RUNNING = True
    while (RUNNING):
        for player in master_player_set:
            if not player.notified:
                dprint(player)
                player.send_text()
            # here you would check if a text was received, but for now we use input
            feedback = get_text(player.phone_number)
            if feedback:
                if feedback == "quit" or feedback == "q": # remove when not needed for debugging
                    RUNNING = False
                    break
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
            if (RUNNING and player.notified): # remove when not needed for debugging
                received_texts.append((player.phone_number, input()))
                print()
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
"""