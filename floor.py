from room import Room

class Floor:

    # string representation of a Floor
    def __repr__(self):
            return (self.name + " on level " + str(self.number) 
                    + " with " + str(len(self.players)) + " player(s) on it.")

    def __init__(self, floor_dump, name):
        self.name = name
        self.class_ = floor_dump["class_"]
        self.number = floor_dump["number"]
        self.rooms = {}
        room_holder = floor_dump["rooms"] # no check for if it's empty because there should always be at least one room
        for value in room_holder:
            temp = Room(room_holder[value], value, self.number)
            self.rooms[temp.name] = temp
        self.players = set()

    # called when Player attempts to exit Floor
    def on_exit(self, player):
        if not player in self.players:
            raise Exception(player.name + " trying to leave floor they aren't on!")
        if not player.room.name in self.rooms.keys():
            raise Exception(player.name + " trying to leave floor from room not on that floor!")
        self.players.remove(player)
        player.room.on_exit(player, None)
        player.floor = None

    # called when Player attempts to enter Floor
    def on_entrance(self, player, room = "Elevator"):
        if not room in self.rooms.keys():
            raise Exception(player.name + " trying to enter floor into room that doesn't exist on that floor!")
        self.players.add(player)
        self.rooms[room].on_entrance(player, None)
        player.floor = self

    # given a string representing a Room name, returns Room object, else raises Exception
    def get_room(self, room_name):
        if room_name in self.rooms:
            return self.rooms[room_name]
        else:
            raise Exception("Room " + room_name + " doesn't exist on this floor.")

    # returns a dictionary of all Rooms on the Floor
    def get_rooms(self):
        return self.rooms