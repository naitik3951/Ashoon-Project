import json

#Jus to create default structure or to reset game later, prob wont be used
def default():
    with open ("weapon_data.json", "w") as f:
        weapon = {
            "name" : "basic sword",
            "multipliers" : { #Passive ones
                    "health" : 1,
                    "attack" : 1.1,
                    "defence" : 1,
                    "speed" : 1,
            },

            "stats" : { #Extra which weapon provides
                    "health" : 0,
                    "attack" : 50,
                    "defence" : 0,
                    "speed" : 0,
            },

            "dot" : {},

            "crit" : {
                    "crate" : 0.2,
                    "cdmg" : 50,
            }
        }

        json.dump(weapon, f, indent=4)

def add():
    with open("weapon_data.json", "a") as f:
        json.dump("\n")

        name = str(input("Name of weapon : "))

        stats_used = ["health", "attack", "defence", "speed"]

        print("\n Multiplier input : ")
        multiplier_val = []
        for i in stats_used:
            multiplier_input = float(input(f"Enter multiplier of {i} : "))
            multiplier_val.append(multiplier_input)
        multipliers = dict(zip(stats_used, multiplier_val))

        print("\n Additive stat increase input : ")
        stats_val = []
        for i in stats_used:
            stats_input = float(input(f"Enter additive stat increase of {i} : "))
            stats_val.append(stats_input)
        stats = dict(zip(stats_used, stats_val))

        dot = {} #Will take input after i define system

        print("\n Taking crit input : ")
        crit_val = []
        for i in ["crate", "cdmg"]:
            crit_input = float(input(f"Enter value of {i} :" ))
            crit_val.append(crit_input)
        crit = dict(zip(["crate", "cdmg"], crit_val))

        weapon = {
            "name" : name,
            "multipliers" : multipliers,
            "stats" : stats,
            "dot" :dot,
            "crit" : crit
        }

        json.dump(weapon, f , indent=4)

add()