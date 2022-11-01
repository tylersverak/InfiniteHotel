import types
import actionfunctions

# map of string:function for each Action
func_dict = {"go":actionfunctions.go_to, "def":actionfunctions.default, "speak":actionfunctions.speak, "examine":actionfunctions.item_default,
             "pickup":actionfunctions.item_pickup, "drop":actionfunctions.item_dropoff,
             "inspect":actionfunctions.inspect, "Laszewo":actionfunctions.laszewo_room, 
             "listen to music":actionfunctions.listen_to_music, "elevator":actionfunctions.elevator_move, "read random book":actionfunctions.random_book,
             "play piano notes":actionfunctions.play_notes, "pull advanced guide 5":actionfunctions.basement_secret,
             "flip power switch":actionfunctions.lighthouse_switch, "steer toward shore":actionfunctions.steer_boat,
             "orb":actionfunctions.orb, "pull machine lever":actionfunctions.slot_machine, "dig":actionfunctions.dig, "jump":actionfunctions.cliff_jump,
             "grab the crawdad":actionfunctions.crawdad, "skip a rock":actionfunctions.skip, "swing":actionfunctions.swing,
             "toss a die":actionfunctions.toss, "shovel":actionfunctions.shovel, "scan":actionfunctions.scan,
             "stack rocks on the pile":actionfunctions.pile, "What is a cottus echinatus":actionfunctions.question_listener,
             "Mango":actionfunctions.question_listener, "Beer":actionfunctions.question_listener, "Orange Chicken":actionfunctions.question_listener,
             "1.8m":actionfunctions.question_listener, "Cow":actionfunctions.question_listener, "6430":actionfunctions.vault1,
             "5007":actionfunctions.vault2, "1349":actionfunctions.vault3, "3295":actionfunctions.vault4, "2487":actionfunctions.vault5,
             "2861":actionfunctions.vault6, "3889":actionfunctions.vault7}
param_set = set(("go", "speak", "examine", "inspect", "drop", "pickup", "elevator", "play piano notes")) # set of Actions that require parameters

class Action():

    # string representation of an Action
    def __repr__(self):
        if self.enabled:
            return ("Action " + self.name + " does: " + self.description_enabled)
        return("Action " + self.name + " does: " + self.description_disabled)

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

    # attempts to perform the Action given by a string argument from Player
    def try_use(self, player, args):
        if not self.enabled:
            player.send_text(self.description_disabled)
            return True
        if args == "" and self.parameters:
            player.send_text('no parameters found, please try again')
            return False
        if args != "" and not self.parameters: # if it doesn't take parameters, ignore them
            return self.use(player, "")
        else:
            return self.use(player, args)

    # given a Player and string parameters, returns the string form of the Action to be displayed to the Player
    # in the menu
    def get_command_name(self, player, parameters):
        res = "> "
        if self.name == "go":
            res += "GO * "
            for value in player.room.exits: # if room has no exits, GO will not be an option
                res += value + ", "
            return res[:-2]
        elif self.name == "examine" or self.name == "drop":
            res += self.name.upper() + " * "
            for value in player.items:
                res += value.name + ", "
            return res[:-2]
        elif self.name == "inspect":
            res += "INSPECT * "
            for value in player.room.features:
                name = value.name
                if value.has_action_by_name("inspect"):
                    res += name + ", "
            return res[:-2]
        elif self.name == "pickup":
            res += "PICKUP * "
            for value in player.room.items:
                res += value.name + ", "
            return res[:-2]
        elif self.name == "speak":
            return res + "SPEAK *"
        else:
            temp_str = self.name.split()
            temp_str[0] = temp_str[0].upper()
            if parameters:
                temp_str[0] += ' *'
            res += " ".join(temp_str)
            return res

    # enabled/disable Action
    def flip_enabled(self):
        self.enabled = not self.enabled