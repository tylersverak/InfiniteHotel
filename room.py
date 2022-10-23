from feature import Feature
from item import Item
from action import Action

class Room:

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
                print(item_holder[value])
                self.items.append(Item(item_holder[value], value)) # STILL NEED TO HANDLE FINDING ITEMS

    def get_actions(self):
        temp_actions = []
        for entity_list in self.items, self.features:
            for entity in entity_list:
                temp_actions.extend(entity.get_actions())
        return temp_actions

    def get_flags(self):
        return self.flags

    def on_exit(self, player, to_room):
        if self.on_exit_message:
            player.send_text(self.on_exit_message)
            player.set_timeout(5)
        player.room = None
        self.players.remove(player)

    def on_entrance(self, player, from_room):
        player.room = self
        self.players.add(player)

    def on_feature_use(self, player, feature, player2):
        pass

    def on_item_use(self, player, item, player2):
        pass

    def player_count(self):
        return len(self.players)

'''
elevator room should handle room flags because evrey floor should have that
also might not need two elevator rooms for quarantine depending on how to
interact with elevator
'''