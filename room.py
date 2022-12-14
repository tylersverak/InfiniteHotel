from feature import Feature
from item import Item
from action import Action

class Room:

    # string representation of a Room
    def __repr__(self):
            feats = ""
            for value in self.features:
                feats += value.name + ', '
            if len(feats) > 0:
                feats = feats[:-2]
            return self.name + " room with " + str(len(self.players)) + " players in it and features [" + feats + ']'

    def __init__(self, room_dump, name, floornumber) -> None:
        self.name = name
        self.floornumber = floornumber
        self.entrances = room_dump["entrances"] # You are going this direction when you enter
        self.exits = room_dump["exits"] # You must go this direction to exit
        self.description = room_dump["description"]
        self.on_exit_message = room_dump.get("exit message")
        self.players = set()
        self.items = []
        self.features = []
        for value in self.exits.keys():
            door_data= {"description":"A door that leads " + value, "actions":["go"]}
            self.features.append(Feature(door_data, "Door to " + value))
        feature_holder = room_dump.get("features")
        if feature_holder:
            for value in feature_holder:
                self.features.append(Feature(feature_holder[value], value))
        item_holder = room_dump.get("items")
        if item_holder:
            for value in item_holder:
                self.items.append(Item(item_holder[value], value))

    # returns list of Actions that can be performed in the Room
    def get_actions(self):
        temp_actions = []
        for entity_list in self.items, self.features:
            for entity in entity_list:
                temp_actions.extend(entity.get_actions())
        return temp_actions

    # returns set of all Players in Room
    def get_players(self):
        return self.players

    # takes an argument as a string and if string is a name of a Feature in the Room, returns Feature, else returns None
    def get_feature(self, name):
        for value in self.features:
            if value.name == name:
                return value
        return None

    # takes an argument as a string and if string is a name of an Item in the Room, returns Item, else returns None
    def get_item(self, name):
        for value in self.items:
            if value.name == name:
                return value
        return None

    # called when Player tried to leave Room
    def on_exit(self, player, to_room):
        if self.on_exit_message:
            player.send_text(self.on_exit_message)
            player.set_timeout(5)
        player.room = None
        self.players.remove(player)
        for value in self.players:
            value.send_text(player.name + " left.")

    # called when Player tries to enter Room
    def on_entrance(self, player, from_room):
        if len(self.players) > 0:
            player.send_text('The players in this room are: ' + str(self.players))
        for value in self.players:
            value.send_text(player.name + " entered.")
        player.room = self
        self.players.add(player)

    # returns number of Players in the Room
    def player_count(self):
        return len(self.players)