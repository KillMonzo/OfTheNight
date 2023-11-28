import random
import json

class Item:
    CATEGORIES = ["Electronic", "Wood", "Metal", "Paper", "Cloth", "Nature", "Glass", "Plastic", "Leather", "Arcane"]
    TYPES = ["Potion", "Equipment", "Artifact", "Book", "Gemstone", "Instrument", "Container", "Toy", "Tool"]
    RARITIES = ["common", "uncommon", "rare", "ultra-rare"]

    def __init__(self, name, description, categories, item_type, effect, rarity, max_uses=1, is_equipped=False):
        # Validations
        if not all(category in self.CATEGORIES for category in categories):
            raise ValueError(f"Invalid category. Valid categories are: {', '.join(self.CATEGORIES)}")
        if item_type not in self.TYPES:
            raise ValueError(f"Invalid item type. Valid types are: {', '.join(self.TYPES)}")
        if rarity not in self.RARITIES:
            raise ValueError(f"Invalid rarity. Valid rarities are: {', '.join(self.RARITIES)}")

        self.name = name
        self.description = description
        self.categories = categories
        self.item_type = item_type
        self.effect = effect
        self.rarity = rarity
        self.max_uses = max_uses
        self.current_uses = 0
        self.is_equipped = is_equipped

    def equip(self):
        self.is_equipped = True

    def unequip(self):
        self.is_equipped = False

    def apply_effect(self, target):
        """Apply the item's effect to a target. The exact functionality depends on the 'effect' attribute of the item."""
        if self.current_uses < self.max_uses:
            effect_type = self.effect.get("type")
            value = self.effect.get("value")
            
            if effect_type == "modifier":
                target.modifiers.append(value)  # Assuming target has a 'modifiers' attribute
            elif effect_type == "resolve":
                if value in target.phenomena:  # Assuming target has a 'phenomena' attribute
                    target.phenomena.remove(value)
            # ... [Other effect types here]

            self.current_uses += 1
            return f"{self.name}'s effect has been applied."
        else:
            return f"{self.name} has been used up and can no longer be used!"

    def display(self):
        """Display the item's details."""
        return (
            f"Item Name: {self.name}\n"
            f"Description: {self.description}\n"
            f"Categories: {', '.join(self.categories)}\n"
            f"Type: {self.item_type}\n"
            f"Effect: {self.effect}\n"
            f"Uses Remaining: {self.max_uses - self.current_uses}/{self.max_uses}\n"
            f"Equipped: {'Yes' if self.is_equipped else 'No'}"
        )

    def view_and_use_items(player):
      
      """Display the items in the player's inventory and give them the option to use an item."""
      if not player.items:
        print("\nYour inventory is empty!")
        return

      while True:
        print("\nYour Inventory:")
        for idx, item in enumerate(player.items, start=1):
            print(f"\nItem {idx}:")
            print(item.display())

        choice = input("\nWhich item do you want to use? (Enter the number or type '0' to go back): ")
        
        if choice.lower() == '0':
            break
        
        if choice.isdigit() and 1 <= int(choice) <= len(player.items):
            chosen_item = player.items[int(choice) - 1]
            chosen_item.apply_effect(player)
            print(f"You used {chosen_item.name}!")
        else:
            print("Invalid choice. Please try again.")

    def grant_ultra_rare_reward(player):
        if not ultra_rare_items:
            print("\nNo ultra-rare items left!")
            return

        reward_item = random.choice(ultra_rare_items)
        ultra_rare_items.remove(reward_item)
        player.items.append(reward_item)

        print(f"\nCongratulations! You've received an ultra-rare item:")
        print(reward_item.display())

    # Deck of items by rarity
with open('item_dictionary.json', 'r') as file:
    data = json.load(file)
    items_data = data['items']

# Create items
all_items = [Item(**item) for item in items_data]

# Sorting the items by rarity (optional)
common_items = [item for item in all_items if item.rarity == "common"]
uncommon_items = [item for item in all_items if item.rarity == "uncommon"]
rare_items = [item for item in all_items if item.rarity == "rare"]
ultra_rare_items = [item for item in all_items if item.rarity == "ultra-rare"]

