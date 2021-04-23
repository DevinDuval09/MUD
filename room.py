from items import item_dict

class Room(object):
    def __init__(self, number, description, inventory=[], exits={}):
        self.number = number
        self._description = description
        self.inventory = inventory
        self.exits = exits
    
    def description(self):
        '''Provide description of room along with any a list of interactable items'''
        print(self.inventory)
        if self.inventory:
            return self._description + f' In the room you see a {" ".join([item_dict[item].description() for item in self.inventory])}.'
        else:
            return self._description


rooms_dict = {0: Room(0, 'A room with doors headed north, west, and east.', inventory=['magic box'], exits={'north': 3, 'west': 1, 'east': 2}),
              1: Room(1, 'A room with a door headed east.', inventory=['steel sword'], exits={'east': 0}),
              2: Room(2, 'A room with a door headed west.', inventory=['wooden shield', 'chainmail shirt'], exits={'west': 0}),
              3: Room(3, 'A room with a door headed south.', exits={'south': 0})}