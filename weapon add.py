import json

with open("weapon_data.json", "a+") as f:
    name = str(input("Enter weapon name : "))
    weapon_damage_min = int(input("Enter minimum weapon attack : "))
    weapon_damage_max = int(input("Enter maximum weapon attack : "))
    crit_rate = int(input("Enter crit rate in percentage : "))
    crit_damage = int(input("Enter crit damage in percentage : "))
    status_effect = str(input("Enter status effect : "))
    status_effect_chance = int(input("Enter status effect chance : "))
