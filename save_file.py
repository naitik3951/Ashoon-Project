import json

def default():
    with open("save_file.json", "w") as f:
        progress = {
            "stage_level" : 1,
            "player_level" : 1,
            "enemies_defeated" : {}
        }

        stats = {
            "health" : 100,
            "attack" : 100,
            "defence" : 100,
            "speed" : 50
        }

        moves = {
            "cut" : {
                "damage" : 10,
                "selfbuff" : {},
                "debuff" : {},
                "dot" : {}
            },

            "block" : {
                "damage" : 0,
                "selfbuff" : {
                    "defence buff" : [1.5, 2, "defence"]
                },
                "debuff" : {},
                "dot" : {}
            }
        }

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

        save = {
            "progress" : progress,
            "stats" : stats,
            "moves" : moves,
            "weapon" : weapon,
        }

        json.dump(save, f, indent=4) #Indent so that it looks better

default()