import random

playeradata = {
    "speed" : 135,
    "health" : 6700,
    "attack" : 350,
    #Selfbuff and debuff are multiplicative so if no selfbuff / debuff then put
    #Self buff = final attack (prob too op), debuff = enemy def
    #Dot is amnt of dmg per enemy turn so put 0 if no dot

    #Buffs stored as name ; [multiplier, expiry, what it effects]
    "moves" : {
        "move1" : {
        "damage" : 100,
        "selfbuff" : {
            "rage" : [1.25, 3, "attack"]
            },
        "debuff" : 0.9,
        "dot" : 0
        },

        "move2" : {
        "damage" : 50,
        "selfbuff" : {
            "haste" : [1.3, 2, "speed"]
        },
            "debuff" : 1,
        "dot" : 0
        },

        "move3" : {
        "damage" : 75,
        "selfbuff" : {
            "battle_focus" : [1.15, 5, "attack"],
            "quickstep" : [1.2, 1, "speed"]
            },
        "debuff" : 0.8,
        "dot" : 0
        },

        "move4" : {
        "damage" : 250,
        "selfbuff" : {
            "berserk" : [1.5, 1 , "attack"]
            },
        "debuff" : 1,
        "dot" : 0
        }
    }
}

enemydata = {
    "speed": 100,
    "health": 10000,
    "defence": 1000,

    "moves": {
        "crushing_blow": {
            "damage": 180,
            "selfbuff": {},
            "debuff": 1
        },

        "war_cry": {
            "damage": 50,
            "selfbuff": {
                "fury": [1.3, 3, "attack"]
            },
            "debuff": 1
        },

        "crippling_hex": {
            "damage": 40,
            "selfbuff": {},
            "debuff": 0.8
        },

        "frenzy": {
            "damage": 120,
            "selfbuff": {
                "frenzy": [1.2, 2, "speed"],
                "bloodlust": [1.15, 2, "attack"]
            },
            "debuff": 1
        },

        "battle_shout": {
            "damage": 70,
            "selfbuff": {
                "battle_hardened": [1.2, 4, "defence"]
            },
            "debuff": 1
        }
    }
}

def speed_sys(progress):
    pav = progress["player"]["pdist"] / playeradata["speed"]
    eav = progress["enemy"]["edist"] / enemydata["speed"]

    if pav<eav:
        next_turn = "p"
    elif eav<pav:
        next_turn = "e"
    else:
        next_turn = random.choice(["p", "e"])

    return next_turn, pav, eav
    

def pturn(progress, status):
    print("Moves available : ", playeradata['moves']) # Could print htis better 
    move_select = str(input("Enter name of move selected : "))

    #Correct move entered
    while move_select not in playeradata['moves']:
        print("Move selected not in move list, reselect")
        move_select = str(input("Enter name of move selected : "))
                
    pmove = playeradata['moves'][move_select]

    pdmg_base = pmove["damage"]
    #Haev to add including buffs
    pdmg = pdmg_base* (playeradata["attack"])/((playeradata["attack"]) + enemydata["defence"])

    #Adding selfbuffs
    for i in pmove["selfbuff"]:
        buff_data = pmove["selfbuff"][i]
        buff_name = i

        multiplier = buff_data[0]
        duration = buff_data[1]

        if buff_data[-1] == "attack":
            status["player"]["attack"][buff_name] = [multiplier, duration]  
        elif buff_data[-1] == "speed":
            status["player"]["speed"][buff_name] = [multiplier, duration] 
        elif buff_data[-1] == "defence" :
            status["player"]["defence"][buff_name] = [multiplier, duration] 
        
    #Code status decreasing here
    expired = []
    for buff_type in status["player"]:
        for buff_name in status["player"][buff_type]:
            buff_data = status["player"][buff_type][buff_name]
            if buff_data[-1]>0:
                buff_data[-1] -= 1
            else:
                expired.append([buff_type, buff_name])

    #Delete seperately cus deleting together was annyoing
    for to_delete in expired:
        del status["player"][to_delete[0]][to_delete[1]]

    progress["enemy"]["ehealth"] -= pdmg
    av = 10000/playeradata["speed"] #Temp fix, diff function later where buffs will also be calced
    progress["player"]["pdist"] = 10000
    progress["enemy"]["edist"] = 10000 - enemydata["speed"]*av

def eturn(progress, status):
    echoice = random.choice(list(enemydata["moves"].keys()))
    emove = enemydata["moves"][echoice]

    edmg_base = emove["damage"]
    edmg = edmg_base #Prob improve this 

    for i in emove["selfbuff"]:
        buff_data = emove["selfbuff"][i]
        buff_name = i

        multiplier = buff_data[0]
        duration = buff_data[1]

        if buff_data[-1] == "attack":
            status["enemy"]["attack"][buff_name] = [multiplier, duration]  
        elif buff_data[-1] == "speed":
            status["enemy"]["speed"][buff_name] = [multiplier, duration] 
        elif buff_data[-1] == "defence" :
            status["enemy"]["defence"][buff_name] = [multiplier, duration]     

    #Status decreasing
    expired = []
    for buff_type in status["enemy"]:
        for buff_name in status["enemy"][buff_type]:
            buff_data = status["enemy"][buff_type][buff_name]
            if buff_data[-1]>0:
                buff_data[-1] -= 1
            else:
                expired.append([buff_type, buff_name])

    #Delete seperately cus deleting together was annyoing
    for to_delete in expired:
        del status["enemy"][to_delete[0]][to_delete[1]]

    progress["player"]["phealth"] -= edmg
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

    while True:
        next_turn = speed_sys(progress)

        if next_turn == "p":
            pturn(progress, status)
        elif next_turn == "e":
            eturn(progress, status)
        else:
            print("Some error occured")

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
