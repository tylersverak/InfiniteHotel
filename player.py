from datetime import datetime
from datetime import timedelta
from action import Action
from feature import Feature
from item import Item
from twiliotext import send_twilio_text
import textwrap

class Player:

    # string representation of Player
    def __repr__(self):
        items = ""
        for value in self.items:
            items += value.name + ", "
        return (self.name + " the player is on floor " + str(self.floor.number) 
                + " room " + self.room.name + " and has items: " + items)   

    def __init__(self, player_dump) -> None:
        self.name = player_dump['name']
        self.phone_number = player_dump['phone_number']
        self.room = None # when put into room, room passes itself and the floor object to the player
        self.floor = None
        self.last_room = None
        self.timeout = datetime.now()
        self.speak_action = Action('speak', self)
        self.use_action = Action('examine', self)
        self.actions = [self.speak_action]
        self.items = []
        for value in player_dump['starting_items']:
            self.give_item(value)
        self.notified = False
        self.all_actions = {} # all possible actions for player

    # checks player, room, and item for all possible actions. actions are added
    # to the dictionary through a name:object pairing
    def update_actions(self):
        temp_actions = {}
        item_actions = []
        for value in self.items:
            item_actions.extend(value.get_actions())
        for action_list in [self.actions, self.room.get_actions(), item_actions]:
            for value in action_list:
                temp_actions[value.name.split()[0]] = value
        self.all_actions = temp_actions

    # returns all Actions the Player can perform
    def get_action_objects(self):
        return self.all_actions

    # returns the names of all Actions as a list of strings the Player can perform
    def get_actions(self):
        return self.all_actions.keys()

    # given a string 'name', returns the Item in the Player's inventory if it exists, else returns None
    def get_item(self, name):
        for value in self.items:
            if value.name == name:
                return value
        return None

    # times the Player out, so no input can be received or given to or from the Player until s seconds have ellasped
    def set_timeout(self, s):
        self.timeout = datetime.now() + timedelta(seconds = s)

    # given an Action name and arguments for that Action as a string, attempts to perform that acton
    def do_action(self, action_name, args):
        action = self.all_actions[action_name]
        if action.try_use(self, args): # if the user correctly input an action that could be used
            self.notified = False
            self.update_actions()

    # sends a text to the Player updating them on what options they can now pick
    def send_info_text(self):
        self.update_actions()
        message = ""
        if self.room != self.last_room: # only gives a room description if the player changed rooms
            message += self.room.description + '\n'
        self.last_room = self.room
        for value in self.all_actions.keys():
            action = self.all_actions[value]
            if not action.hidden:
                message += action.get_command_name(self, action.parameters) + '\n'
        message += 'What do you choose to do?'
        self.notified = True
        self.send_text(message)

    # add the Item to the Player's inventory. If they had no Items previously, gives them access to use Action
    def give_item(self, item):
        if len(self.items) == 0:
            self.actions.append(self.use_action)
        self.items.append(item)
        item.owner = self

    # creates an Item with the given data and gives it to the Player
    def make_item(self, item_dump, name):
        self.give_item(Item(item_dump, name, owner=self))

    # removes item from Player's inventory. Removes the use Action if the Player had no other items.
    def take_item(self, item):
        self.items.remove(item)
        item.owner = None
        if len(self.items) == 0:
            self.actions.remove(self.use_action)

    # takes a message as a string and texts it to the Player
    def send_text(self, message):
        if len(self.phone_number)<7:
            print(message)
            return
        if len(message) > 1500:
            chunks = textwrap.wrap(message, 1500)
            for value in chunks:
                send_twilio_text(value, to_num = self.phone_number)
        else:
            send_twilio_text(message, to_num = self.phone_number) 
        print("[" + self.name + "]: " + message)