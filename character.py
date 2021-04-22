'''character class'''
from room import rooms_dict
from items import item_dict
#TODO: add character classes
#TODO: add commands method to get list of commands
#TODO: add stats command that displays all stats data, including equipment and inventory buffs
#TODO: add equipment
class Character(object):
    '''
    Store information about characters and provide
    commands for the characters to use.
    '''
    def __init__(self, name):
        self.name = name
        self.strength = 1
        self.inventory = []
        self.room = 0
    
    def grab(self, item):
        if item in rooms_dict[self.room].inventory:
            rooms_dict[self.room].inventory.remove(item)
            self.inventory.append(item)
            return f'You pick up a {item}.'
        else:
            return f'You must be halucinating. There is no {item} in here.'

    def drop(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            rooms_dict[self.room].inventory.append(item)
            return f'You drop a {item}.'
        else:
            return f'You are not carrying a {item}.'

    def move(self, argument):
        """
        Moves the client from one room to another.
        
        Examines the argument, which should be one of:
        
        * "north"
        * "south"
        * "east"
        * "west"
        
        "Moves" the client into a new room by adjusting self.room to reflect the
        number of the room that the client has moved into.
        
        Puts the room description (see `self.room_description`) for the new room
        into "self.output_buffer".
        
        :param argument: str
        :return: None
        """
        #TODO: Make this section easier to scale.
        new_room = False
        arg = argument.lower().strip()
        if self.room == 0 and arg == 'north':
            new_room = 3
        elif self.room == 0 and arg == 'east':
            new_room = 2
        elif self.room == 0 and arg == 'west':
            new_room = 1
        elif self.room == 1 and arg == 'east':
            new_room = 0
        elif self.room == 2 and arg == 'west':
            new_room = 0
        elif self.room == 3 and arg == 'south':
            new_room = 0
        
        if new_room is False:
            return f"You bump your head against the {argument.lower()}ern wall. That was dumb."
        else:
            self.room = new_room
            return rooms_dict[self.room].description()

    def look(self, argument=None):
        '''
        Repeat the view of the room or object
        '''
        if argument is None:
            description = rooms_dict[self.room].description()
        else:
            try:
                if argument in self.inventory:
                    item = item_dict[argument]
                elif argument in rooms_dict[self.room].inventory:
                    item = item_dict[argument]
                else:
                    item = None
                if item:
                    description = item.description()
                else:
                    description = f'You wish you had an {argument}.'
            except AttributeError:
                description = rooms_dict[self.room].description()
        return f'{description}'

    def say(self, argument):
        """
        Lets the client speak by putting their utterance into the output buffer.
        
        For example:
        `self.say("Is there anybody here?")`
        would put
        `You say, "Is there anybody here?"`
        into the output buffer.
        
        :param argument: str
        :return: None
        """

        self.output_buffer = f'You say "{argument}"'


