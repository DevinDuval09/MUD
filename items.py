'''track item information'''
#TODO: add equipment subclass
#TODO: add skills that give bonus
#TODO: passive vs active skills
from types import MethodType
stats_list = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'armor']
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

class Book(Item):
    def __init__(self, id, description, effect=[None], active_skills=[], passive_skills=[], proficiency_skills=[], **stats):
        super().__init__(id, description, active_skills=active_skills, passive_skills=passive_skills, proficiency_skills=proficiency_skills, **stats)
        self.effects = effect

    def reading_effect(self, player)->str:
        message = "You read the book and "
        for effect in self.effects:
            if effect:
                if effect == 'stats':
                    my_stats = [stat for stat in stats_list if stat in dir(self)]
                    my_values = [getattr(self, stat) for stat in my_stats]
                    for stat, value in zip(my_stats, my_values):
                        message += f'feel your {stat} increasing '
                        setattr(player, stat, getattr(player, stat) + value)
                elif effect == 'passive_skills':
                    for skill in self.passive_skills:
                        if skill not in player.passive_skills:
                            message += f'suddenly understand the art of {skill.__name__}'
                            player.passive_skills.append(skill)
                elif effect == 'active_skills':
                    for skill in self.active_skills:
                        if skill.__name__ not in dir(player):
                            message += f'think you can now {skill.__name__}'
                            setattr(player, skill.__name__, MethodType(skill, player))
                            print(getattr(player, skill.__name__))
                elif effect == 'proficiency_skills':
                    print('in proficiency_skills loop')
                    for skill, rating in self.proficiency_skills.items():
                        print('skill: ', skill)
                        print('rating: ', rating)
                        message += f'gain a better understanding of {skill} usage'
                        if skill in player.proficiency_skills.keys():
                            player.proficiency_skills[skill] += rating
                        else:
                            player.proficiency_skills[skill] = rating
                else:
                    message += 'realize it is gibberish'
            else:
                message += 'think it is a bit of a bore'
            message += '.'
        return message







    
    