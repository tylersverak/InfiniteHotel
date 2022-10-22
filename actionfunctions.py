import random
from hashlib import sha256
################################################### CONSTANTS ######################################################################
# for library reading random book
LIST_OF_BOOKS = ["\"How to Make Carrot Soup: A Book About Carrot Soup\". Hm, seems boring.", "\"Top 10 Top 10 YouTube Videos of 2010\". You can learn about the best Top 10 videos of the 2010s."]



# every function returns True on success and False on failure/inability to use

def default(player, args):
    player.send_text(player.name + ' did default action in ' + player.room.name)
    return True

def item_default(player, args):
    for value in player.items:
        if value.name.lower() == args:
            player.send_text(player.name + ' used the item ' + value.name + ' (default item use)')
            return True
    player.send_text("Hm... you don't seem to have that item... (check your spelling?)")
    return False
    
def item_pickup(player, args):
    for value in player.room.items:
        if value.name.lower() == args:
            player.give_item(value)
            player.room.items.remove(value)
            player.send_text("You picked up " + value.name + ".")
            return True
    player.send_text("That item doesn't seem to be here... (check your spelling?)")
    return False

def item_dropoff(player, args):
    for value in player.items:
        if value.name.lower() == args:
            player.room.items.append(value)
            player.take_item(value)
            player.send_text("You put " + value.name + " down.")
            return True
    player.send_text("Hm... you don't seem to have that item... (check your spelling?)")

def go_to(player, args):
    start_room = player.room
    end_room = player.room.exits.get(args)
    if end_room: # checks if exit from current room is valid
        start_room_name = start_room.name
        if player.floor.number == 1:
            if start_room.name == "Elevator" and end_room == "Elevator Hall": # special case for first floor, where there is no elevator hall
                end_room = "Main Hall"
            elif start_room.name =="Main Hall" and end_room == "Elevator":
                start_room_name = "Elevator Hall"
        end_room = player.floor.get_room(end_room) # takes name of end room and gets room object
        if args in end_room.entrances and end_room.entrances[args] == start_room_name: # checks if exit is an entrance of the other room
            if end_room.name == "Elevator" and end_room.player_count() > 0: # checks if the elevator is already in use
                player.send_text("The elevator seems to be busy. Wait for that person to get off then try again.")
                return True
            start_room.on_exit(player, end_room)
            end_room.on_entrance(player, start_room)
            player.send_text(player.name + ' went ' + args + ' into the room ' + end_room.name)
            return True
        else:
            player.send_text("Hm... can't go that way now. Might have to wait or find another way there, or it might be locked. Now what?")
    else:
        player.send_text("Hm... doesn't seem you can go that way... (check your spelling?)")
    return False

def speak(player, args):
    player.send_text(player.name + ' said ' + args + ' in ' + player.room.name)
    actions = player.get_action_objects()
    for value in actions.keys():
        if actions[value].hidden:
            actions[value].use(player, args)
    for value in player.room.players:
        if value != player:
            value.send_text(player.name + " said: " + args)
    return True

# need to update if items have multiple different uses that can be picked from at the same time
def use_item(player, args):
    for value in player.items:
        if value.name.lower() == args:
            value.actions[0].try_use()
            return True
    player.send_text("Hm... you don't seem to have that item... (check your spelling?)")
    return False

def inspect(player, args):
    features = player.room.features
    for value in features:
        if value.name.lower() == args:
            player.send_text(player.name + ' inspected the ' + value.name + '.')
            player.send_text(value.description)
            for hidden_action in value.hidden_actions:
                hidden_action.hidden = False
            return True
    player.send_text("Hm... whatever you're trying to inspect isn't here... (check your spelling?)")
    return False

def laszewo_room(player, args):
    if args == "laszewo" and player.room.name == "Main Hall" and player.floor.number == 3:
        player.floor.rooms['Main Hall'].exits['east'] = 'Laszewo Room'
        player.floor.rooms['Main Hall'].entrances['west'] = 'Laszewo Room'
        player.send_text("The symbol on the ground reacted to your words! The circle in the wall retracted, revealing a secret room!")
        return True

def listen_to_music(player, args):
    player.send_text('Hope you like it!')
    player.send_text('text player https://open.spotify.com/artist/6jxGLrn1I14RIeRYodOpLN?si=ttpZiyibTiKzoWO4NYjoKA')
    return True

def elevator_move(player, args):
    if player.room.name != "Elevator":
        raise Exception(player.name + " attempting to use elevator without being in it!")
    if args.strip('-').isdigit():
        number = int(args.strip('-'))
        print(str(hash(sha256(str(number).encode('utf-8')).hexdigest()) % 10 + 2) + " is what you would go to if hash was used")
        if number == player.floor.number:
            player.send_text("You're on that floor, so the elevator didn't move.")
            return True
        floor_list = player.room.floor_list
        if number in floor_list.keys():
            player.floor.on_exit(player)
            floor_list[number].on_entrance(player)
            player.send_text("The elevator started moving and took you to another floor.")
        else:
            player.send_text("[currently no functionality programmed for non existing floors, implementation tbd]")
            return False
        return True
    else:
        player.send_text("Not a number... please try again.")
        return False

def random_book(player, args):
    player.send_text(random.choice(LIST_OF_BOOKS))
    return True

def play_notes(player, args):
    notes = ""
    print(args.split()[0])
    for char in args.split()[0]:
        ascii = ord(char)
        if ascii >= 97 and ascii <= 104:
            notes += char.upper()
    if notes == "":
        player.send_text("Can't play that.")
        return False
    elif notes == "BAGBAGGGGGAAAABAG":
        player.send_text("Played " + notes + "\nHey, that's hot cross buns!")
    else:
        player.send_text("Played " + notes)
    return True

def basement_secret(player, args):
    if player.floor.number != 0 or player.room.name != "Basement":
        raise Exception(player.name + " tried to use hidden basement switch from outside of basement!")
    new_room = player.floor.get_room("Underground")
    start_room = player.room
    start_room.on_exit(player, new_room)
    new_room.on_entrance(player, start_room)
    for value in start_room.features:
        for action in value.hidden_actions:
            action.hidden = True
    player.send_text("As you pull the book, the bookshelves swings out of the wall and you feel the floor moving under your feet. The whole bookshelf rotates 180 degrees, throws you into a secret room opposite from the basement you were in, and swings around again, sealing you inside.")
    return True