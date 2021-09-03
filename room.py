from os import stat
from mongo import mongo


class Room(object):
    @classmethod
    def fromId(cls, number):
        with mongo as m:
            collection = m.db["Rooms"]
            room_dict = collection.find_one({"number": number})
            return cls(
                room_dict["number"],
                room_dict["description"],
                inventory=[number for number in room_dict["inventory"]],
                characters=[npc for npc in room_dict["characters"]],
            )

    def __init__(self, number, description, inventory=[], characters=[], exits={}):
        self.number = number
        self._description = description
        self.inventory = inventory
        self.exits = exits
        self.characters = characters

    def save(self):
        room_dict = {
            "number": self.number,
            "description": self._description,
            "inventory": [item.number for item in self.inventory],
            "characters": [NPC.name for NPC in self.characters],
            "exits": {
                direction: room_number
                for (direction, room_number) in self.exits.items()
            },
        }
        with mongo:
            collection = mongo.db["Rooms"]
            collection.replace_one({"number": self.number}, room_dict)

    def description(self):
        """Provide description of room along with any a list of interactable items"""
        desc = self._description
        if self.inventory:
            desc += f'\nIn the room you see a {" ".join([item.description() for item in self.inventory])}.'
        if self.characters:
            desc += f"\nStanding in the room you see {[character.name for character in self.characters]}."

        if self.exits.keys():
            desc += f"\n There are exits to the {self.exits.keys()}."
        return desc
