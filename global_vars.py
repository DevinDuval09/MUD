from items import Item, Container, Equipment, Book
from room import Room
from skills import block, bash
from character import Character 

item_dict = {'magic box': Container(0, 'magic box', inventory_items=[], strength=2, dexterity=2),
             'magical crystal': Item(1, 'magical crystal', strength=5, dexterity=5),
             'steel sword': Equipment(2, 'steel sword', 'main hand', associated_skill='sword'),
             'wooden shield': Equipment(3, 'wooden shield', 'off hand', associated_skill='shield', passive_skills=[block], armor=1),
             'chainmail shirt': Equipment(4, 'chainmail shirt', 'chest', armor=3),
             'book of butt kicking': Book(5, 'book of butt kicking', effect=['active_skills', 'proficiency_skills'], active_skills=[bash], proficiency_skills={'shield': 1, 'sword': 2})}

item_dict['magic box'].inventory.append(item_dict['magical crystal'])

training_dummy = Character('training dummy', 3, DEX=9)
training_dummy.current_health = 100
training_dummy.inventory.append(item_dict['magical crystal'])
rooms_dict = {0: Room(0, 'A room with doors headed north, west, and east.', inventory=[item_dict['magic box']], exits={'north': 3, 'west': 1, 'east': 2}),
              1: Room(1, 'A room with a door headed east.', inventory=[item_dict['steel sword'], item_dict['book of butt kicking']], exits={'east': 0}),
              2: Room(2, 'A room with a door headed west.', inventory=[item_dict['wooden shield'], item_dict['chainmail shirt']], exits={'west': 0}),
              3: Room(3, 'A room with a door headed south.', characters=[training_dummy], exits={'south': 0})}

training_dummy.room = rooms_dict[3]
