from random import randint
from character import Character
from items import Equipment

#TODO: add get_object and connect to mongodb
def roll_d20():
    '''generate random number between 1 and 20'''
    return randint(1, 20)
    
def roll_d10():
    '''generate random number between 1 and 10'''
    return randint(1, 10)

def roll_d4():
    return randint(1, 4)

def to_hit_roll(player:Character, weapon:Equipment)->int:
    bonus = player.proficiency_skills.get(weapon.associated_skill, 0)
    return roll_d20() + bonus