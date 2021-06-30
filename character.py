'''character class'''
from logger import logger
from room import Room
from items import Item, Container, Equipment, Book
#TODO: add character classes
#TODO: add inventory command to review inventory
#TODO: add customizable player descriptions
#TODO: object permanence. mongodb?
#TODO: documentation
#TODO: active, passive combat commands
#TODO: player creation sequence
#TODO: add unequip command
#TODO: fix attack
class Character(object):
    '''
    Store information about characters and provide
    commands for the characters to use.
    '''
    def __init__(self, name:str, spawn_point:Room, desc=None, STR:int=1, DEX:int=1, INT:int=1, CON:int=1, WIS:int=1, CHA:int=1):
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
        self.room = spawn_point
        if desc is None:
            self._description = name
        else:
            self._description = desc
    
    def actions(self):
        attrs = dir(self)
        actions = []
        for attr in attrs:
            if callable(getattr(self, attr)) and attr[1] != '_' and 'Character' not in attr:
                actions.append(attr)
        actions.append('attack')
        return f'Your available actions are {actions}.'
    
    def __get_stat(self, stat:str)->int:
        '''
        Calculate fully buffed value for stat
        '''
        logger.info('stat: %s' % stat)
        level = getattr(self, stat)
        for item in self.inventory:
            if not isinstance(item, Equipment):
                if stat in dir(item):
                    level += getattr(item, stat)
        for item in self.equipment.values():
            if item:
                logger.info('item: %s' % item._description)
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
                           }
        for key in character_stats.keys():
            character_stats[key] = self.__get_stat(key)
        
        summary = 'Your current stats are: '
        for stat, value in character_stats.items():
            summary += f'\n{stat}: {value}\tbonus: {value // 3}'
        additional_stats = {'armor': self.__get_stat('armor'), 'current_health': self.__get_stat('current_health')}
        for stat, value in additional_stats.items():
            summary += f'\n{stat}: {value}'
        main_weapon = self.equipment['main hand']
        if main_weapon:
            bonus = self.proficiency_skills.get(self.equipment['main hand'].associated_skill, 0)
        else:
            bonus = 0
        summary += f'\nmain hand to hit bonus: {bonus}'
        armor_bonus = self.__get_stat('armor')
        dex_bonus = self.__get_stat('dexterity') // 3
        summary += f'\ntotal defense rating: {armor_bonus + dex_bonus}'
        summary += '\nProficiencies:'
        for proficiency, rating in self.proficiency_skills.items():
            summary += f'\n{proficiency}: {rating}'
        logger.info(f'{self.name}stats: \nsummary')
        return summary
    
    def grab(self, thing:Item)->str:
        logger.info('grab item: %s' % thing._description)
        available_stuff = {self.room: self.room.inventory}
        for item in self.inventory:
            #check inventory for open containers
            if isinstance(item, Container) and item._open:
                available_stuff[item] = item.inventory
        for item in self.room.inventory:
            #check items in room for open containers
            if isinstance(item, Container) and item._open:
                available_stuff[item] = item.inventory
        for container, inventory in available_stuff.items():
            for item in inventory:
                if thing._description == item._description:
                    thing = item
                container.inventory.remove(thing)
                self.inventory.append(thing)
                return f'You pick up a {thing._description} from {container._description}.'
        else:
            return f'You must be halucinating. There is no {thing._description} in here.'

    def drop(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            self.room.inventory.append(item)
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
        new_room = argument
        if not new_room:
            return f"You bump your head against the {argument.lower()}ern wall. That was dumb."
        else:
            self.room = new_room
            return self.room.description()

    def look(self, argument=None):
        '''
        Repeat the view of the room or object
        '''
        if argument is None:
            description = self.room.description()
        else:
            try:
                if argument in self.inventory:
                    item = item._description
                elif argument in self.room.inventory:
                    item = item._description
                else:
                    item = None
                if item:
                    description = item.description()
                else:
                    description = f'You wish you had an {argument}.'
            except AttributeError:
                description = self.room.description()
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
    
    def open(self, item:Item)->str:
        if item in self.inventory or self.room.inventory:
            if isinstance(item, Container) and not item._open:
                message = f'You open the {item.description()}. It contains {[thing._description for thing in item.inventory]}.'
                item.open()
                return message
            elif isinstance(item, Container) and item._open:
                return f'You feel that there is a deep philosophical question between trying to open an open {item.description}.'
            elif not isinstance(item, Container):
                return f'You desparately try to open the {item.description}, for reasons unknown, but it refuses to open.'
        else:
            f'There is no {item}.'
    
    def equip(self, item: Equipment)->str: #not working
        if not isinstance(item, Equipment):
            return f'How do you intend to equip a {item.description()}?'
        equipment = item
        logger.info('player equipment: %s' % equipment._description)
        logger.info('equipment slot: %s' % equipment.slot)
        if self.equipment[equipment.slot] is None:
            #logger.info(f'{self.name} inventory: ', self.inventory)
            self.inventory.remove(equipment)
            self.equipment[equipment.slot] = equipment
            response = f'You equipped the {equipment._description} on your {equipment.slot}.'
        elif self.equipment[equipment.slot] and equipment.slot[-4:] == 'hand':
            if equipment.slot == 'main hand' and not self.equipment['off hand']:
                self.equipment['off hand'] = equipment
                response = f'You take hold of the {equipment._description} in your off hand.'
            if equipment.slot == 'off hand' and not self.equipment['main hand']:
                self.equipment['main hand'] = equipment
                response = f'You take hold of the {equipment._description} in your main hand.'
        else:
            response = f'You must first remove {self.equipment[equipment.slot]._description} from your {equipment.slot}.'
        
        if 'remove' not in response:
            logger.info('equipment: %s' % equipment._description)
            logger.info('equipment skills: %s' % equipment.active_skills)
            for skill in equipment.active_skills:
                setattr(self, skill.__name__, skill)
                self.active_skills[equipment._description] = skill.__name__
            logger.info('equipment skills: %s' % equipment.proficiency_skills)
            for skill, level in equipment.proficiency_skills.items():
                if skill in self.proficiency_skills.keys():
                    self.proficiency_skills[skill] += level
                else:
                    self.proficiency_skills[skill] = level
            logger.info('eqiupment skills: %s' % equipment.passive_skills)
            for skill in equipment.passive_skills:
                if skill not in self.passive_skills:
                    setattr(self, skill.__name__, skill)
        return response
    
    def read(self, book:Book)->str:
        effect = book.reading_effect(self)
        return f'You read {book._description}. {effect}'
