import random
from hashlib import sha256
################################################### CONSTANTS ######################################################################
# for library reading random book
LIST_OF_BOOKS = ["\"How to Make Carrot Soup: A Book About Carrot Soup\". Hm, seems boring.", "\"Top 10 Top 10 YouTube Videos of 2010\". You can learn about the best Top 10 videos of the 2010s."]



# every function returns True on success and False on failure/inability to use

# default action if the action is not assigned another function. this function should only be seen in testing.
def default(player, args):
    player.send_text(player.name + ' did default action in ' + player.room.name)
    return True

# takes an argument as a string and sends a description of the Item to the Player, if they have it in their inventory
def item_default(player, args):
    for value in player.items:
        print(value.name.lower())
        print(args)
        if value.name.lower() == args:
            player.send_text(player.name + ' inspected ' + value.name + '. ' + value.description)
            return True
    player.send_text("Hm... you don't seem to have that item... (check your spelling?)")
    return False

# takes an argument as a string and if an Item exists in the room with that name, the Player picks it up
def item_pickup(player, args):
    for value in player.room.items:
        if value.name.lower() == args:
            player.give_item(value)
            player.room.items.remove(value)
            player.send_text("You picked up " + value.name + ".")
            return True
    player.send_text("That item doesn't seem to be here... (check your spelling?)")
    return False

# takes an argument as a string and if an Item exists with that name in the Player's inventory, drops it in the current room
def item_dropoff(player, args):
    for value in player.items:
        if value.name.lower() == args:
            player.room.items.append(value)
            player.take_item(value)
            player.send_text("You put " + value.name + " down.")
            return True
    player.send_text("Hm... you don't seem to have that item... (check your spelling?)")

# takes an argument as a string, and goes that direction from the current Room, if possible
def go_to(player, args):
    start_room = player.room
    end_room = player.room.exits.get(args)
    if end_room: # checks if exit from current Room is valid
        start_room_name = start_room.name
        if player.floor.number == 1:
            if start_room.name == "Elevator" and end_room == "Elevator Hall": # special case for first Floor, where there is no elevator hall
                end_room = "Main Hall"
            elif start_room.name =="Main Hall" and end_room == "Elevator":
                start_room_name = "Elevator Hall"
        end_room = player.floor.get_room(end_room) # takes name of end Room and gets Room object
        if args in end_room.entrances and end_room.entrances[args] == start_room_name: # checks if exit is an entrance of the other Room
            if end_room.name == "Elevator" and end_room.player_count() > 0: # checks if the elevator is already in use
                player.send_text("The elevator seems to be busy. Wait for that person to get off then try again.")
                return True
            start_room.on_exit(player, end_room)
            end_room.on_entrance(player, start_room)
            player.send_text(player.name + ' went ' + args)
            return True
        else:
            player.send_text("Hm... can't go that way now. Might have to wait or find another way there, or it might be locked. Now what?")
    else:
        player.send_text("Hm... doesn't seem you can go that way... (check your spelling?)")
    return False

# takes an argument as a string and allows the Player to speak it aloud in the room. The speech can sometimes unlock hidden Actions in the Room
def speak(player, args):
    player.send_text(player.name + ' said "' + args + '" in ' + player.room.name)
    actions = player.get_action_objects()
    for value in actions.keys():
        if actions[value].hidden and (args == actions[value].name.lower() or actions[value].name == "elevator"):
            actions[value].use(player, args)
    for value in player.room.players:
        if value != player:
            value.send_text(player.name + " said: " + args)
    return True

# takes an argument as a string, if a Feature exists in the Room, tells the Player its description
def inspect(player, args):
    features = player.room.features
    for value in features:
        if value.name.lower() == args:
            player.send_text(player.name + ' inspected the ' + value.name + '.')
            player.send_text(value.description)
            for hidden_action in value.hidden_actions: # make hidden actions visible for that one feature
                hidden_action.hidden = False
            return True
    player.send_text("Hm... whatever you're trying to inspect isn't here... (check your spelling?)")
    return False

# takes an argument as a string, if that argument is the secret word, allows the Player to travel to a secret Room
def laszewo_room(player, args):
    if args == "laszewo" and player.room.name == "Main Hall" and player.floor.number == 3:
        player.floor.rooms['Main Hall'].exits['east'] = 'Laszewo Room'
        player.floor.rooms['Main Hall'].entrances['west'] = 'Laszewo Room'
        player.send_text("The symbol on the ground reacted to your words! The circle in the wall retracted, revealing a secret room!")
        return True
    raise Exception(player.name + " tried to open secret L room from somewhere else.")

# sends a link to the Player to listen to some cool tunes
def listen_to_music(player, args):
    player.send_text('Hope you like it!')
    player.send_text('https://open.spotify.com/artist/6jxGLrn1I14RIeRYodOpLN?si=ttpZiyibTiKzoWO4NYjoKA')
    return True

# takes what the Player said in the elevator and moves the elevator as needed
def elevator_move(player, args):
    if player.room.name != "Elevator":
        raise Exception(player.name + " attempting to use elevator without being in it!")
    if args.strip('-').isdigit():
        number = int(args.strip('-'))
        if number == player.floor.number:
            player.send_text("You're on that floor, so the elevator didn't move.")
            return True
        floor_list = player.room.floor_list
        if number >= len(floor_list):
            number = (number % (len(floor_list) - 2)) + 2 # if Player tries to go to Floor that doesn't exist, corrals the value between 2-15
        if number in floor_list.keys():
            player.floor.on_exit(player)
            floor_list[number].on_entrance(player)
            player.send_text("The elevator started moving and took you to another floor.")
        else:
            raise Exception(player.name + " tried to go to illegal floor!")
        return True
    else:
        player.send_text("Not a number... please try again.")
        return False

# reads a random book off the shelf. There's only two books, for now.
def random_book(player, args):
    player.send_text(random.choice(LIST_OF_BOOKS))
    return True

# HARDCODED TO ASSUME BOAT IS FLOOR 4!!!
# turns the lighthouse lamp on/off, when the light is on the boat is able to steer to shore
def lighthouse_switch(player, args):
    other = player.floor.get_room("Elevator").floor_list[4]
    temp_features = other.get_room("Main Deck").features
    helm_action = None
    for value in temp_features:
        if value.name == "The Helm":
            helm_action = value.actions[0]
            break
    if helm_action.enabled:
        player.send_text("You flip the switch and the lamp goes off, you notice how dark it is.")
        player.room.description = "You come to the top of the lighthouse. The ocean air smells foul. You can't see much, but you can hear the waves crashing against the shore. The lamp is off."
    else:
        player.send_text("You flip the switch and the lamp comes on, shining a light over the sea.")
        player.room.description = "You come to the top of the lighthouse. The ocean air smells foul. You can't see much, but you can hear the waves crashing against the shore. The lamp is on and illuminates the sea."
    helm_action.enabled = not helm_action.enabled # flip whether light can be seen
    return True

# given a string, if the string contains characters a-g, plays those notes on the piano
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

# pulls the secret basement switch which throws the player into a secret underground Room
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

# if the lighthouse is on, allows the Player to steer the boat to shore. need to update so it moved every Player in the Room.
def steer_boat(player, args):
    player.send_text("You notice the lighthouse in the distant, and steer towards it. After a while of sailing, you see the shore, and a dock to pull the boat into. When the boat stops, a small glass orb slides falls out of a compartment and rolls across the boat's deck.")
    player.room.entrances = {}
    print(player.room)
    print(player.room.entrances)
    new_floor = player.floor.get_room("Elevator").floor_list[5]
    start_floor = player.floor
    start_floor.on_exit(player)
    new_floor.on_entrance(player, room="Boat 2")
    new_floor.get_room("Dock").entrances["west"] = "Boat 2"
    new_floor.get_room("Dock").exits["east"] = "Boat 2"
    return True

# if the Player brings the Sea Orb into the lighthouse, they can gaze into it using equipment in the room. otherwise they see nothing
def orb(player, args):
    orb = player.get_item("Sea Orb")
    if player.floor.name == "Lighthouse Floor" and player.room.name == "Entryway" and orb:
        player.send_text("You place the orb on the indentation. As it rests there, you look down the telescopic lens into the middle of it. A fog swirls inside the orb. You can faintly make out writing in the orb: \"GUTS:3295\". The orb remains on the apparatus.")
        player.take_item(orb)
        player.room.items.append(orb)
        return True
    player.send_text("You look into the orb, but the swirling fog obscures your view and you can't see anything useful. You'd need a tool to see inside.")
    return True

# pulls the lever of the slot machine and pays out accordingly
def slot_machine(player, args):
    luck = random.randint(1, 100)
    machine = player.room.get_feature("Slot Machine")
    prizes = player.floor.get_room("Prize Room")
    if luck == 1:
        player.send_text("You pull the lever on the machine... It displays: [*][*][*]. Jackpot! The machine's bells are going crazy, and a message is displayed on the machine: \"LUCK:2861\".")
    elif luck <= 5:
        shovel = prizes.get_item("Frying Pan")
        if shovel:
            prizes.items.remove(shovel)
            player.send_text("You pull the lever on the machine... It displays: [P][P][P]. You won... a frying pan? The frying pan comes out of the bottom of the machine. Better pick it up fast.")
            player.room.items.append(shovel)
        else:
            player.send_text("You pull the lever on the machine... It displays: [P][P][P]. Looks like you would've won a frying pan, but someone won it already.")
    elif luck <= 15:
        lemon = prizes.get_item("Lemon")
        if lemon:
            prizes.items.remove(lemon)
            player.send_text("You pull the lever on the machine... It displays: [L][L][L]. You won... a lemon? The lemon comes out of the bottom of the machine. Better pick it up fast.")
            player.room.items.append(lemon)
        else:
            player.send_text("You pull the lever on the machine... It displays: [L][L][L]. Looks like you would've won a lemon, but someone won it already.")
    elif luck <= 20:
        player.send_text("You pull the lever on the machine... It displays: [s][s][s]. You got a drink coupon!\n[take a shot IRL! if you want, I guess...]")
    else:
        losing = ["[P]", "[*]", "[s]", "[L]"]
        choices = [random.randrange(len(losing)), random.randrange(len(losing)), random.randrange(len(losing))]
        if choices[2] == choices[1]:
            choices[2] = (choices[2] + 1) % len(losing)
        player.send_text("You pull the lever on the machine... It displays: " + losing[choices[0]] + losing[choices[1]] + losing[choices[2]] + ". Rats! Try again.")
    return True

# if the Player is in a Room they can dig, they will dig. otherwise they will not dig
def dig(player, args):
    if player.room.name == "Dad Pool" and player.floor.name == "Creek Floor":
        if player.room.get_feature("Sword Spot").description != "nothing":
            player.send_text("There's something buried here. You dig it up, and find... an awesome sword! Good find.")
            player.room.get_feature("Sword Spot").description = "nothing"
            sword_data = {"description":"An awesome sword you dug up in a creek. Truly, does it get any cooler than this?", "actions":["swing"]}
            player.make_item(sword_data, "Sword")
        else:
            player.send_text("Someone's already dug something up here.")
        return True
    elif player.room.name == "Hole" and player.floor.name == "Rock Pile":
        crystal = player.room.get_feature("Crystal")
        if player.room.get_feature("Crystal") and player.room.get_feature("Crystal").description != "nothing":
            player.send_text("You start digging and the shovel hits something hard. You keep going, unearthing an awesome semitransparent crystal! I wonder what is does.")
            player.room.get_feature("Crystal").description = "nothing"
            crystal_data = {"description":"A crystal you found buried in a cave. It seems to respond to hidden things in the environment.", "actions":["scan"]}
            player.make_item(crystal_data, "Crystal")
        else:
            player.send_text("Someone's already dug something up here.")
        return True
    player.send_text("There doesn't appear to be a good spot to dig here... try somewhere else.")
    return True

# Player jumps from the top of the waterfall and ends in Pool Room
def cliff_jump(player, args):
    if player.room.name != "Top":
        raise Exception(player.name + " tried to cliffjump somewhere other than top!")
    new_room = player.floor.get_room("Pool")
    start_room = player.room
    start_room.on_exit(player, new_room)
    new_room.on_entrance(player, start_room)
    player.send_text("You take two steps back, then... F*** it, time to JUMP!!!")
    player.set_timeout(3)
    return True

# skips a rock.
def skip(player, args):
    res = ""
    skips = 1
    while random.randrange(2) == 0:
        skips += 1
    for x in range(1, skips):
        res += str(x) + "... "
    if skips == 1:
        res += "1 skip, that's a dud."
    elif skips < 4:
        res += str(skips) + " skips, nice."
    elif skips < 6:
        res += str(skips) + " skips! Holy cow."
    else:
        res += str(skips) + " SKIPS? ARE YOU OUT OF YOUR MIND? YOU'RE CRACKED AS SHIT!!! [you should actually tell me you did this, this is impressive]"
    player.send_text(res)
    return True

# attempts to grab a crawdad out of the stream
def crawdad(player, args):
    respond = ("You try to nab it... Ah! Not this time...", "You go for the crawdad... it nips you! Ouch!",
                "You slowly go for the dad... rats! It barely darted away at the last second.",
                "You reach for the crawdad... snatched! With perfect form, you get him right behind the claws. Good job! Probably best to let him go now...")
    index = random.randrange(len(respond))
    player.send_text(respond[index])
    return True

# swings sword around. if the Player is in the Main Room of the Great Library, it opens the office
def swing(player, self):
    if player.floor.name == "Great Library" and player.room.name == "Main Room":
        player.floor.get_room("Office").entrances["upstairs"] = "Main Room"
        player.send_text("WHOOSH! WHOOSH! You swing the sword around. The sword seems to pull you upstairs, toward the office doors. You put the sword in the keyhole and unlock the office door!")
        return True
    player.send_text("WHOOSH! WHOOSH! You swing the sword around. Pretty darn cool.")
    return True

# tosses a die
def toss(player, self):
    player.send_text("You throw one of the die high into the air, and it comes crashing down on the cement. Not sure where you were aiming with that one.")
    return True

# gives the Player the shovel if no one has retrieved the shovel yet
def shovel(player, self):
    if player.room.name != "Courtyard" or player.floor.name != "House Floor":
        raise Exception(player.name + " tried to use shovel outside of house floor")
    if player.room.get_feature("Shovel Spot").description != "nothing":
            player.send_text("You sift through the junk pile and find a shovel. Maybe there's a good place to dig somewhere.")
            player.room.get_feature("Shovel Spot").description = "nothing"
            shovel_data = {"description":"A shovel you found in a pile of junk.", "actions":["dig"]}
            player.make_item(shovel_data, "Shovel")
    else:
        player.send_text("You look through the junk, but there's no shovel here... someone else must've gotten it.")
    return True

# scans the Room, if secret Actions exists there, the crystal glows
def scan(player, self):
    message = "You gaze into the crystal. You feel its energy scan the environment... "
    for value in player.room.features:
        if value.hidden_actions != []:
            player.send_text(message + "the crystal begins to glow with a faint glowing light. Something hidden is nearby.")
            return True
    player.send_text(message + "but nothing special happens. Try using it somewhere else.")
    return True

# piles another rock on the stack
def pile(player, self):
    respond = ("You pile rocks on the stack. It starts to look a little bigger! Hopefully that's not just your imagination.",
                "You throw a few more rocks at the pile. Nothing's changed yet...",
                "You search the room for more rocks to stack. You find a few, and throw them on the pile.",
                "More rocks get put onto the stack.",
                "You add rocks to the pile.",
                "You toss a rock on the top of the pile.",
                "Another rock gets added to the pile.",
                "You put another few rocks on the pile in hopes it will get bigger",
                "After adding a few more rocks to the stack, you try to scale the wall. You're so close, but not quite able to get out.",
                "More rocks get added to the pile. Maybe you should keep adding more.",
                "You add another rock. Each rock has to make the pile bigger, right?",
                "You find a lot of rocks, and careful add each one to the pile. You can't quite reach the hole, but a few more really ought to be enough.")
    index = random.randrange(len(respond))
    player.send_text(respond[index])
    return True

# takes an argument as a string and checks if that string is an answer to one of the trivia questions. unlocks a prize when all 5 are answered
def question_listener(player, args):
    questions = {'a', 't', 'w', 'i', 'h'}
    for value in player.room.features:
        if value.name[:4].lower() != 'door':
            if value.description[:1].lower() in questions:
                player.send_text("Correct! You have one less question to answer.")
                player.room.features.remove(value)
                if len(player.room.features) <= 2:
                    player.send_text("That's the last question! Your prize has been given to you.")
                    knowledge = {"description":"A prize from winning trivia. It reads: \"KNOWLEDGE:1349\".", "actions":[]}
                    player.make_item(knowledge, "Trivia Prize")
                return True
            player.send_text("Correct, but someone already answered that question.")
            return True
    return True

# takes an argument as a string and opens vault1 if the string is the PIN
def vault1(player, args):
    if args == "6430" and player.room.name == "Ability Room" and player.floor.name == 'Vault':
        player.floor.rooms['Ability Room'].exits['east'] = 'Spirits Room'
        player.send_text("The door unlocked!")
        return True

# takes an argument as a string and opens vault2 if the string is the PIN
def vault2(player, args):
    if args == "5007" and player.room.name == "Spirits Room" and player.floor.name == 'Vault':
        player.floor.rooms['Spirits Room'].exits['east'] = 'Knowledge Room'
        player.send_text("The door unlocked!")
        return True

# takes an argument as a string and opens vault3 if the string is the PIN
def vault3(player, args):
    if args == "1349" and player.room.name == "Knowledge Room" and player.floor.name == 'Vault':
        player.floor.rooms['Knowledge Room'].exits['east'] = 'Guts Room'
        player.send_text("The door unlocked!")
        return True

# takes an argument as a string and opens vault4 if the string is the PIN
def vault4(player, args):
    if args == "3295" and player.room.name == "Guts Room" and player.floor.name == 'Vault':
        player.floor.rooms['Guts Room'].exits['east'] = 'Tactics Room'
        player.send_text("The door unlocked!")
        return True

# takes an argument as a string and opens vault5 if the string is the PIN
def vault5(player, args):
    if args == "2487" and player.room.name == "Tactics Room" and player.floor.name == 'Vault':
        player.floor.rooms['Tactics Room'].exits['east'] = 'Luck Room'
        player.send_text("The door unlocked!")
        return True

# takes an argument as a string and opens vault6 if the string is the PIN
def vault6(player, args):
    if args == "2861" and player.room.name == "Luck Room" and player.floor.name == 'Vault':
        player.floor.rooms['Luck Room'].exits['east'] = 'Brave Room'
        player.send_text("The door unlocked!")
        return True

# takes an argument as a string and opens vault7 if the string is the PIN
def vault7(player, args):
    if args == "3889" and player.room.name == "Brave Room" and player.floor.name == 'Vault':
        player.floor.rooms['Brave Room'].exits['east'] = 'Finale'
        player.send_text("The door unlocked!")
        return True

