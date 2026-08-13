import random

playeradata = {
    "speed": 135,
    "health": 6700,
    "attack": 350,
    "defence": 1000,

    "moves": {
        "move1": {
            "damage": 100,
            "selfbuff": {
                "rage": [1.25, 3, "attack"]
            },
            "debuff": {
                "weaken": [0.8, 3, "attack"]
            },
            "dot": 0
        },

        "move2": {
            "damage": 50,
            "selfbuff": {
                "haste": [1.3, 2, "speed"]
            },
            "debuff": {
                "slow": [0.7, 2, "speed"]
            },
            "dot": 0
        },

        "move3": {
            "damage": 75,
            "selfbuff": {
                "battle_focus": [1.15, 5, "attack"],
                "quickstep": [1.2, 1, "speed"]
            },
            "debuff": {
                "expose": [0.75, 2, "defence"]
            },
            "dot": 0
        },

        "move4": {
            "damage": 250,
            "selfbuff": {
                "berserk": [1.5, 1, "attack"]
            },
            "debuff": {
                "weaken": [0.6, 1, "attack"],
                "expose": [0.8, 1, "defence"]
            },
            "dot": 0
        }
    }
}


enemydata = {
    "speed": 100,
    "health": 10000,
    "attack": 1000,
    "defence": 1000,

    "moves": {
        "crushing_blow": {
            "damage": 180,
            "selfbuff": {},
            "debuff": {
                "weaken": [0.8, 2, "attack"]
            },
            "dot": 0
        },

        "war_cry": {
            "damage": 50,
            "selfbuff": {
                "fury": [1.3, 3, "attack"]
            },
            "debuff": {
                "slow": [0.75, 2, "speed"]
            },
            "dot": 0
        },

        "crippling_hex": {
            "damage": 40,
            "selfbuff": {},
            "debuff": {
                "expose": [0.8, 3, "defence"]
            },
            "dot": 0
        },

        "frenzy": {
            "damage": 120,
            "selfbuff": {
                "frenzy": [1.2, 2, "speed"],
                "bloodlust": [1.15, 2, "attack"]
            },
            "debuff": {
                "expose": [0.85, 2, "defence"]
            },
            "dot": 0
        },

        "battle_shout": {
            "damage": 70,
            "selfbuff": {
                "battle_hardened": [1.2, 4, "defence"]
            },
            "debuff": {
                "weaken": [0.7, 2, "attack"]
            },
            "dot": 0
        }
    }
}

def speed_sys(progress, status):
    pav = progress["player"]["pdist"] / (playeradata["speed"]*status["buff"]["multipliers"]["player"]["speed"])
    eav = progress["enemy"]["edist"] / (enemydata["speed"]*status["buff"]["multipliers"]["enemy"]["speed"])

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
        return( move["damage"] * ((playeradata["attack"]) * (status["multipliers"][next_turn]["attack"])) / (((playeradata["attack"]) * (status["multipliers"][next_turn]["attack"])) + (enemydata["defence"]*status["multipliers"]["enemy"]["defence"])) )

    elif next_turn == "enemy":
        return( move["damage"] * ((enemydata["attack"]) * (status["multipliers"][next_turn]["attack"])) / (((enemydata["attack"]) * (status["multipliers"][next_turn]["attack"])) + (playeradata["defence"]*status["multipliers"]["player"]["defence"])) )  

    else:
        print("Some error occured")
        return


def turn(next_turn, progress, status):
    if next_turn == "player":
        opponent = "enemy"

        print("Moves available : ", playeradata['moves']) # Could print htis better 
        move_select = str(input("Enter name of move selected : "))

        #Correct move entered
        while move_select not in playeradata['moves']:
            print("Move selected not in move list, reselect")
            move_select = str(input("Enter name of move selected : "))
                    
        move = playeradata['moves'][move_select]

        dmg = damage_calculation(next_turn, move, status)

    elif next_turn == "enemy":
        opponent = "player"

        echoice = random.choice(list(enemydata["moves"].keys()))
        move = enemydata["moves"][echoice]

        dmg = damage_calculation(next_turn, move, status)

    else:
        print("Some error occured")
        return

    buff_duration(move, next_turn, status)
    
    if next_turn == "player":
        print("You moved!")
        print()
        progress["enemy"]["ehealth"] -= dmg
        av = 10000/playeradata["speed"] #Temp fix, diff function later where buffs will also be calced
        progress["player"]["pdist"] = 10000
        progress["enemy"]["edist"] = 10000 - enemydata["speed"]*av

    elif next_turn == "enemy":
        print("Enemy moved!")
        print()
        progress["player"]["phealth"] -= dmg
        av = 10000/enemydata["speed"]#Temp fix, diff function lated where buffs also calced
        progress["enemy"]["edist"] = 10000
        progress["player"]["pdist"] -= playeradata["speed"]*av
   
def fight():
    progress = {
        "player" : {
            "pdist" : 10000,
            "phealth" : playeradata["health"]
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

        print(status) #To see if its working

fight() 
