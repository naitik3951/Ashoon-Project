import random

stats = {
    'player_hp' : 10000,
    'player_defence' : 50,
    'player_attack' : 20,
    'player_spd' : 1
}
enemy = {
    'name' : 'test enemy 1',
    'enemy_hp' : 10000,
    'enemy_defence' : 50,
    'enemy_attack' : 20,
    'enemy_spd' : 2.1
}

weapon = {
    'name' : 'scythe',
    'weapon_attack_min' : 50,
    'weapon_attack_max' : 100,
    'crit_rate' : 50,
    'crit_damage' : 100,
}


def fight():
    #Defining few stuff for battle(later load from file directly i think)
    player_distance = 10
    enemy_distance = 10
    player_health = stats['player_hp']
    enemy_health = enemy['enemy_hp']


    fighting = True
    while fighting:
        player_damage = (stats['player_attack'] + random.randint(weapon['weapon_attack_min'], weapon['weapon_attack_max']))*2 - (enemy['enemy_defence']) #Change to Lx/x+d form later ig
        if player_damage<0: #Temporary
            player_damage = 0

        enemy_damage = (enemy['enemy_attack'])*2 - stats['player_defence']
        if enemy_damage<0: #Temporary
            enemy_damage = 0

        player_av = player_distance/stats['player_spd']
        enemy_av = enemy_distance/enemy['enemy_spd']

        if player_av < enemy_av : #Player moves
            #Crit attmept 
            roll = random.random()*100
            if roll <= weapon['crit_rate']:
                player_damage = player_damage * (weapon['crit_damage']/100) #Might change later
                print("Crit hit")

            enemy_health = enemy_health - player_damage
            print('Player did attack')
            print("Player damage : ", player_damage)
            print()
            player_distance = 10
            enemy_distance = enemy_distance - player_av * enemy['enemy_spd'] #Player av cus av = time bassicly and time elapsed is calculated for player only at htis moment

        elif enemy_av < player_av : #Enemy moves
            player_health = player_health - enemy_damage
            print('Enemy did attack')       
            print('Enemy damage : ', enemy_damage)
            print()
            enemy_distance = 10
            player_distance = player_distance - enemy_av * stats['player_spd'] #Same as above

        elif enemy_av == player_av : #Both act
            enemy_health = enemy_health - player_damage
            player_av = 10
            print('Player did attack')
            print('Player damage : ', player_damage)
            print()
            player_health = player_health - enemy_damage
            enemy_av = 10
            print('Enemy did attack')    
            print('Enemy damage', enemy_damage)
            print()
            player_distance = 10
            enemy_distance = 10

        #Alive or dead check
        if player_health <= 0:
            print('Player died')
            fighting = False
        elif enemy_health <=0:
            print('Enemy died')
            fighting = False


fight()
