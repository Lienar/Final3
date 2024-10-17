from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import *
from random import randint
from .Battel import *
from .Inventory import *

# Create your views here.
def Enter_page(request):
    Players = Player.objects.all()
    if request.method == 'POST':
        run_len = int(request.POST.get('run_len'))
        if run_len < 7:
            run_len = 7
        if run_len > 20:
            run_len = 20
        Map_len.objects.all().update(map_len=run_len)
        name = request.POST.get('name')
        for player in Players:
            if player.name == name:
                player_class = Player_class.objects.get(class_id=player.player_class)
                default_inventory = Class_inventory.objects.get(inventory_id=player_class.class_inventory)
                Player.objects.filter(name=player.name).update(player_health=player_class.class_heals)
                Player_inventory.objects.filter(inventory_id=player.player_inventory).update(
                    item1=default_inventory.item1, item2=default_inventory.item2, item3=default_inventory.item3,
                    item4=default_inventory.item4, item5=default_inventory.item5, item6=default_inventory.item6,
                    is_have_heal=default_inventory.is_have_heal, is_have_empty_slot=default_inventory.is_have_empty_slot)
                url_temp = f'http://127.0.0.1:8000/Player/?player_name={name}'
                return redirect(url_temp)
        url_temp = f'http://127.0.0.1:8000/create/'
        return redirect(url_temp)
    info = {'Players': [' ', ' ']}
    for player in Players:
        i=0
        if len(info) < i:
            info['Players'].append([player.name, Player_class.objects.get(class_id=player.player_class).class_name])
        else:
            info['Players'][i] = [player.name, Player_class.objects.get(class_id=player.player_class).class_name]
        i += 1
    return render(request, 'Enter.html', info)

def Create_player_page(request):
    Players = Player.objects.all()
    Player_classes=Player_class.objects.all()
    info = {'error': ' ', 'Player_classes': Player_classes}
    print(Player_classes)
    is_player_created = False
    if request.method == 'POST':
        name = request.POST.get('name')
        for player in Players:
            if player.name == name:
                info['error'] = 'Игрок уже существует'
                return render(request, 'Create_player.html', info)
        player_class_id = int(request.POST.get('player_class'))
        for player_class in Player_classes:
            if player_class.class_id == player_class_id and is_player_created == False:
                player_inventory = len(Player_inventory.objects.all()) + 1
                default_inventory = Class_inventory.objects.get(inventory_id=player_class.class_inventory)
                Player_inventory.objects.create(inventory_id=player_inventory,
                                                item1=default_inventory.item1, item2=default_inventory.item2,
                                                item3=default_inventory.item3, item4=default_inventory.item4,
                                                item5=default_inventory.item5, item6=default_inventory.item6,
                                                is_have_heal=default_inventory.is_have_heal,
                                                is_have_empty_slot=default_inventory.is_have_empty_slot)
                Player.objects.create(name=name, player_class=player_class_id, player_inventory=player_inventory,
                                      player_health=player_class.class_heals)
                url_temp = f'http://127.0.0.1:8000/Player/?player_name={name}'
                return redirect(url_temp)
            else:
                info['error'] = 'Такого класса не существует'
        return render(request, 'Create_player.html', info)
    return render(request, 'Create_player.html', info)

def Player_page(request):
    name = request.GET.get('player_name', 'Vasya')
    player = Player.objects.get(name=name)
    player_class = Player_class.objects.get(class_id=player.player_class)
    player_inventory = Player_inventory.objects.get(inventory_id=player.player_inventory)
    item1 = Item_list.objects.get(item_id=player_inventory.item1)
    item2 = Item_list.objects.get(item_id=player_inventory.item2)
    item3 = Item_list.objects.get(item_id=player_inventory.item3)
    item4 = Item_list.objects.get(item_id=player_inventory.item4)
    item5 = Item_list.objects.get(item_id=player_inventory.item5)
    item6 = Item_list.objects.get(item_id=player_inventory.item6)
    items = [item1, item2, item3, item4, item5, item6]
    inventory = [{'item_name': items[0].item_name, 'item_cooldown': items[0].skill_cooldown,
                  'damage_min': items[0].skill_effect_min, 'damage_max': items[0].skill_effect_max, 'item_description': items[0].description},
                 {'item_name': items[1].item_name, 'item_cooldown': items[1].skill_cooldown,
                  'damage_min': items[1].skill_effect_min, 'damage_max': items[1].skill_effect_max, 'item_description': items[1].description},
                 {'item_name': items[2].item_name, 'item_cooldown': items[2].skill_cooldown,
                  'damage_min': items[2].skill_effect_min, 'damage_max': items[2].skill_effect_max, 'item_description': items[2].description},
                 {'item_name': items[3].item_name, 'item_cooldown': items[3].skill_cooldown,
                  'damage_min': items[3].skill_effect_min, 'damage_max': items[3].skill_effect_max, 'item_description': items[3].description},
                 {'item_name': items[4].item_name, 'item_cooldown': items[4].skill_cooldown,
                  'damage_min': items[4].skill_effect_min, 'damage_max': items[4].skill_effect_max, 'item_description': items[4].description},
                 {'item_name': items[5].item_name, 'item_cooldown': items[5].skill_cooldown,
                  'damage_min': items[5].skill_effect_min, 'damage_max': items[5].skill_effect_max, 'item_description': items[5].description}]
    is_have_heal = player_inventory.is_have_heal
    is_have_empty_slot = player_inventory.is_have_empty_slot
    context = {'player_name': player.name, 'player_class': player_class.class_name,
               'player_inventory': inventory, 'health': player.player_health,
               'is_have_heal': is_have_heal, 'is_have_empty_slot': is_have_empty_slot, 'inventory': inventory, }
    return render(request, 'Player.html', context)

def Move_request(request):
    player_name = request.GET.get('player_name', 'Player')
    location_map_id = int(request.GET.get('location_map_id', '1'))
    run_end_location = Map_len.objects.get(id=1)
    location_map_id += 1
    if location_map_id == run_end_location.map_len:
        url_temp = f'http://127.0.0.1:8000/Winning_page/?player_name={player_name}'
        return redirect(url_temp)
    map_location = Map.objects.get(id_number=location_map_id)
    location = Location.objects.get(id_number=map_location.location_id)
    if (location.location_type == 'Empty'):
        print(location.location_name)
        this_location = Location_empty.objects.get(location_name=location.location_name)
        url_temp = f'http://127.0.0.1:8000/Location/?player_name={player_name}&location_name={this_location.location_name}&location_map_id={location_map_id}'
        return redirect(url_temp)
    if (location.location_type == 'Trap'):
        this_location = Location_trap.objects.get(location_name=location.location_name)
        url_temp = f'http://127.0.0.1:8000/Trap/?player_name={player_name}&location_name={this_location.location_name}&location_map_id={location_map_id}'
        return redirect(url_temp)
    if (location.location_type == 'Riddle'):
        this_location = Location_riddle.objects.get(location_name=location.location_name)
        url_temp = f'http://127.0.0.1:8000/Riddle/?player_name={player_name}&location_name={this_location.location_name}&location_map_id={location_map_id}'
        return redirect(url_temp)
    if (location.location_type == 'Enemy'):
        this_location = Location_enemy.objects.get(location_name=location.location_name)
        url_temp = f'http://127.0.0.1:8000/Battel/?player_name={player_name}&location_map_id={location_map_id}&location_name={this_location.location_name}&turn={0}'
        return redirect(url_temp)


def Riddel_page(request):
    player_name = request.GET.get('player_name', 'Player')
    location_name = request.GET.get('location_name', 'Default')
    location_map_id = request.GET.get('location_map_id', '3')
    location = Location_riddle.objects.get(location_name=location_name)
    is_riddle_solved = False
    context = {'player_name': player_name, 'location_name': location.location_name, 'location_map_id':location_map_id,
               'location_description': location.description, 'is_riddle_solved': is_riddle_solved,}
    if request.method == 'POST':
        answer = request.POST.get('answer')
        if answer == location.riddle_answer:
            is_riddle_solved = True
            riddle_solved_text = location.riddle_solved_text
            context = {'player_name': player_name, 'location_name': location.location_name,
                       'location_map_id': location_map_id, 'location_description': location.description,
                       'is_riddle_solved': is_riddle_solved, 'riddle_solved_text': riddle_solved_text}
            return render(request, 'Riddle.html', context)
        is_riddle_solved = False
        riddle_solved_text = 'Ответ не верен'
        context = {'player_name': player_name, 'location_name': location.location_name,
                   'location_map_id': location_map_id, 'location_description': location.description,
                   'is_riddle_solved': is_riddle_solved, 'riddle_solved_text': riddle_solved_text}
        return render(request, 'Riddle.html', context)
    return render(request, 'Riddle.html', context)
    pass

def Trap_page(request):
    player_name = request.GET.get('player_name', 'Player')
    location = request.GET.get('location_name', 'Default')
    location_map_id = request.GET.get('location_map_id', '3')
    trap_location = Location_trap.objects.get(location_name=location)
    trap_activation_chance = trap_location.trap_activation_chance
    if randint(0, 100) < trap_activation_chance and trap_location.trap_exists == True:
        this_player_health = Player.objects.get(name=player_name).player_health
        trap_damage = randint(trap_location.trap_damage_min, trap_location.trap_damage_max + 1)
        if this_player_health - trap_damage < 0:
            is_player_dead = True
            contex = {'player_name': player_name, 'reason_name': trap_location.name, 'is_player_dead': is_player_dead,
                      'text': f'Игрок {player_name} ловушка в {trap_location.location_name} оказалась слишком коварна'}
            url_temp = f'http://127.0.0.1:8000/Gameover/?player_name={player_name}&reason_name={trap_location.location_name}'
            return redirect(url_temp)
        Player.objects.filter(name=player_name).update(player_health=this_player_health - trap_damage)
        is_player_dead = False
        context = {'player_name': player_name, 'player_health': this_player_health,
                   'location_name': trap_location.location_name, 'location_description': trap_location.description, 'is_player_dead': is_player_dead,
                   'trap_exists': True, 'trap_found': False, 'trap_damage': trap_damage, 'trap_description': trap_location.trap_description,
                   'location_map_id': location_map_id, }
    else:
        is_player_dead = False
        context = {'player_name': player_name, 'location_name': trap_location.location_name, 'is_player_dead': is_player_dead,
                   'location_description': trap_location.description, 'trap_description': trap_location.trap_description,
                   'trap_exists': True, 'trap_found': True, 'trap_damage': 0, 'location_map_id': location_map_id, }
    return render(request, 'Trap.html', context)

def Battel_page(request):
    player_name = request.GET.get('player_name', 'Player')
    location_name = request.GET.get('location_name', 'Default')
    location_map_id = request.GET.get('location_map_id', '3')
    location = Location_enemy.objects.get(location_name=location_name)
    enemy_name = location.enemy_name
    turn = int(request.GET.get('turn', '0'))
    player = Player.objects.get(name=player_name)
    enemy = Enemy.objects.get(name=enemy_name)
    is_player_win = request.GET.get('is_player_win', False)
    location_description = location.description
    enemy_description = enemy.enemy_description
    if turn == 0:
        Battel_start(player_name, enemy_name)
        battel = Battel_stat.objects.get(id=1)
        inventory = make_inventory(player, battel, turn)
        context = {'player_name': player_name, 'enemy_name': enemy_name, 'location_name': location.location_name,
                   'location_description': location_description, 'enemy_description': enemy_description,
                   'location_map_id': location_map_id, 'turn': turn, 'player_health': player.player_health, 'inventory': inventory, }
        return render(request, 'Battel.html', context)
    battel = Battel_stat.objects.get(id=1)
    inventory = make_inventory(player, battel, turn)
    player_used_item = request.GET.get('player_used_item', 'Empty')
    player_inventory_slot = 5
    for item in inventory:
        if item['item_name'] == player_used_item:
            player_inventory_slot = item['slot']
    Player_turn(player_used_item, player_inventory_slot)
    battel = Battel_stat.objects.get(id=1)
    if battel.Enemy_current_health <= 0:
        is_player_win = True
        location_description = f'{player_name} победил {enemy_name}'
        Player.objects.filter(name=player_name).update(player_health=battel.Player_current_health)
        context = {'player_name': player_name, 'enemy_name': enemy_name, 'location_name': location.location_name,
                   'location_description': location_description, 'enemy_description': enemy_description,
                   'location_map_id': location_map_id, 'turn': turn, 'player_health': player.player_health,
                   'inventory': inventory, 'is_player_win': is_player_win, }
        return render(request, 'Battel.html', context)
    Enemy_turn(enemy)
    battel = Battel_stat.objects.get(id=1)
    if battel.Player_current_health <= 0:
        url_temp = f'http://127.0.0.1:8000/Gameover/?reason_name={location_name}&player_name={player_name}'
        return redirect(url_temp)
    turn += 1
    inventory = make_inventory(player, battel, turn)
    context = {'player_name': player_name, 'enemy_name': enemy_name, 'location_name': location.location_name,
               'location_description': location_description, 'enemy_description': enemy_description,
               'location_map_id': location_map_id, 'turn': turn, 'player_health': player.player_health,
               'inventory': inventory, 'is_player_win': is_player_win,
               'enemy_battel_text': battel.Enemy_battel_text, }
    Player.objects.filter(name=player_name).update(player_health=battel.Player_current_health)
    return render(request, 'Battel.html', context)


def Location_page(request):
    player_name = request.GET.get('player_name', 'Player')
    location_name = request.GET.get('location_name', 'Default')
    location = Location_empty.objects.get(location_name = location_name)
    location_map_id = request.GET.get('location_map_id', '3')
    context = {'player_name': player_name, 'location_name': location.location_name,
               'location_description': location.description, 'location_map_id': location_map_id}
    return render(request, 'Location.html', context)

def Enter_dungeon_page(request):
    player_name = request.GET.get('player_name', 'Player')
    run_len = Map_len.objects.get(id=1).map_len
    current_len = int(len(Map.objects.all()))
    if current_len < run_len:
        for i in range(current_len+1, run_len):
            Map.objects.create()
    for i in range(3, run_len+1):
        Map.objects.filter(id=i).update(id_number=i, location_id=randint(3, len(Location.objects.all())))
    map_location = Map.objects.get(id=1)
    location = Location.objects.get(id_number=map_location.location_id)
    location_description = Location_empty.objects.get(location_name=location.location_name)
    player = Player.objects.get(name=player_name)
    player_class = Player_class.objects.get(class_id=player.player_class)
    Player.objects.filter(name=player_name).update(player_health=player_class.class_heals)
    default_inventory = Class_inventory.objects.get(inventory_id=player_class.class_inventory)
    Player_inventory.objects.filter(inventory_id=player.player_inventory).update(item1=default_inventory.item1,
    item2=default_inventory.item2, item3=default_inventory.item3, item4=default_inventory.item4,
    item5=default_inventory.item5, item6=default_inventory.item6, is_have_heal=default_inventory.is_have_heal,
    is_have_empty_slot=default_inventory.is_have_empty_slot)
    context = {'player_name': player_name, 'location_name': location.location_name,
                   'location_description': location_description.description, 'location_map_id': 2}
    return render(request, 'Enter_dungeon.html', context)


def Winning_page(request):
    player_name = request.GET.get('player_name', 'Player')
    map_location = Map.objects.get(id=2)
    this_location = Location.objects.get(id_number=map_location.location_id)
    location = Location_empty.objects.get(location_name=this_location.location_name)
    context = {'player_name': player_name, 'location_name': location.location_name,
               'location_description': location.description, 'location_map_id': 2}
    battel = Battel_stat.objects.get(id=1)
    Player.objects.filter(name=player_name).update(player_health=battel.Player_default_health)
    Map_len.objects.all().update(map_len=10)
    return render(request, 'Winning_page.html', context)

def Gameover_page(request):
    player_name = request.GET.get('player_name', 'Player')
    reason_name = request.GET.get('reason_name', 'Вход')
    text=f'{player_name} пал в локации {reason_name}'
    context = {'player_name': player_name, 'reason_name': reason_name, 'text': text}
    battel = Battel_stat.objects.get(id=1)
    Player.objects.filter(name=player_name).update(player_health=battel.Player_default_health)
    return render(request, 'Gameover.html', context)
