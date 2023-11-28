from character import Character

class Player:
  
    def __init__(self, character: Character):
        # Inheriting attributes from the chosen character
        self.name = character.name
        self.profession_key = character.profession_key
        self.profession = character.profession
        self.description = character.description
        self.goal = character.goal
        self.affectations = character.affectations
        self.skills = character.skills
        
        # Gameplay specific attributes
        self.items = []
        self.current_location = None
        self.max_actions = 3
        self.remaining_actions = self.max_actions
        self.cleared_locations = []
        

    def use_action(self):
        if self.remaining_actions > 0:
            self.remaining_actions -= 1

    def reset_actions(self):
        self.remaining_actions = self.max_actions

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
          
    def add_cleared_location(self,location):
        #player.current_location.cleared = True
        self.cleared_locations.append(location)
        #print (f"{self.current_location} is cleared")
    # Other methods for altering stats, interacting with items, etc. can be added here
