import random

playeradata = {
    "speed" : 135,
    "health" : 6700,
    "attack" : 350,
    #Moves = [base dmg, self buff, debuff, dot]
    #Selfbuff and debuff are multiplicative so if no selfbuff / debuff then put
    #Self buff = final attack (prob too op), debuff = enemy def
    #Dot is amnt of dmg per enemy turn so put 0 if no dot
    "moves" : {
        "move1" : {
            "damage" : 100,
            "selfbuff" : 1,
            "debuff" : 0.8,
            "dot" : 0
        },
        "move2" : {
            "damage" : 50,
            "selfbuff" : 1.5,
            "debuff" : 1,
            "dot" : 0
        },
        "move3" : {
            "damage" : 20,
            "selfbuff" : 1,
            "debuff" : 1,
            "dot" : 75
        },
        "move4" : {
            "damage" : 250,
            "selfbuff" : 1,
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

def fight():
    pdist = 10000
    pbuffs = 1 #For final dmg
    pdebuff = 0 #Not defining enemy rn

    edist = 10000
    ebuffs = 1 #Not defining rn
    edebuff = 1
    edot = 0

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