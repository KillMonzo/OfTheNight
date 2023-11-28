import random
import json
from item import Item 

with open('character_dictionary.json', 'r') as file:
    data = json.load(file)

class Character:
    def __init__(self):
        self.name = self.generate_name()
        self.profession_key, profession_data = self.choose_profession()
        self.profession = profession_data['profession_name']
        self.description = random.choice(data['descriptions'])
        self.goal = random.choice(data['goals'])

        self.piloting_value = profession_data['affectations']['Piloting']["value"]
        self.engineering_value = profession_data['affectations']['Engineering']["value"]
        self.diplomacy_value = profession_data['affectations']['Diplomacy']["value"]
        self.combat_value = profession_data['affectations']['Combat']["value"]
        self.research_value = profession_data['affectations']['Research']["value"]
        self.survival_value = profession_data['affectations']['Survival']["value"]
      
        self.gravity_value = profession_data['affectations']['Gravity']["value"]
        self.radiation_value = profession_data['affectations']['Radiation']["value"]
        self.atmosphere_value = profession_data['affectations'][
            'Atmosphere']["value"]
        self.starenergy_value = profession_data['affectations'][
            'Star Energy']["value"]
        #self.affectations = self.parse_data(profession_data, 'affectations')
        self.skills = self.parse_data(profession_data, 'skills')

    def generate_name(self):
        """Generate a random name from the data."""
        first_name = random.choice(data['first_names'])
        last_name = random.choice(data['last_names'])
        return f"{first_name} {last_name}"

    def choose_profession(self):
        """Randomly choose a profession from the data."""
        profession_key = random.choice(list(data['professions'].keys()))
        return profession_key, data['professions'][profession_key]

    def parse_data(self, profession_data, key):
        """Parse either affectations or skills from profession data."""
        details_dict = {}
        for item, (value, reasoning) in profession_data[key].items():
            details_dict[item] = {
                'value': value,
                'reasoning': reasoning
            }
        return details_dict

    def display(self):
        """Return a formatted string of the character's details."""
        details = f"Name: {self.name}\nProfession: {self.profession}\nDescription: {self.description}\nGoal: {self.goal}\n"
        affectation_details = self.format_details(self.affectations, "Affectations")
        skill_details = self.format_details(self.skills, "Skills")
        return details + affectation_details + skill_details

    def format_details(self, details_dict, title):
        """Format the affectations or skills details."""
        formatted_details = f"\n{title}:\n"
        for key, data in details_dict.items():
            formatted_details += f"{key}: {data['value']} - {data['reasoning']}\n"
        return formatted_details

# Sample usage:


    def character_selection():
      """Lets the player select a character from a list of 5 randomly generated characters.Returns the chosen character."""
    # Generate 5 random characters
      random_characters = [Character() for _ in range(5)]

    # Display them to the player
      print("Choose your character:")
      for index, character in enumerate(random_characters, start=1):
        print(f"\nCharacter {index}:")
        print(character.display())
        print("\n" + "-"*50 + "\n")

    # Let the player choose a character
      while True:
        choice = input("Enter the number corresponding to your choice (1-5): ")
        if choice.isdigit() and 1 <= int(choice) <= 5:
            chosen_character = random_characters[int(choice) - 1]
            return chosen_character

        print("Invalid choice. Please try again.")

    def view_character_details(player,game):
      """Display the character's details and provide options to view Skills, Affectations, and Items."""
      print(f"\nName: {player.name}")
      print(f"Description: {player.description}")
      print(f"Goal: {player.goal}\n")

      while True:
        print("\nOptions:")
        print("0. Go Back")
        print("1. View Skills")
        print("2. View Affectations")
        print("3. View Items")
        
        choice = input("\nEnter your choice: ")

        if choice == "1":
          print("\nSkills:")
          for skill, details in player.skills.items():
            value = details.get('value', '')
            reasoning = details.get('reasoning', '')
            print(f"{skill}: {value} - {reasoning}")
        elif choice == "2":
            print("\nAffectations:")
            for affectation, details in player.affectations.items():
              value = details.get('value', '')
              reasoning = details.get('reasoning', '')
              print(f"{affectation}: {value} - {reasoning}")  
        elif choice == "3":
            Item.view_and_use_items(player)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")
