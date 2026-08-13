import random

class Fighter:
    def __init__(self, name, hp, attack, speed, move_name):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack_power = attack
        self.speed = speed
        self.move_name = move_name

    def is_alive(self):
        return self.hp > 0

    def attack(self, target):
        damage = random.randint(self.attack_power - 3, self.attack_power + 3)
        target.hp -= damage
        if target.hp < 0:
            target.hp = 0
        print(f"{self.name} uses {self.move_name} on {target.name} for {damage} damage!")

def run_turn(p1, p2, p1_action, p2_action):
    # Determine order based on speed
    if p1.speed >= p2.speed:
        first, second = p1, p2
        first_act, second_act = p1_action, p2_action
    else:
        first, second = p2, p1
        first_act, second_act = p2_action, p1_action

    # First attacker's turn
    if first.is_alive():
        if first_act == "attack":
            first.attack(second)
        elif first_act == "run":
            print(f"{first.name} tries to run away!")
            return "run"

    # Second attacker's turn (if still alive)
    if second.is_alive():
        if second_act == "attack":
            second.attack(first)
        elif second_act == "run":
            print(f"{second.name} tries to run away!")
            return "run"
    
    return "continue"

# Example Battle Setup
player = Fighter("Hero", 50, 12, 10, "Slash")
enemy = Fighter("Goblin", 40, 10, 8, "Bite")

# Main Loop Example
while player.is_alive() and enemy.is_alive():
    print(f"\n{player.name} HP: {player.hp}/{player.max_hp} | {enemy.name} HP: {enemy.hp}/{enemy.max_hp}")
    
    # Get player choice
    choice = input("Do you want to [attack] or [run]?: ").strip().lower()
    if choice not in ["attack", "run"]:
        continue
        
    # Enemy simple AI choice
    enemy_choice = "attack"
    
    result = run_turn(player, enemy, choice, enemy_choice)
    
    if result == "run":
        print("Battle ended by escape.")
        break
        
if not player.is_alive():
    print("\nYou lost the battle!")
elif not enemy.is_alive():
    print(f"\nYou defeated {enemy.name}!")
