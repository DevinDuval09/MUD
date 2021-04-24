'''character class'''
from room import rooms_dict
from items import item_dict, Container, Equipment
#TODO: add character classes
#TODO: add inventory command to review inventory
#TODO: add customizable player descriptions
#TODO: object permanence. mongodb?
#TODO: documentation
#TODO: active, passive combat commands
#TODO: player creation sequence
#TODO: add unequip command
class Character(object):
    '''
    Store information about characters and provide
    commands for the characters to use.
    '''
    def __init__(self, name, STR=1, DEX=1, INT=1, CON=1, WIS=1, CHA=1):
        self.name = name
        self.strength = STR #melee to hit: str + skill bonus + roll/damage = weapon stat + roll + str bonus
        self.dexterity = DEX #range to hit: dex + skill bonus + roll/damage = weapon stat + roll + dex bonus/initiative = roll + dex bonus
        self.intelligence = INT
        self.constitution = CON #10 hp per const = max_health
        self.wisdom = WIS
        self.charisma = CHA
        self.current_health = CHA * 10
        self.armor = 0 #armor = armor(from equipment/magic) + dex bonus? - overburden/to hit must beat armor
        self.inventory = []
        self.active_skills = {}
        self.proficiency_skills = {}
        self.passive_skills = []
        self.equipment = {'head':None,
                          'chest': None,
                          'hands': None,
                          'main hand': None,
                          'off hand': None,
                          'utility belt': None,
                          'pants': None,
                          'shoes': None}
        self.room = 0
    
    def actions(self):
        attrs = dir(self)
        actions = []
        for attr in attrs:
            print('attr: ', attr)
            print('attr[1]: ', attr[1])
            if callable(getattr(self, attr)) and attr[1] != '_' and 'Character' not in attr:
                actions.append(attr)
        actions.append('attack')
        return f'Your available actions are {actions}.'
    
    def __get_stat(self, stat:str)->int:
        '''
        Calculate fully buffed value for stat
        '''
        level = getattr(self, stat)
        for item in self.inventory:
            item = item_dict[item]
            if not isinstance(item, Equipment):
                if stat in dir(item):
                    level += getattr(item, stat)
        for value in self.equipment.values():
            if value:
                item = item_dict[value]
                if stat in dir(item):
                    level += getattr(item, stat)
        return level

    def stats(self):
        character_stats = {'strength': 0,
                           'dexterity': 0,
                           'intelligence': 0,
                           'constitution': 0,
                           'wisdom': 0,
                           'charisma': 0,
                           'current_health': 0,
                           'armor': 0}
        for key in character_stats.keys():
            character_stats[key] = self.__get_stat(key)
        
        summary = 'Your current stats are: '
        for stat, value in character_stats.items():
            summary += f'\n{stat}: {value}'
        return summary
    
    def grab(self, item):
        available_stuff = {rooms_dict[self.room]: rooms_dict[self.room].inventory}
        for thing in self.inventory:
            if isinstance(item_dict[thing], Container) and item_dict[thing]._open:
                available_stuff[item_dict[thing]] = item_dict[thing].inventory
        for thing in rooms_dict[self.room].inventory:
            if isinstance(item_dict[thing], Container) and item_dict[thing]._open:
                available_stuff[item_dict[thing]] = item_dict[thing].inventory
        for container, inventory in available_stuff.items():
            if item in inventory:
                container.inventory.remove(item)
                self.inventory.append(item)
                return f'You pick up a {item} from {container._description}.'
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
        new_room = False
        current_room = rooms_dict[self.room]
        arg = argument.lower().strip()
        if arg in current_room.exits.keys():
            new_room = current_room.exits[arg]
        
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

        return f'You say "{argument}"'
    
    def open(self, item):
        if item in self.inventory or rooms_dict[self.room].inventory:
            item = item_dict[item]
            if isinstance(item, Container) and not item._open:
                x = f'You open the {item.description()}. It contains {item.inventory}.'
                item.open()
                return x
            elif isinstance(item, Container) and item._open:
                return f'You feel that there is a deep philosophical question between trying to open an open {item.description}.'
            elif not isinstance(item, Container):
                return f'You desparately try to open the {item.description}, for reasons unknown, but it refuses to open.'
        else:
            f'There is no {item}.'
    
    def equip(self, item):
        if not isinstance(item_dict[item], Equipment):
            return f'How do you intend to equip a {item}?'
        equipment = item_dict[item]
        print('player equipment: ', self.equipment)
        print('equipment slot: ', equipment.slot)
        if self.equipment[equipment.slot] is None:
            #print(f'{self.name} inventory: ', self.inventory)
            self.inventory.remove(equipment._description)
            self.equipment[equipment.slot] = equipment._description
            response = f'You equipped the {equipment._description} on your {equipment.slot}.'
        elif self.equipment[equipment.slot] and equipment.slot[-4:] == 'hand':
            if equipment.slot == 'main hand' and not self.equipment['off hand']:
                self.equipment['off hand'] = equipment._description
            if equipment.slot == 'off hand' and not self.equipment['main hand']:
                self.equipment['main hand'] = equipment._description
        else:
            response = f'You must first remove {self.equipment[equipment.slot]} from your {equipment.slot}.'
        
        if 'remove' not in response:
            print('equipment: ', equipment._description)
            print('equipment skills: ', equipment.active_skills)
            for skill in equipment.active_skills:
                setattr(self, skill.__name__, skill)
                self.active_skills[equipment._description] = skill.__name__
            print('equipment skills: ', equipment.proficiency_skills)
            for skill, level in equipment.proficiency_skills.items():
                if skill in self.proficiency_skills.keys():
                    self.proficiency_skills[skill] += level
                else:
                    self.proficiency_skills[skill] = level
            print('eqiupment skills: ', equipment.passive_skills)
            for skill in equipment.passive_skills:
                if skill not in self.passive_skills:
                    setattr(self, skill.__name__, skill)
        return response

    



