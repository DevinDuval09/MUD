from items import item_dict

class Room(object):
    def __init__(self, number, description, inventory=[], characters=[], exits={}):
        self.number = number
        self._description = description
        self.inventory = inventory
        self.exits = exits
        self.characters = characters
    
    def description(self):
        '''Provide description of room along with any a list of interactable items'''
        desc = self._description
        if self.inventory:
            desc += f'\nIn the room you see a {" ".join([item_dict[item].description() for item in self.inventory])}.'
        if self.characters:
            desc += f'\nStanding in the room you see {self.characters}.'
        
        if self.exits.keys():
            desc += f'\n There are exits to the {self.exits.keys()}.'
        return desc


rooms_dict = {0: Room(0, 'A room with doors headed north, west, and east.', inventory=['magic box'], exits={'north': 3, 'west': 1, 'east': 2}),
              1: Room(1, 'A room with a door headed east.', inventory=['steel sword'], exits={'east': 0}),
              2: Room(2, 'A room with a door headed west.', inventory=['wooden shield', 'chainmail shirt'], exits={'west': 0}),
              3: Room(3, 'A room with a door headed south.', characters=['training dummy'], exits={'south': 0})}