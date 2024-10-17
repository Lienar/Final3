from .models import *


inventory = {'skill1': ['None', 99, 5, 3, 1], 'skill2': ['None', 99, 5, 3, 2], 'skill3': ['None', 99, 5, 3, 3],
             'skill4': ['None', 99, 5, 3, 4], 'skill5': ['None', 99, 5, 3, 5], 'skill6': ['None', 99, 5, 3, 6]}


def make_inventory(player, battel, turn):
    inventory_temp = Player_inventory.objects.get(inventory_id = player.player_inventory)
    item1 = Item_list.objects.get(item_id=inventory_temp.item1)
    item2 = Item_list.objects.get(item_id=inventory_temp.item2)
    item3 = Item_list.objects.get(item_id=inventory_temp.item3)
    item4 = Item_list.objects.get(item_id=inventory_temp.item4)
    item5 = Item_list.objects.get(item_id=inventory_temp.item5)
    item6 = Item_list.objects.get(item_id=inventory_temp.item6)
    items = [item1, item2, item3, item4, item5, item6]
    inventory = [{'item_name': items[0].item_name, 'item_cooldown': items[0].skill_cooldown,
                  'damage_min': items[0].skill_effect_min, 'damage_max': items[0].skill_effect_max,
                  'item_description': items[0].description, 'slot': 0},
                 {'item_name': items[1].item_name, 'item_cooldown': items[1].skill_cooldown,
                  'damage_min': items[1].skill_effect_min, 'damage_max': items[1].skill_effect_max,
                  'item_description': items[1].description, 'slot': 1},
                 {'item_name': items[2].item_name, 'item_cooldown': items[2].skill_cooldown,
                  'damage_min': items[2].skill_effect_min, 'damage_max': items[2].skill_effect_max,
                  'item_description': items[2].description, 'slot': 2},
                 {'item_name': items[3].item_name, 'item_cooldown': items[3].skill_cooldown,
                  'damage_min': items[3].skill_effect_min, 'damage_max': items[3].skill_effect_max,
                  'item_description': items[3].description, 'slot': 3},
                 {'item_name': items[4].item_name, 'item_cooldown': items[4].skill_cooldown,
                  'damage_min': items[4].skill_effect_min, 'damage_max': items[4].skill_effect_max,
                  'item_description': items[4].description, 'slot': 4},
                 {'item_name': items[5].item_name, 'item_cooldown': items[5].skill_cooldown,
                  'damage_min': items[5].skill_effect_min, 'damage_max': items[5].skill_effect_max,
                  'item_description': items[5].description, 'slot': 5}]
    if turn == 0:
        for item in inventory:
            if item['item_name'] != 'Empty':
                item['item_cooldown'] = 0
            else:
                item['item_cooldown'] = 99
    else:
        inventory = [{'item_name': items[0].item_name, 'item_cooldown': battel.Player_item1_cooldown,
                      'damage_min': items[0].skill_effect_min, 'damage_max': items[0].skill_effect_max,
                      'item_description': items[0].description, 'slot': 0},
                     {'item_name': items[1].item_name, 'item_cooldown': battel.Player_item2_cooldown,
                      'damage_min': items[1].skill_effect_min, 'damage_max': items[1].skill_effect_max,
                      'item_description': items[1].description, 'slot': 1},
                     {'item_name': items[2].item_name, 'item_cooldown': battel.Player_item3_cooldown,
                      'damage_min': items[2].skill_effect_min, 'damage_max': items[2].skill_effect_max,
                      'item_description': items[2].description, 'slot': 2},
                     {'item_name': items[3].item_name, 'item_cooldown': battel.Player_item4_cooldown,
                      'damage_min': items[3].skill_effect_min, 'damage_max': items[3].skill_effect_max,
                      'item_description': items[3].description, 'slot': 3},
                     {'item_name': items[4].item_name, 'item_cooldown': battel.Player_item5_cooldown,
                      'damage_min': items[4].skill_effect_min, 'damage_max': items[4].skill_effect_max,
                      'item_description': items[4].description, 'slot': 4},
                     {'item_name': items[5].item_name, 'item_cooldown': battel.Player_item6_cooldown,
                      'damage_min': items[5].skill_effect_min, 'damage_max': items[5].skill_effect_max,
                      'item_description': items[5].description, 'slot': 5}]
    return inventory
