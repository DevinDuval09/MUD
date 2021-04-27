from character import Character
from items import Equipment
from utilities import to_hit_roll, roll_d10, roll_d20

def bash(self, target:Character)->str:
    print('self: ', self.name)
    print('target: ', target.name)
    if self.equipment['off hand']:
        weapon = self.equipment['off hand']
    else:
        weapon = Equipment(None, 'fist',slot='off hand', associated_skill=None)
    to_hit = to_hit_roll(self, weapon)
    if to_hit >= target._Character__get_stat('armor'):
        if weapon._description == 'fist':
            damage = max(roll_d10() - 5, 1)
        else:
            damage = roll_d10()
    target.current_health -= damage
    return f'{self.name} bashes {target.name} in the face with his {weapon._description} for {damage} damage.'

def block(self):
    return "You wave your shield around to block huge sweeping bats."

skills_dict = {'bash': bash, 'block': block}