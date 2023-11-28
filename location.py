import random
import json
from phenomenon import Phenomenon, phenomenon_data

# Load affectation data and locations from JSON
with open('location_dictionary.json', 'r') as file:
    data = json.load(file)
    affectation_data = data['affectation_data']
    locations_data = data['locations']

# Class for Location
class Location:
    def __init__(self, name, description, ambiance, Gravity_Value, Gravity_Reasoning, Radiation_Value, Radiation_Reasoning, Atmosphere_Value, Atmosphere_Reasoning, StarEnergy_Value, StarEnergy_Reasoning, is_locked):
      
        self.name = name
        self.description = description
        self.ambiance = ambiance
        self.is_locked = is_locked
        self.phenomena = []
        self.is_visited = False
        self.cleared = False
        self.Gravity_Value = Gravity_Value
        self.Gravity_Reasoning = Gravity_Reasoning
        self.Radiation_Value = Radiation_Value
        self.Radiation_Reasoning = Radiation_Reasoning
        self.Atmosphere_Value = Atmosphere_Value
        self.Atmosphere_Reasoning = Atmosphere_Reasoning
        self.StarEnergy_Value = StarEnergy_Value
        self.StarEnergy_Reasoning = StarEnergy_Reasoning
        
        if self.name != "The Ship":
            self.draw_phenomena()

    def enter(self):
        """Handles the actions taken when a player enters a location."""
        if not self.is_visited:
            self.is_visited = True
            # If there's an inactive phenomenon, activate it
            if self.phenomena:
                self.phenomena[0].activate()
        return self

    def draw_phenomena(self):
        num_phenomena = random.randint(1, 4)  
        available_phenomena_ids = list(range(0, len(phenomenon_data)))
        drawn_ids = random.sample(available_phenomena_ids, min(num_phenomena, len(available_phenomena_ids)))
        for phenomenon_id in drawn_ids:
            new_phenomenon = Phenomenon(phenomenon_id)
            self.phenomena.append(new_phenomenon)

    def attempt_phenomenon(self):
        """Allows the player to attempt to resolve a phenomenon. Returns the phenomenon for further processing."""
        if self.phenomena:
            phenomenon = self.phenomena.pop(0)  # Pop the first phenomenon
            return phenomenon
        else:
            return None  # No more phenomena left to attempt


all_possible_locations = [Location(**location) for location in locations_data]
