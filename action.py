import types
import actionfunctions


func_dict = {"go":actionfunctions.go_to, "def":actionfunctions.default, "speak":actionfunctions.speak, "use":actionfunctions.item_default,
             "pickup":actionfunctions.item_pickup, "drop":actionfunctions.item_dropoff, "itemdefault":actionfunctions.item_default,
             "inspect":actionfunctions.inspect, "open laszewo room":actionfunctions.laszewo_room, 
             "listen to music":actionfunctions.listen_to_music, "elevator":actionfunctions.elevator_move, "read random book":actionfunctions.random_book,
             "play piano notes":actionfunctions.play_notes, "pull advanced guide 5":actionfunctions.basement_secret}
param_set = set(("go", "speak", "use", "inspect", "drop", "pickup", "elevator", "play piano notes"))

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
        self.use = func_dict.get(self.name, func_dict['def'])
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