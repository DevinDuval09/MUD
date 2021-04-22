'''track item information'''
#TODO: add container subclass
class Item(object):
    def __init__(self, id, description, inventory=False, **stats):
        self.number = id
        self._description = description
        for key, value in stats.items():
            if key.lower() != 'inventory_items':
                setattr(self, key, value)
        if inventory:
            self.inventory = []
            if 'inventory_items' in stats:
                self.inventory.extend(stats['inventory_items'])
    
    def description(self):
        if self.inventory:
            return 'a ' + self._description + f' containing {self.inventory}.'
        else:
            return f'a {self._description}.'
    
item_dict = {'magic box': Item(0, 'magic box', inventory=True, inventory_items=['magical crystal'], strength=2),
             'magical crystal': Item(1, 'magical crystal', inventory=False, strength=5)}
    