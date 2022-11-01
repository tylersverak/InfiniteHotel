from action import Action

class Feature():

    # string representation of a Feature
    def __repr__(self):
            return ("Feature called " + self.name + ' that does ' + ("nothing" if self.actions == [] else "some actions"))

    def __init__(self, feature_dump, name) -> None:
        self.name = name
        self.image_name = feature_dump.get("image_name")
        self.description = feature_dump["description"]
        self.actions = []
        self.hidden_actions = []
        self.custom_actions = []
        hidden_holder = feature_dump.get("hidden actions")
        action_holder = feature_dump.get("actions")
        custom_holder = feature_dump.get("custom actions") # custom actions require more info from other Actions
        if action_holder:
            for value in action_holder:
                self.actions.append(Action(value, self))
        if hidden_holder:
            for value in hidden_holder:
                self.hidden_actions.append(Action(value, self, hidden=True))
        if custom_holder:
            for value in custom_holder:
                temp = Action(value, self, enabled=custom_holder[value]["enabled"], description_enabled=custom_holder[value]["description enabled"],
                    description_disabled=custom_holder[value]["description disabled"], hidden=custom_holder[value]["hidden"])
                self.actions.append(temp)

    # returns all Actions the feature has in a list
    def get_actions(self):
        temp_actions = []
        temp_actions.extend(self.actions)
        temp_actions.extend(self.hidden_actions)
        return temp_actions

    # takes an argument as a string and if string is an Action name, returns True, else return False
    def has_action_by_name(self, action_name):
        for value in self.get_actions():
            if value.name == action_name:
                return True
        return False