'''track item information'''
#TODO: add equipment subclass
class Item(object):
    def __init__(self, id, description, inventory=False, **stats):
        self.number = id
        self._description = description
        for key, value in stats.items():
            if key.lower() != 'inventory_items':
                setattr(self, key, value)
    
    def description(self):
        return f'a {self._description}.'


class Container(Item):
    def __init__(self, id, description, **stats):
        super().__init__(id, description, **stats)
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

    
item_dict = {'magic box': Container(0, 'magic box', inventory_items=['magical crystal'], strength=2),
             'magical crystal': Item(1, 'magical crystal', strength=5)}
    