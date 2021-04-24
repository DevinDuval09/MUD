'''track item information'''
#TODO: add equipment subclass
#TODO: add skills that give bonus
#TODO: passive vs active skills
from skills import block, bash
class Item(object):
    def __init__(self, id, description, active_skills=[], passive_skills= [], proficiency_skills={}, **stats):
        self.number = id
        self._description = description
        self.active_skills = active_skills
        self.proficiency_skills = proficiency_skills
        self.passive_skills = passive_skills
        for key, value in stats.items():
            if key.lower() != 'inventory_items':
                setattr(self, key, value)
    
    def description(self):
        return f'a {self._description}.'


class Container(Item):
    def __init__(self, id, description, active_skills=[], proficiency_skills={}, **stats):
        super().__init__(id, description, active_skills=active_skills, proficiency_skills=proficiency_skills, **stats)
        self._open = False
        self.inventory = []
        if 'inventory_items' in stats:
            self.inventory.extend(stats['inventory_items'])
    
    def description(self):
        if self._open:
            return 'an open ' + self._description + f' containing {self.inventory}.'
        else:
            return f'a {self._description}.'
    
    def open(self):
        self._open = True
        return f'You open the {self._description}. It contains {self.inventory}.'

class Equipment(Item):
    def __init__(self, id, description, slot, associated_skill=None, active_skills=[], proficiency_skills={}, **stats):
        super().__init__(id, description, active_skills=active_skills, proficiency_skills=proficiency_skills, **stats)
        self.slot = slot
        self.associated_skill = associated_skill
    


    
item_dict = {'magic box': Container(0, 'magic box', inventory_items=['magical crystal'], strength=2),
             'magical crystal': Item(1, 'magical crystal', strength=5),
             'steel sword': Equipment(2, 'steel sword', 'in hand', associated_skill='sword'),
             'wooden shield': Equipment(3, 'wooden shield', 'in hand', associated_skill='shield', passive_skills=[block], armor=1),
             'chainmail shirt': Equipment(4, 'chainmail shirt', 'chest', armor=3),
             'book of butt kicking': Item(5, 'book of butt kicking', active_skills=[bash], proficiency_skills={'shield': 1, 'sword': 2})}
    