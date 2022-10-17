from action import Action
from feature import Feature

class Player:

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
        self.speak_action = Action('speak', self)
        self.use_action = Action('use', self)
        self.actions = [self.speak_action]
        self.items = []
        for value in player_dump['starting_items']:
            self.give_item(value)
        self.flags = {}
        self.next_message = "Hello welcome" # didn't document this now I dont know what it does
        self.notified = False
        self.all_actions = {} # all possible actions for player

    def get_flags(self):
        return self.flags

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

    def get_action_objects(self):
        return self.all_actions

    def get_actions(self):
        return self.all_actions.keys()

    def do_action(self, action_name, args):
        action = self.all_actions[action_name]
        #if action.hidden: #disable hidden actions until discovered?
        #    print('not a valid option, please try again')
        #    return
        if action.try_use(self, args): # if the user correctly input an action that could be used
            self.notified = False
            self.update_actions()
            print('*************************************************************') # remove after debugging

    def send_text(self):
        message = ""
        if self.room != self.last_room:
            message += self.room.description + '\n'
        self.last_room = self.room
        for value in self.all_actions.keys():
            action = self.all_actions[value]
            if not action.hidden:
                message += self.all_actions[value].get_command_name(self) + '\n'
        message += 'What do you choose to do?' # maybe for debugging only
        self.notified = True
        print("[DEBUG] " + self.name + ' got sent: \n' + message) # change to sending text later

    def give_item(self, item):
        if len(self.items) == 0:
            self.actions.append(self.use_action)
        self.items.append(item)
        item.owner = self

    def take_item(self, item):
        self.items.remove(item)
        item.owner = None
        if len(self.items) == 0:
            self.actions.remove(self.use_action)



'''
functionality for now
speak, move rooms, interact with feature, get item, use item, leave item
'''