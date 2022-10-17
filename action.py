import types
import action_functions


func_dict = {"go":action_functions.go_to, "def":action_functions.default, "speak":action_functions.speak, "use":action_functions.item_default,
             "pickup":action_functions.item_pickup, "drop":action_functions.item_dropoff, "itemdefault":action_functions.item_default,
             "inspect":action_functions.inspect, "open laszewo room":action_functions.laszewo_room, 
             "listen to music":action_functions.listen_to_music, "elevator":action_functions.elevator_move}
param_set = set(("go", "speak", "use", "inspect", "drop", "pickup", "elevator"))

class Action():

    def __repr__(self):
            return ("Action " + self.name + " does: " + self.description_enabled)

    def __init__(self, name, owner, enabled = True, description_enabled = None, description_disabled = None, hidden = False) -> None:
        self.name = name
        self.parameters = (self.name in param_set)
        self.hidden = hidden
        self.description_enabled = name + " is enabled"
        self.description_disabled = name + " is disabled"
        if description_enabled:
            self.description_enabled = description_enabled
        if description_disabled:
            self.description_disabled = description_disabled
        self.owner = owner
        self.use = func_dict['def']
        if self.name in func_dict.keys():
            self.use = func_dict[self.name] # later need to have a dict of name:function for each action, with default being "default_func"
        self.enabled = enabled
        self.notified = False

    def try_use(self, player, args):
        if args == "" and self.parameters:
            print('no parameters found, please try again') # text to player
            return False
        if args != "" and not self.parameters: # if it doesn't take parameters, ignore them
            return self.use(player, "")
        else:
            return self.use(player, args)

    def get_command_name(self, player):
        res = "> "
        if self.name == "go":
            res += "GO "
            for value in player.room.exits: # assumes room has at least one exit, which it should
                res += value + ", "
            return res[:-2]
        elif self.name == "use" or self.name == "drop":
            res += self.name.upper() + " "
            for value in player.items:
                res += value.name + ", "
            return res[:-2]
        elif self.name == "inspect":
            res += "INSPECT "
            for value in player.room.features:
                name = value.name
                if value.has_action_by_name("inspect"):
                    res += name + ", "
            return res[:-2]
        elif self.name == "pickup":
            res += "PICKUP "
            for value in player.room.items:
                res += value.name + ", "
            return res[:-2]
        else:
            temp_str = self.name.split()
            temp_str[0] = temp_str[0].upper()
            res += " ".join(temp_str)
            return res

'''
each action's function has to have its own logic for catching argument edgecases,
and how to handle in the case of too much or bad input
'''