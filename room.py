class Room(object):
    def __init__(self, number, description, inventory):
        self.number = number
        self._description = description
        self.inventory = inventory
    
    def description(self):
        '''Provide description of room along with any a list of interactable items'''
        if self.inventory:
            return self._description + f' In the room you see a {" ".join(self.inventory)}.'
        else:
            return self._description


rooms_dict = {0: Room(0, 'A room with doors headed north, west, and east.', ['box']),
              1: Room(1, 'A room with a door headed east.', []),
              2: Room(2, 'A room with a door headed west.', []),
              3: Room(3, 'A room with a door headed south.', [])}