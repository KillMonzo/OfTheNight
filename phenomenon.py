import random
import json
from entity import Entity
from item import Item, common_items, uncommon_items, rare_items, ultra_rare_items

# Load predefined Phenomena data from the JSON file
with open('phenomenon_dictionary.json', 'r') as file:
    phenomenon_data = json.load(file)

class Phenomenon:
    def __init__(self, phenomenon_id):
        #print(phenomenon_data)    
        self.data = phenomenon_data[str(phenomenon_id)]
        #[phenomenon_id]
        self.entity = Entity()
        self.description = self.data["description"]
        self.effect = self.data["effect"]
        self.difficulty = self.data["difficulty"]
        self.skill_check = self.data["skill_check"]
        self.associated_skill = self.data["associated_skill"]
        self.secondary_requirement = self.data["secondary_requirement"]
        self.resolved = False
        self.active = False
  
    def activate(self):
        """Make this phenomenon active and show its effects."""
        self.active = True

    def resolve(self, player, skill_met: bool):
      """Resolve the phenomenon, make it inactive, and grant the player the reward."""
      secondary_met = self.meets_secondary_requirement(player)

      if skill_met or secondary_met:  # Either the skill or secondary requirements are met
        self.resolved = True
        self.active = False
        reward_item_name = self.grant_reward()
        return f"Phenomenon resolved! You receive: {reward_item_name}", reward_item_name, True
      elif not skill_met:
        return "Failed to resolve due to insufficient skill.", None, False
      elif not secondary_met:
        return "Failed to resolve due to missing required item.", None, False
      else:
        return "Failed to resolve the phenomenon.", None, False





    def _meets_skill_requirement(self, player):
      """Check if the player's skill is sufficient to resolve the phenomenon."""
      dice_roll = self._roll_d6()
      player_skill_value = getattr(player, self.associated_skill.lower(), 0)
      

    # Display information to the player
      print(f"\nAssociated Skill: {self.associated_skill}")
      print(f"Your {self.associated_skill} Level: {player_skill_value}")
      print(f"Dice Roll: {dice_roll}")
      total_check_value = player_skill_value + dice_roll
      print(f"Total (Skill Level + Dice Roll): {total_check_value}")
    
    # Check for success and print the result
      if total_check_value >= self.skill_check:
        print(f"Success! Needed a {self.skill_check} or higher.")
        return True
      else:
        print(f"Failed! Needed a {self.skill_check} or higher.")
        return False


    def _roll_d6(self):
        """Simulate rolling a 6-sided dice."""
        return random.randint(1, 6)

    def grant_reward(self):
      """Grants a reward to the player based on the difficulty of the phenomenon."""
      if self.difficulty == "Common":
        reward_pool = common_items
      elif self.difficulty == "Uncommon":
        reward_pool = common_items + uncommon_items
      else:  # for rare
        reward_pool = common_items + uncommon_items + rare_items

      #print(f"Reward pool for {self.difficulty}: {reward_pool}")  # Debugging line

    # Ensure there's a reward available to give
      if not reward_pool:
        return "No items left to give as rewards."

    # Choose and remove the item from its deck
      reward_item = random.choice(reward_pool)
      if reward_item in common_items:
        common_items.remove(reward_item)
      elif reward_item in uncommon_items:
        uncommon_items.remove(reward_item)
      elif reward_item in rare_items:
        rare_items.remove(reward_item)
    
      return reward_item.name


    def meets_secondary_requirement(self, player):
        """Check if the player has the required item."""
        required_item_type = self.secondary_requirement

        return any(item for item in player.items if required_item_type == item.item_type)

    def display(self):
        return (
            f"\nRace: {self.entity.race}\n"
            f"Name: {self.entity.name}\n"
            f"Description: {self.description}\n"
            f"Skill Check: {self.skill_check} {self.associated_skill}\n"
            f"Secondary Requirement: {self.secondary_requirement}\n"
            #f"Reward: {self.reward}"
        )
