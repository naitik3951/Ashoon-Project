import random
import json

#To set these 2 as global variables
playerdata = {} 
enemydata = {}

def load_data():
    global playerdata, enemydata

    with open("game_data/save_file.json", "r") as save_data, open("game_data/weapon_data.json", "r") as weapon_data: #../ tells python to go up 1 folder
        data = json.load(save_data)
        weapons = json.load(weapon_data)
        playerdata = {
            "stats" : data["stats"],
            "moves" : data["moves"],
            "weapon" : weapons[data["weapon"]]
        }

    with open("game_data/enemy_data.json", "r") as enemy_data_file:
        enemies  = json.load(enemy_data_file)
        encounter = "void_tyrant" #Set ourselves for now as encouinter happening is up to pygame ppl
        enemydata = enemies[encounter]

    return playerdata, enemydata

def speed_sys(progress, status):
    pav = (progress["player"]["pdist"]
           / ((playerdata["stats"]["speed"] + playerdata["weapon"]["stats"]["speed"])
                *status["buff"]["multipliers"]["player"]["speed"]
                *status["debuff"]["multipliers"]["player"]["speed"]
                *playerdata["weapon"]["multipliers"]["speed"]
                )
           )

    eav = (progress["enemy"]["edist"]
            /(enemydata["speed"]
                *status["buff"]["multipliers"]["enemy"]["speed"]
                *status["debuff"]["multipliers"]["enemy"]["speed"]    
                )
           )

    if pav<eav:
        next_turn = "player"
    elif eav<pav:
        next_turn = "enemy"
    else:
        next_turn = random.choice(["player", "enemy"])

    return next_turn

def buff_duration(move, next_turn, status):
    #Adding selfbuffs
    for i in move["selfbuff"]:
        buff_data = move["selfbuff"][i]
        buff_name = i

        multiplier = buff_data[0]
        duration = buff_data[1]

        if buff_data[-1] == "attack":
            status["buff"][next_turn]["attack"][buff_name] = [multiplier, duration + 1]  # +1 cus in next loop it removes 1 turn from the buff
        elif buff_data[-1] == "speed":
            status["buff"][next_turn]["speed"][buff_name] = [multiplier, duration + 1] 
        elif buff_data[-1] == "defence" :
            status["buff"][next_turn]["defence"][buff_name] = [multiplier, duration + 1] 

    #Code status decreasing here
    expired = []
    for buff_type in status["buff"][next_turn]:
        for buff_name in status["buff"][next_turn][buff_type]:
            buff_data = status["buff"][next_turn][buff_type][buff_name]
            if buff_data[-1]>0:
                buff_data[-1] -= 1
            else:
                expired.append([buff_type, buff_name])

    #Delete seperately cus deleting together was annyoing
    for to_delete in expired:
        del status["buff"][next_turn][to_delete[0]][to_delete[1]]

def buff_calculations(next_turn, status):
    for buff_type in status["buff"][next_turn]:
        status["buff"]["multipliers"][next_turn][buff_type] = 1
        for buff_name in status["buff"][next_turn][buff_type]:
            multiplier = status["buff"][next_turn][buff_type][buff_name][0]
            status["buff"]["multipliers"][next_turn][buff_type] *= multiplier

def debuff_duration(move, opponent, status):
    #Adding debuffs
    for i in move["debuff"]:
        buff_data = move["debuff"][i]
        buff_name = i

        multiplier = buff_data[0]
        duration = buff_data[1]

        if buff_data[-1] == "attack":
            status["debuff"][opponent]["attack"][buff_name] = [multiplier, duration + 1]  # +1 cus in next loop it removes 1 turn from the buff
        elif buff_data[-1] == "speed":
            status["debuff"][opponent]["speed"][buff_name] = [multiplier, duration + 1] 
        elif buff_data[-1] == "defence" :
            status["debuff"][opponent]["defence"][buff_name] = [multiplier, duration + 1] 

    #Code status decreasing here
    expired = []
    for buff_type in status["debuff"][opponent]:
        for buff_name in status["debuff"][opponent][buff_type]:
            buff_data = status["debuff"][opponent][buff_type][buff_name]
            if buff_data[-1]>0:
                buff_data[-1] -= 1
            else:
                expired.append([buff_type, buff_name])

    #Delete seperately cus deleting together was annyoing
    for to_delete in expired:
        del status["debuff"][opponent][to_delete[0]][to_delete[1]]  

def debuff_calculations(opponent, status):
#Similar to buff calculations
    for buff_type in status["debuff"][opponent]:
        status["debuff"]["multipliers"][opponent][buff_type] = 1
        for buff_name in status["debuff"][opponent][buff_type]:
            multiplier = status["debuff"][opponent][buff_type][buff_name][0]
            status["debuff"]["multipliers"][opponent][buff_type] *= multiplier

#Recode using debuff
def damage_calculation(next_turn, move, status):
    if next_turn == "player":
        #Expeidiont 33 type dmg fomrula here
        base_dmg = move["damage"]

        attack_multiplier = (
        (playerdata["stats"]["attack"] + playerdata["weapon"]["stats"]["attack"]) 
        * (status["buff"]["multipliers"]["player"]["attack"]) 
        * (status["debuff"]["multipliers"]["player"]["attack"])
        * playerdata["weapon"]["multipliers"]["attack"]
        )

        defence_multiplier = (
        10000
        / (
            (enemydata["defence"])
            *status["buff"]["multipliers"]["enemy"]["defence"]
            *status["debuff"]["multipliers"]["enemy"]["defence"]
            +10000
            )
        )

        #Crit dmg part
        if random.random() < (playerdata["weapon"]["crit"]["crate"]) / 100:
            crit_multiplier = 1 + playerdata["weapon"]["crit"]["cdmg"] / 100 # 250 cdmg = 1 + 2.5 = 3.5, 50 cdmg = 1 + .5 = 1.5
            did_crit = True
        else:
            crit_multiplier = 1
            did_crit = False

        return(base_dmg * attack_multiplier * defence_multiplier * crit_multiplier), did_crit

    elif next_turn == "enemy":
        base_dmg = move["damage"]

        attack_multiplier = (
            enemydata["attack"]
            * status["buff"]["multipliers"]["enemy"]["attack"]
            * status["debuff"]["multipliers"]["enemy"]["attack"]
        )

        defence_multiplier = (
            10000
            / (
                (playerdata["stats"]["defence"] + playerdata["weapon"]["stats"]["defence"])
                *status["buff"]["multipliers"]["player"]["defence"]
                *status["debuff"]["multipliers"]["player"]["defence"]
                *playerdata["weapon"]["multipliers"]["defence"]
                + 10000
            )
        )

        return(base_dmg * attack_multiplier *defence_multiplier)

    else:
        print("Some error occured")
        return

def turn(next_turn, progress, status):
    if next_turn == "player":
        opponent = "enemy"

        print("Moves available : ", playerdata['moves'].keys()) # Could print htis better 
        move_select = str(input("Enter name of move selected : "))

        #Correct move entered
        while move_select not in playerdata['moves']:
            print("Move selected not in move list, reselect")
            move_select = str(input("Enter name of move selected : "))
                    
        move = playerdata['moves'][move_select]

        dmg, did_crit = damage_calculation(next_turn, move, status)

    elif next_turn == "enemy":
        opponent = "player"

        echoice = random.choice(list(enemydata["moves"].keys()))
        move = enemydata["moves"][echoice]

        dmg = damage_calculation(next_turn, move, status)

    else:
        print("Some error occured")
        return

    buff_duration(move, next_turn, status)
    debuff_duration(move, opponent, status)
    
    if next_turn == "player":
        print("You moved!")
        if did_crit:
            print("Crit Hit!")
        print("Damage dealt : ", dmg)
        progress["enemy"]["ehealth"] -= dmg

        av_spent = (10000
              /((playerdata["stats"]["speed"] + playerdata["weapon"]["stats"]["speed"])
                *status["buff"]["multipliers"]["player"]["speed"]
                *status["debuff"]["multipliers"]["player"]["speed"]
                *playerdata["weapon"]["multipliers"]["speed"]
                )
              )
        
        progress["player"]["pdist"] = 10000

        progress["enemy"]["edist"] -= (enemydata["speed"]
                                       *status["buff"]["multipliers"]["enemy"]["speed"]
                                       *status["debuff"]["multipliers"]["enemy"]["speed"]                              
                                      )*av_spent

    elif next_turn == "enemy":
        print("Enemy moved!")
        print("Damge dealt : ", dmg)

        progress["player"]["phealth"] -= dmg
        av_spent = (10000
                    /(
                        enemydata["speed"]
                        *status["buff"]["multipliers"]["enemy"]["speed"] 
                        *status["debuff"]["multipliers"]["enemy"]["speed"]) 
                    )

        progress["enemy"]["edist"] = 10000

        progress["player"]["pdist"] -= ((playerdata["stats"]["speed"] + playerdata["weapon"]["stats"]["speed"])
                                        *status["buff"]["multipliers"]["player"]["speed"]
                                        *status["debuff"]["multipliers"]["player"]["speed"]
                                        *playerdata["weapon"]["multipliers"]["speed"]
                                         )*av_spent
   
def fight():
    load_data()

    progress = {
        "player" : {
            "pdist" : 10000,
            "phealth" : (playerdata["stats"]["health"] + playerdata["weapon"]["stats"]["health"])*playerdata["weapon"]["multipliers"]["health"]
        },
        "enemy" : {
            "edist" : 10000,
            "ehealth" : enemydata["health"]
        }
    }

    status = {
        #For actual game calcs
        "buff" : {
            "multipliers" : {
                "player" : {
                    "attack" : 1,
                    "speed" : 1,
                    "defence" : 1
                },

                "enemy" : {
                    "attack" : 1,
                    "speed" : 1,
                    "defence" : 1
                }
            },
            #format = buff name, multiplier, duration in list
            "player" : {
                "attack" : {},
                "speed" : {},
                "defence" : {},
            },
            "enemy" : {
                "attack" : {},
                "speed" : {},
                "defence" : {},
            }
        },

        "debuff" : {
            "multipliers" : {
                "player" : {
                    "attack" : 1,
                    "speed" : 1,
                    "defence" : 1
                },

                "enemy" : {
                    "attack" : 1,
                    "speed" : 1,
                    "defence" : 1
                }
            },
            #format = buff name, multiplier, duration in list
            "player" : {
                "attack" : {},
                "speed" : {},
                "defence" : {},
            },
            "enemy" : {
                "attack" : {},
                "speed" : {},
                "defence" : {},
            }      
        } 
    }

    while True:
        buff_calculations("player", status)
        buff_calculations("enemy", status)
        debuff_calculations("player", status)
        debuff_calculations("enemy", status)

        next_turn = speed_sys(progress,status)

        turn(next_turn, progress, status)
        

        if progress["player"]["phealth"] <= 0 :
            print("You died")
            break
        elif progress["enemy"]["ehealth"] <= 0 :
            print("You won")
            break
        else:
            print("Your health : ", progress["player"]["phealth"])
            print("Enemy health : ", progress["enemy"]["ehealth"]) 
        print()

fight() 
