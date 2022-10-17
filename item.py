from re import I
from action import Action

class Item:
    
    def __init__(self, item_dump, name, owner = None) -> None:
        self.name = name
        self.owner = owner
        self.image_name = item_dump.get("image_name")
        self.description = item_dump["description"]
        self.actions = []
        action_holder = item_dump['actions'] # item should always have some action, at least says description (for now items have one action)
        self.pickup_action = Action("pickup", self)
        self.drop_action = Action("drop", self)
        for value in action_holder:
            self.actions.append(Action(value, self))

    def get_actions(self):
        temp_actions = []
        for value in self.actions:
            temp_actions.append(value)
        if self.owner:
            temp_actions.append(self.drop_action)
        else:
            temp_actions.append(self.pickup_action)
        return temp_actions