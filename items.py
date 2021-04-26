'''track item information'''
#TODO: add equipment subclass
#TODO: add skills that give bonus
#TODO: passive vs active skills
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



    
    