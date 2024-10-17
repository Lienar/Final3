from .models import *
from random import randint

players_skill_default_cooldown = [0, 0, 99, 99, 99, 99]
enemy_skill_default_cooldown = [0, 0]
turn = 0

def Battel_start(player_name, enemy_name):
    turn = 0
    player = Player.objects.get(name=player_name)
    enemy = Enemy.objects.get(name=enemy_name)
    battel = Battel_stat.objects.get(id=1)
    Player_cooldowns_setup(player)
    Enemy_cooldowns_setup(enemy)
    battel = Battel_stat.objects.get(id=1)
    Battel_stat.objects.filter(id=1).update(Player_item1_default_cooldown = battel.Player_item1_cooldown)
    Battel_stat.objects.filter(id=1).update(Player_item2_default_cooldown = battel.Player_item1_cooldown)
    Battel_stat.objects.filter(id=1).update(Player_item3_default_cooldown = battel.Player_item1_cooldown)
    Battel_stat.objects.filter(id=1).update(Player_item4_default_cooldown = battel.Player_item1_cooldown)
    Battel_stat.objects.filter(id=1).update(Player_item5_default_cooldown = battel.Player_item1_cooldown)
    Battel_stat.objects.filter(id=1).update(Player_item6_default_cooldown = battel.Player_item1_cooldown)
    enemy_skill_default_cooldown[0] = battel.Enemy_skill1_cooldown
    enemy_skill_default_cooldown[1] = battel.Enemy_skill2_cooldown

def Player_turn(player_used_item, player_inventory_slot):
    item = Item_list.objects.get(item_name=player_used_item)
    battel_stats = Battel_stat.objects.get(id=1)
    if item.item_type == 'Weapon':
        Player_strike(item, player_inventory_slot, battel_stats)
    if item.item_type == 'Heal':
        Player_heal(item, player_inventory_slot, battel_stats)


def Player_strike(item, player_inventory_slot, battel_stats):
    damage = randint(item.skill_effect_min, item.skill_effect_max)
    players_skill_default_cooldown = Restart_defualt_cooldown()
    if players_skill_default_cooldown[player_inventory_slot] > 0:
        damage = 0
        player_inventory_slot = 10
    current_enemy_health = battel_stats.Enemy_current_health - damage
    Battel_stat.objects.filter(id=1).update(Enemy_current_health=current_enemy_health)
    for i in range(0, 6):
        if i != player_inventory_slot:
            if players_skill_default_cooldown[i] != 0:
                players_skill_default_cooldown[i] -= 1
            if players_skill_default_cooldown[i] <= 0:
                players_skill_default_cooldown[i] = 0
        elif i == player_inventory_slot:
            players_skill_default_cooldown[i] = item.skill_cooldown
    Cooldowns_setup_progress(players_skill_default_cooldown)


def Restart_defualt_cooldown():
    cooldowns = [0, 0, 0, 0, 0, 0]
    battel = Battel_stat.objects.get(id=1)
    cooldowns[0] = battel.Player_item1_default_cooldown
    cooldowns[1] = battel.Player_item2_default_cooldown
    cooldowns[2] = battel.Player_item3_default_cooldown
    cooldowns[3] = battel.Player_item4_default_cooldown
    cooldowns[4] = battel.Player_item5_default_cooldown
    cooldowns[5] = battel.Player_item6_default_cooldown
    return cooldowns

def Cooldowns_setup_progress(cooldowns):
    Battel_stat.objects.filter(id=1).update(Player_item1_cooldown=cooldowns[0],
                                            Player_item2_cooldown=cooldowns[1],
                                            Player_item3_cooldown=cooldowns[2],
                                            Player_item4_cooldown=cooldowns[3],
                                            Player_item5_cooldown=cooldowns[4],
                                            Player_item6_cooldown=cooldowns[5])


def Player_heal(item, player_inventory_slot, battel_stats):
    heal = randint(item.skill_effect_min, item.skill_effect_max)
    players_skill_default_cooldown = Restart_defualt_cooldown()
    if players_skill_default_cooldown[player_inventory_slot] > 0:
        heal = 1
        player_inventory_slot = 10
    current_player_health = battel_stats.Player_current_health + heal
    if current_player_health <= battel_stats.Player_default_health:
        Battel_stat.objects.filter(id=1).update(Player_current_health=current_player_health)
    if current_player_health > battel_stats.Player_default_health:
        Battel_stat.objects.filter(id=1).update(Player_current_health=battel_stats.Player_default_health)
    for i in range(0, 6):
        if i != player_inventory_slot:
            if players_skill_default_cooldown[i] != 0:
                players_skill_default_cooldown[i] -= 1
            if players_skill_default_cooldown[i] <= 0:
                players_skill_default_cooldown[i] = 0
        elif i == player_inventory_slot:
            players_skill_default_cooldown[i] = item.skill_cooldown
    Cooldowns_setup_progress(players_skill_default_cooldown)


def Enemy_turn(enemy):
    battel_stats = Battel_stat.objects.get(id=1)
    enemy_have_heal1 = False
    enemy_have_heal2 = False
    heal_skill = 0
    skill1 = Enemy_skill.objects.get(skill_id=enemy.enemy_skill1_id)
    skill2 = Enemy_skill.objects.get(skill_id=enemy.enemy_skill2_id)
    strike = 1
    if skill1.skill_type == 'Heal':
        enemy_have_heal1 = True
    if skill2.skill_type == 'Heal':
        enemy_have_heal2 = True
    if randint(0,100) < 51 and battel_stats.Enemy_skill1_cooldown <= 0 and battel_stats.Enemy_skill2_cooldown <= 0:
        strike = 1
    elif battel_stats.Enemy_skill1_cooldown <= 0 and battel_stats.Enemy_skill2_cooldown <= 0:
        strike = 2
    if battel_stats.Enemy_current_health <= (battel_stats.Enemy_default_health)/2:
        if skill1.skill_type == 'Heal' and battel_stats.Enemy_skill1_cooldown <= 0 and randint(0,100) < 90:
            strike = 1
        if skill2.skill_type == 'Heal' and battel_stats.Enemy_skill2_cooldown <= 0 and randint(0,100) < 90:
            strike = 2
        if battel_stats.Enemy_skill1_cooldown > 0:
            strike = 2
        if battel_stats.Enemy_skill2_cooldown > 0:
            strike = 1
        if randint(0,100) < 51:
            strike = 1
    if  battel_stats.Enemy_skill1_cooldown <= 0 and battel_stats.Enemy_skill2_cooldown > 0:
        strike = 1
    if  battel_stats.Enemy_skill1_cooldown > 0 and battel_stats.Enemy_skill2_cooldown <= 0:
        strike = 2
    if strike == 1:
        if skill1.skill_type == 'Attack':
            skill = Enemy_skill.objects.get(skill_name=skill1.skill_name)
            Enemy_strike(skill, battel_stats, strike)
        if skill1.skill_type == 'Heal':
            skill = Enemy_skill.objects.get(skill_name=skill1.skill_name)
            Enemy_heal(skill, battel_stats, strike)
    if strike == 2:
        if skill2.skill_type == 'Attack':
            skill = Enemy_skill.objects.get(skill_name=skill2.skill_name)
            Enemy_strike(skill, battel_stats, strike)
        if skill2.skill_type == 'Heal':
            skill = Enemy_skill.objects.get(skill_name=skill2.skill_name)
            Enemy_heal(skill, battel_stats, strike)


def Enemy_strike(skill, battel_stats, strike):
    damage = randint(skill.skill_effect_min, skill.skill_effect_max)
    current_player_health = battel_stats.Player_current_health-damage
    if strike == 1:
        Battel_stat.objects.filter(id=1).update(Enemy_skill1_cooldown=skill.skill_cooldown)
        if battel_stats.Enemy_skill2_cooldown - 1 > 0:
            cooldown = Battel_stat.objects.get(id=1).Enemy_skill2_cooldown - 1
            Battel_stat.objects.filter(id=1).update(Enemy_skill2_cooldown=cooldown)
        else:
            Battel_stat.objects.filter(id=1).update(Enemy_skill2_cooldown=0)
    if strike == 2:
        Battel_stat.objects.filter(id=1).update(Enemy_skill2_cooldown=skill.skill_cooldown)
        if battel_stats.Enemy_skill1_cooldown - 1 > 0:
            cooldown = Battel_stat.objects.get(id=1).Enemy_skill1_cooldown - 1
            Battel_stat.objects.filter(id=1).update(Enemy_skill1_cooldown=cooldown)
        else:
            Battel_stat.objects.filter(id=1).update(Enemy_skill1_cooldown=0)
    Battel_stat.objects.filter(id=1).update(Enemy_battel_text=skill.skill_description)
    Battel_stat.objects.filter(id=1).update(Player_current_health=current_player_health)


def Enemy_heal(skill, battel_stats, strike):
    heal = randint(skill.skill_effect_min, skill.skill_effect_max+1)
    Battel_stat.objects.filter(id=1).update(Enemy_battel_text=skill.skill_description)
    current_enemy_health = battel_stats.Enemy_current_health + heal
    if current_enemy_health <= battel_stats.Enemy_default_health:
        Battel_stat.objects.filter(id=1).update(Enemy_current_health=current_enemy_health)
    if current_enemy_health > battel_stats.Enemy_default_health:
        Battel_stat.objects.filter(id=1).update(Enemy_current_health=battel_stats.Enemy_default_health)
    if strike == 1:
        Battel_stat.objects.filter(id=1).update(Enemy_skill1_cooldown=skill.skill_cooldown)
        if battel_stats.Enemy_skill2_cooldown - 1 > 0:
            cooldown = Battel_stat.objects.get(id=1).Enemy_skill2_cooldown - 1
            Battel_stat.objects.filter(id=1).update(Enemy_skill2_cooldown=cooldown)
        else:
            Battel_stat.objects.filter(id=1).update(Enemy_skill2_cooldown=0)
    if strike == 2:
        Battel_stat.objects.filter(id=1).update(Enemy_skill2_cooldown=skill.skill_cooldown)
        if battel_stats.Enemy_skill1_cooldown - 1 > 0:
            Battel_stat.objects.filter(id=1).update(Enemy_skill1_cooldown=skill.skill_cooldown)
        else:
            Battel_stat.objects.filter(id=1).update(Enemy_skill1_cooldown=0)
    Battel_stat.objects.filter(id=1).update(Enemy_battel_text=skill.skill_description)




def Player_cooldowns_setup(player):
    inventory = Player_inventory.objects.get(inventory_id=player.player_inventory)
    item1_id = Item_list.objects.get(item_id=inventory.item1)
    item2_id = Item_list.objects.get(item_id=inventory.item2)
    item3_id = Item_list.objects.get(item_id=inventory.item3)
    item4_id = Item_list.objects.get(item_id=inventory.item4)
    item5_id = Item_list.objects.get(item_id=inventory.item5)
    item6_id = Item_list.objects.get(item_id=inventory.item6)
    inventory_slot = [True, True, True, True, True, True]
    for i in range(1, 6):
        locals()['item' + str(i)] = Player_item_setup(locals()['item' + str(i)+ '_id'])
        if locals()['item' + str(i)] != 0:
            inventory_slot[i] = False
            players_skill_default_cooldown[i] = 0
        else:
            inventory_slot[i] = True
            players_skill_default_cooldown[i] = 99
    player_class = Player_class.objects.get(class_id=player.player_class)
    Battel_stat.objects.filter(id=1).update(Player_default_health=player_class.class_heals,
                                            Player_current_health=player.player_health,
                                            Player_item1_cooldown=players_skill_default_cooldown[0],
                                            Is_slot1_empty=inventory_slot[0],
                                            Player_item2_cooldown=players_skill_default_cooldown[1],
                                            Is_slot2_empty=inventory_slot[1],
                                            Player_item3_cooldown=players_skill_default_cooldown[2],
                                            Is_slot3_empty=inventory_slot[2],
                                            Player_item4_cooldown=players_skill_default_cooldown[3],
                                            Is_slot4_empty=inventory_slot[3],
                                            Player_item5_cooldown=players_skill_default_cooldown[4],
                                            Is_slot5_empty=inventory_slot[4],
                                            Player_item6_cooldown=players_skill_default_cooldown[5],
                                            Is_slot6_empty=inventory_slot[5])


def Player_item_setup(item_id):
    if item_id.item_type == 'Weapon':
        return Item_list.objects.get(item_name=item_id.item_name)
    if item_id.item_type == 'Heal':
        return Item_list.objects.get(item_name=item_id.item_name)
    return 0

def Enemy_cooldowns_setup(enemy):
    skill1_id = Enemy_skill.objects.get(skill_id=enemy.enemy_skill1_id)
    skill2_id = Enemy_skill.objects.get(skill_id=enemy.enemy_skill2_id)
    skill1 = Enemy_skill.objects.get(skill_name=skill1_id.skill_name)
    skill2 = Enemy_skill.objects.get(skill_name=skill2_id.skill_name)
    enemy_skill_default_cooldown[0] = 0
    enemy_skill_default_cooldown[1] = 0
    Battel_stat.objects.filter(id=1).update(Enemy_default_health=enemy.health,
                                            Enemy_current_health=enemy.health,
                                            Enemy_battel_text=' ',
                                            Enemy_skill1_cooldown=enemy_skill_default_cooldown[0],
                                            Enemy_skill2_cooldown=enemy_skill_default_cooldown[1])
