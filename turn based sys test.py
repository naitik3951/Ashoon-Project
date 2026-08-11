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
    "speed" : 100,
    "health" : 10000,
    "defence" : 1000,
    "moves" : {
        "move1" : 100,
        "move2" : 50,
        "move3" : 75
    }
}

def pturn(progress, status):
    print("Moves available : ", playeradata['moves']) # Could print htis better 
    move_select = str(input("Enter name of move selected : "))

    #Correct move entered
    while move_select not in playeradata['moves']:
        print("Move selected not in move list, reselect")
        move_select = str(input("Enter name of move selected : "))
                
    pmove = playeradata['moves'][move_select]

    pdmgbase = playeradata[move_select]["damage"]
    pdmg = pdmgbase* (playeradata["attack"]*status["player"]["attack"])/((playeradata["attack"]*status["player"]["attack"]) + enemydata["defence"]*status["enemy"]["defence"])

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
    

def fight():
    pdist = 10000
    pbuffs = 1 #For final dmg
    pdebuff = 0 #Not defining enemy rn

    edist = 10000
    ebuffs = 1 #Not defining rn
    edebuff = 1
    edot = 0

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

    phealth = playeradata['health']
    ehealth = enemydata['health']


    while True:
        pav = pdist / playeradata['speed']
        eav = edist / enemydata['speed']



        if pav < eav:
            print("Moves available : ", playeradata['moves']) # Could print htis better 
            move_select = str(input("Enter name of move selected : "))

            #Correct move entered
            while move_select not in playeradata['moves']:
                print("Move selected not in move list, reselect")
                move_select = str(input("Enter name of move selected : "))
                    

            pmove = playeradata['moves'][move_select]

            #Player appling buffs, debuffs, selfbuffs, dot
            pdmg_base = pmove["damage"]
            pdmg = (playeradata["attack"]*pbuffs) * pdmg_base /((playeradata["attack"]*pbuffs) + enemydata["defence"]*edebuff) #Improve this later

            pbuffs *= pmove["selfbuff"] # For pattack

            edebuff *= pmove["debuff"] # For edefence

            edot +=pmove["dot"] # Have to add dot countdown

            ehealth = ehealth - pdmg - edot
            pdist = 10000
            edist = edist - eav * enemydata['speed']

        elif eav < pav:
            print("Enemy moved!")
            choices = list(enemydata['moves'])
            move_select = random.choice(choices)
            emove = enemydata['moves'][move_select]

            phealth = phealth - emove
            edist = 10000
            pdist = pdist - pav * playeradata['speed']

  

        if phealth < 0 :
            print("You died")
            break
        elif ehealth < 0 :
            print("You won")
            break
        else:
            print("Your health : ", phealth)
            print("Enemy health : ", ehealth) 
        print()

fight() 