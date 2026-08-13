import random

stats = {
    'player_hp' : 100,
    'player_defence' : 50,
    'player_attack' : 20,
    'player_spd' : 1
}
enemy = {
    'name' : 'test enemy 1',
    'enemy_hp' : 100,
    'enemy_defence' : 50,
    'enemy_attack' : 20,
    'enemy_spd' : 2
}

weapon = {
    'name' : 'scythe',
    'weapon_attack' : 100,
    'crit_rate' : 50,
    'crit_dammage' : 100,
}

def fight():
    #Taking player stats and dammage formula
    net_attack = stats['player_attack'] + weapon['weapon_attack']
    player_spd = stats['player_spd']
    enemy_spd = enemy['enemy_spd']
    player_health = stats['player_hp']
    enemy_health = enemy['enemy_hp']

    player_dammage = 1
    enemy_dammage = 1

    #Fighting
    fighting = True
    player_distance = 10
    enemy_distance = 10
    while fighting:
        player_distance = player_distance- player_spd
        enemy_distance = enemy_distance - enemy_spd

        if player_distance <= 0:
            enemy_health = enemy_health - player_dammage
            player_distance = 10
            print(player_health)
            print(enemy_health)
            print()
        
        if enemy_distance <= 0:
            player_health = player_health - enemy_dammage 
            enemy_distance = 10
            print(player_health)
            print(enemy_health)
            print()

        if player_health <= 0:
            print("Player died lmao")
            fighting = False
        elif enemy_health <= 0:
            print("You won sad")
            fighting = False

    

fight()
