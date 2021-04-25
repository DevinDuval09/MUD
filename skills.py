'''Injectable skills that a character can learn / obtain.
   These are all active skills.'''
from character import Character
from server import roll_d10, roll_d20, to_hit_roll
from items import item_dict, Equipment

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

