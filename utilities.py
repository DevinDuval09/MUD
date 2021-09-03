from random import randint
from character import Character
from items import *
from mongo import mongo

# TODO: add get_object and connect to mongodb
def roll_d20():
    """generate random number between 1 and 20"""
    return randint(1, 20)


def roll_d10():
    """generate random number between 1 and 10"""
    return randint(1, 10)


def roll_d4():
    return randint(1, 4)


def to_hit_roll(player: Character, weapon: Equipment) -> int:
    bonus = player.proficiency_skills.get(weapon.associated_skill, 0)
    return roll_d20() + bonus


def convert_id_list_to_object_list(id_list: list, cls: object) -> list:
    item_type = None
    for value in id_list:
        if cls.__module__ == "items":
            with mongo as m:
                collection = m.db["Items"]
                item_dict = collection.find_one({"number": id_list[value]})
                item_type = item_dict["item_type"]
        id = id_list[value]
        if item_type:
            id_list[value] = eval(item_type).fromId(id)
        else:
            id_list[value] = cls.fromId(id)


def convert_id_dict_to_object_dict(id_dict: dict, cls: object) -> dict:
    for key, id in id_dict.items():
        id_dict[key] = cls.fromId(id)
