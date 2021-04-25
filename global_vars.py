from random import randint
from items import Container, Item, Equipment
from character import Character
from room import Room

rooms_dict = {0: Room(0, 'A room with doors headed north, west, and east.', inventory=['magic box'], exits={'north': 3, 'west': 1, 'east': 2}),
              1: Room(1, 'A room with a door headed east.', inventory=['steel sword'], exits={'east': 0}),
              2: Room(2, 'A room with a door headed west.', inventory=['wooden shield', 'chainmail shirt'], exits={'west': 0}),
              3: Room(3, 'A room with a door headed south.', characters=['training dummy'], exits={'south': 0})}

item_dict = {'magic box': Container(0, 'magic box', inventory_items=['magical crystal'], strength=2),
             'magical crystal': Item(1, 'magical crystal', strength=5),
             'steel sword': Equipment(2, 'steel sword', 'main hand', associated_skill='sword'),
             'wooden shield': Equipment(3, 'wooden shield', 'off hand', associated_skill='shield', passive_skills=[block], armor=1),
             'chainmail shirt': Equipment(4, 'chainmail shirt', 'chest', armor=3),
             'book of butt kicking': Item(5, 'book of butt kicking', active_skills=[bash], proficiency_skills={'shield': 1, 'sword': 2})}

def roll_d20():
    '''generate random number between 1 and 20'''
    return randint(1, 20)
    
def roll_d10():
    '''generate random number between 1 and 10'''
    return randint(1, 10)

def to_hit_roll(player:Character, weapon:Equipment)->int:
    bonus = player.proficiency_skills.get(weapon.associated_skill, 0)
    return roll_d20() + bonus

def block(self):
    return "You wave your shield around to block huge sweeping bats."

def bash(self, target:Character, weapon:str=None)->str:
    if weapon:
        weapon = item_dict[weapon]
    else:
        if self.equipment['off hand']:
            weapon = self.equipment['off hand']
        else:
            weapon = Equipment(None, 'fist',slot='off hand', associated_skill=None)
    to_hit = to_hit_roll(self, weapon)
    if to_hit >= target.__get_stat('armor'):
        if weapon._description == 'fist':
            damage = max(roll_d10() - 5, 1)
        else:
            damage = roll_d10()
    target.current_health -= damage
    return f'{self.name} bashes {target.name} in the face with his {weapon._description} for {damage} damage.'