from player import Player
from location import Location, all_possible_locations
from phenomenon import Phenomenon, phenomenon_data
from item import Item, common_items, uncommon_items, rare_items, ultra_rare_items
from character import Character
import random

available_locations = all_possible_locations.copy()

class Area:
    def __init__(self, name):
        global available_locations
        self.name = name
        chosen_locations = random.sample(available_locations, random.randint(1, 2))
        the_ship = Location(
            name="The Ship",
            description="A state-of-the-art spaceship designed for intergalactic exploration and adventure. Its sleek metal exterior shines brightly among the stars.",
            ambiance="Soft hum of the engines, gentle glow of instrument panels, and the distant view of space through the windows.",
            affectations={
                'Gravity': (0, 'Artificial gravity ensures everyone moves comfortably.'),
                'Radiation': (0, 'Shields protect against harmful space radiation.'),
                'Atmosphere': (0, 'Controlled atmosphere suitable for crew members.'),
                'Star Energy': (0, 'Neutral star energy due to the ship’s advanced systems.')
            },
            is_locked=False
        )
        self.locations = [the_ship] + chosen_locations
        for loc in chosen_locations:
            available_locations.remove(loc)

class GameState:
    def __init__(self):
        self.active_phenomena = []
        self.item_deck = common_items + uncommon_items + rare_items + ultra_rare_items
        self.areas = [Area(name) for name in ["Alpha", "Beta", "Delta", "Gamma"]]
        self.current_area = self.areas[0]  # Start at "Alpha"
        self.current_location = self.current_area.locations[0]
        # Start at "The Ship" in "Alpha"

def display_location(player, game):
    print(f"\nWelcome, {player.name}!")
    print(f"\nCurrent Area: {game.current_area.name}")
    print(f"Current Location: {player.current_location.name}")
    print(f"\nAmbiance: {player.current_location.ambiance}")
    print(f"Gravity: {player.current_location.Gravity_Value}: {player.current_location.Gravity_Reasoning}")
    print(f"Radiation: {player.current_location.Radiation_Value}: {player.current_location.Radiation_Reasoning}")
    print(f"Atmosphere: {player.current_location.Atmosphere_Value}: {player.current_location.Atmosphere_Reasoning}")
    print(f"\nStar Energy: {player.current_location.Star_Energy_Value}: {player.current_location.Star_Energy_Reasoning}")
    print(f"\n{player.current_location.description}")
    print(f"\nNumber of Phenomena at this location: {len(player.current_location.phenomena)}")    

def interact_with_phenomenon(player: Player, game):

    unresolved_phenomena = [p for p in player.current_location.phenomena if not p.resolved]
    
    # Activate the next phenomenon if only 1 is currently active
    active_phenomena = [p for p in unresolved_phenomena if p.active]
    if len(active_phenomena) == 0:
      next_phenomenon = unresolved_phenomena[0]
      next_phenomenon.activate()
      active_phenomena.append(next_phenomenon)
      # If no unresolved phenomena, grant ultra-rare reward and move player
    
    print("\nPhenomenon Detected!\n")
    for idx, phenomenon in enumerate(active_phenomena, 1):
        phenomenon_details = phenomenon.display()  # Get the details of the phenomenon
        print(f"{idx}. {phenomenon_details}")

    choice = int(input("Choose a phenomenon to interact with or '0' to draw another: "))

    if choice == 0:
        if len(active_phenomena) < len(unresolved_phenomena):
            next_phenomenon = unresolved_phenomena[len(active_phenomena)]
            next_phenomenon.activate()
            interact_with_phenomenon(player, game)
            return
        else:
            print("All phenomena at this location are active.")
            return

    active_phenomenon = active_phenomena[choice - 1]

    required_skill = active_phenomenon.associated_skill
    required_skill_value = active_phenomenon.skill_check
    player_skill_value = player.skills[required_skill]['value']

    print(f"\nSkill Check: {required_skill} {required_skill_value}")
    print(f"Your {required_skill} Skill Level: {player_skill_value}\n")

    print("\nWould you like to try and resolve this phenomenon?")
    print("\nActions:")
    print("0. Do not attempt")
    print("1. Attempt skill check")
    
    # Check if player has the required item
    has_required_item = any(item for item in player.items if item.item_type == active_phenomenon.secondary_requirement)
    if has_required_item:
        print("2. Use a required item")
    choice = input("\nEnter your choice: ")
    
    if choice == '1':
        skill_met = skill_check(player_skill_value, required_skill_value)
        result_msg, reward_item_name, resolved = active_phenomenon.resolve(player, skill_met)
    elif choice == '2' and has_required_item:
        # Using an item to resolve the phenomenon
        required_item = next(item for item in player.items if item.item_type == active_phenomenon.secondary_requirement)
        player.items.remove(required_item)  # Remove the item from player's inventory
        print(f"\nYou used the {required_item.name} to resolve the phenomenon!")
        result_msg, reward_item_name, resolved = active_phenomenon.resolve(player, True)  # Assume item use always resolves
    else:
      return
    if resolved and active_phenomenon in player.current_location.phenomena:
        player.current_location.phenomena.remove(active_phenomenon)
        print(result_msg)

    if reward_item_name:
            reward_item = next((item for item in game.item_deck if item.name == reward_item_name), None)
            if reward_item:
                player.items.append(reward_item)
                game.item_deck.remove(reward_item)
                print(f"\nYou have gained a new item: {reward_item.name}")
                print(f"Description: {reward_item.description}")

    location_clear_check(player,game)
                
def skill_check(player_skill_value, required_skill_value) -> bool:
    """Perform a skill check."""
    dice_roll = random.randint(1, 6)  # Assuming a D6 roll
    total_check_value = player_skill_value + dice_roll
    print(f"\nSkill Level: {player_skill_value}")
    print(f"Dice Roll: {dice_roll}")
    print(f"Total: {total_check_value}")
    
    if total_check_value >= required_skill_value:
        print(f"Success! Needed a {required_skill_value} or higher.")
        return True
    else:
        print(f"Failed! Needed a {required_skill_value} or higher.")
        return False
    
def location_clear_check(player,game):
  
    unresolved_phenomena = [p for p in player.current_location.phenomena if not p.resolved]
    if not unresolved_phenomena and player.current_location.name != 'The Ship':
                    print("\nThis location is cleared of Phenomena!")
                    Item.grant_ultra_rare_reward(player)
                    player.add_cleared_location(player.current_location.name)
                    player.current_location = game.current_area.locations[0]
                    return
      
def move_location_or_area(player, game):
    # Display all locations except the current one.
    all_locations = [
        location for location in game.current_area.locations 
        if location.name != player.current_location.name
    ]

    print("\nChoose a location within the current area:")
    for i, location in enumerate(all_locations, 1):
        status = " (Cleared)" if location.name in player.cleared_locations else ""
        print(f"{i}. {location.name}{status}")

    print("\nChoose another area to move to:")
    total_options_within_area = len(all_locations)  # This gives the total count of options in the current area
    for idx, area in enumerate(game.areas, start=total_options_within_area):
        if area != game.current_area:  # Do not show the current area as an option
            print(f"{idx}. {area.name}")

    choice = int(input("\nEnter your choice: "))

    if 1 <= choice <= total_options_within_area:
        selected_location = all_locations[choice - 1]
        if selected_location.name in player.cleared_locations:
            print("\nThis location is already cleared. Choose another location or area.")
            return move_location_or_area(player, game)  # Recall the function to allow the player to select again
        else:
            player.current_location = selected_location
    elif total_options_within_area + 1 <= choice <= total_options_within_area + len(game.areas):
        game.current_area = game.areas[choice - total_options_within_area - 1]
        player.current_location = game.current_area.locations[0]  # Set to "The Ship"
    else:
        print("Invalid choice.")
        return move_location_or_area(player, game)  # Recall the function to allow the player to select again

def main_actions(player, game):

    # Display location details
    display_location(player, game)
  
    actions = [
        ("View Character", Character.view_character_details),
        ("Move", move_location_or_area),
    ]
    
    if player.current_location.name != 'The Ship':
        actions.insert(0, ("Interact with Phenomena", interact_with_phenomenon))
    
    actions.append(("Exit game", None))

    # Display actions and get user choice
    for i, (action_text, _) in enumerate(actions, 1):
        print(f"{i}. {action_text}")
    choice = input("\nEnter your choice: ")
    
    if choice.isdigit() and 1 <= int(choice) <= len(actions):
        action_fn = actions[int(choice) - 1][1]
        if action_fn:
            action_fn(player,game)
    else:
        print("Invalid choice. Please try again.")

def main():
    game = GameState()

    # Character selection
    chosen_char = Character.character_selection()
    print("\nYou have chosen:")
    print(chosen_char.display())
    player = Player(chosen_char)
    # Assign starting location and items to the player
    player.current_location = game.current_location  # Set to "The Ship" in "Alpha"
    # Assign starting items to the player
    starting_items = random.sample(uncommon_items, 2)
    player.items.extend(starting_items)
    for item in starting_items:
        uncommon_items.remove(item)
    
    while True:
        main_actions(player, game)
      
if __name__ == "__main__":
    main()