from django.db import models

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=30)
    player_class = models.IntegerField(default=1)
    player_inventory = models.IntegerField(default=1)
    player_health = models.IntegerField(default=15)

class Player_inventory(models.Model):
    inventory_id = models.IntegerField(default=1)
    item1 = models.IntegerField(default=0)
    item2 = models.IntegerField(default=0)
    item3 = models.IntegerField(default=0)
    item4 = models.IntegerField(default=0)
    item5 = models.IntegerField(default=0)
    item6 = models.IntegerField(default=0)
    is_have_heal = models.BooleanField(default=False)
    is_have_empty_slot = models.BooleanField(default=True)

class Player_class(models.Model):
    class_id = models.IntegerField(default=1)
    class_heals = models.IntegerField(default=15)
    class_name = models.CharField(max_length=30)
    class_description = models.CharField(default='',max_length=30)
    class_inventory = models.IntegerField(default=1)

class Class_inventory(models.Model):
    inventory_id = models.IntegerField(default=1)
    item1 = models.IntegerField(default=0)
    item2 = models.IntegerField(default=0)
    item3 = models.IntegerField(default=0)
    item4 = models.IntegerField(default=0)
    item5 = models.IntegerField(default=0)
    item6 = models.IntegerField(default=0)
    is_have_heal = models.BooleanField(default=False)
    is_have_empty_slot = models.BooleanField(default=True)

class Item_list(models.Model):
    item_id = models.IntegerField(default=0)
    item_type = models.CharField(default='Empty', max_length=30)
    item_name = models.CharField(default='Empty', max_length=30)
    description = models.TextField(null=True, blank=True)
    skill_description = models.CharField(max_length=30, null=True)
    skill_effect_max = models.IntegerField(default=3)
    skill_effect_min = models.IntegerField(default=1)
    skill_cooldown = models.IntegerField(default=1)

class Enemy(models.Model):
    name = models.CharField(max_length=30)
    enemy_class = models.IntegerField(default=1)
    enemy_description = models.TextField(null=True, blank=True)
    health = models.IntegerField(default=5)
    enemy_skill1_id = models.IntegerField(default=0)
    enemy_skill2_id = models.IntegerField(default=0)


class Enemy_skill(models.Model):
    skill_name = models.CharField(max_length=30)
    skill_id = models.IntegerField(default=1)
    skill_type = models.CharField(default='Attack', max_length=30)
    skill_description = models.TextField(null=True, blank=True)
    skill_effect_max = models.IntegerField(default=3)
    skill_effect_min = models.IntegerField(default=1)
    skill_cooldown = models.IntegerField(default=1)


class Location(models.Model):
    id_number = models.IntegerField(null=True)
    location_name = models.CharField(max_length=30)
    location_type = models.CharField(default='Empty', max_length=30)
    is_it_tech = models.BooleanField(default=False)


class Location_trap(models.Model):
    location_name = models.CharField(default='Trap', max_length=30)
    description = models.TextField(null=True, blank=True)
    trap_description = models.TextField(null=True, blank=True)
    trap_activation_chance = trap_damage_max = models.IntegerField(default=36)
    trap_exists = models.BooleanField(default=True)
    trap_found = models.BooleanField(default=False)
    trap_damage_max = models.IntegerField(default=3)
    trap_damage_min = models.IntegerField(default=1)


class Location_enemy(models.Model):
    location_name = models.CharField(default='Enemy', max_length=30)
    description = models.TextField(null=True, blank=True)
    enemy_name = models.CharField(max_length=30)


class Location_riddle(models.Model):
    location_name = models.CharField(default='Riddle', max_length=30)
    description = models.TextField(null=True, blank=True)
    riddle_answer = models.CharField(max_length=30)
    riddle_solved_text = models.CharField(max_length=30)


class Location_empty(models.Model):
    location_name = models.CharField(default='Empty', max_length=30)
    description = models.TextField(null=True, blank=True)


class Map(models.Model):
    id_number = models.IntegerField(null=True)
    location_id = models.IntegerField(null=True)

class Map_len(models.Model):
    map_len = models.IntegerField(default=7)

class Battel_stat(models.Model):
    Player_default_health = models.IntegerField(default=15)
    Player_current_health = models.IntegerField(default=15)
    Enemy_default_health = models.IntegerField(default=15)
    Enemy_current_health = models.IntegerField(default=15)
    Enemy_skill1_cooldown = models.IntegerField(default=0)
    Enemy_skill2_cooldown = models.IntegerField(default=0)
    Player_item1_cooldown = models.IntegerField(default=0)
    Player_item1_default_cooldown = models.IntegerField(default=99)
    Is_slot1_empty = models.BooleanField(default=True)
    Player_item2_cooldown = models.IntegerField(default=0)
    Player_item2_default_cooldown = models.IntegerField(default=99)
    Is_slot2_empty = models.BooleanField(default=True)
    Player_item3_cooldown = models.IntegerField(default=0)
    Player_item3_default_cooldown = models.IntegerField(default=99)
    Is_slot3_empty = models.BooleanField(default=True)
    Player_item4_cooldown = models.IntegerField(default=0)
    Player_item4_default_cooldown = models.IntegerField(default=99)
    Is_slot4_empty = models.BooleanField(default=True)
    Player_item5_cooldown = models.IntegerField(default=0)
    Player_item5_default_cooldown = models.IntegerField(default=99)
    Is_slot5_empty = models.BooleanField(default=True)
    Player_item6_cooldown = models.IntegerField(default=0)
    Player_item6_default_cooldown = models.IntegerField(default=99)
    Is_slot6_empty = models.BooleanField(default=True)
    Enemy_battel_text = models.TextField(null=True, blank=True)


