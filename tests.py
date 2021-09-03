"""Write some tests"""
import multiprocessing as mp
import socket as sock
import unittest as ut
from logger import logger
from server import Server, rooms_dict
from character import Character
from mongo import mongo
from global_vars import item_dict, rooms_dict, training_dummy


class MongoTest(ut.TestCase):
    def setUp(self):

        training_dummy.save()
        for item in item_dict.values():
            item.save()

        for room in rooms_dict.values():
            room.save()

    def test_character_fromId(self):
        test_dummy = Character.fromId("training dummy")
        self.assertEqual(training_dummy.name, test_dummy.name)
        self.assertEqual(training_dummy.room, test_dummy.room)

class CommandsTest(ut.TestCase):
    logger.info("Running CommandsTest")
    host = "127.0.0.1"
    port = 50000
    server_process = None
    server = None
    client = None

    def send_command(self, command):
        my_message = f"{command}".encode("utf-8") + b"\n"
        self.client.sendall(my_message)

    def receive_response(self):
        return self.client.recv(4096).decode()

    def setUp(self):
        self.server = Server(port=self.port)
        test_character = Character(
            "Player 1", self.server.object_dicts[1][0], STR=3, DEX=3
        )
        self.server.player = test_character
        self.server_process = mp.Process(target=self.server.serve, args=())
        self.server_process.start()
        self.client = sock.socket()
        self.client.connect((self.host, self.port))
        response = self.receive_response()
        self.assertIn("What be your name, adventurer?", response)
        self.send_command("Player 1")
        response = self.receive_response()
        self.assertIn("Player 1", response)

    def tearDown(self) -> None:
        self.client.close()
        self.server_process.kill()
        return super().tearDown()

    def test_bad_commands(self):
        self.send_command("south")
        response = self.receive_response()
        self.assertIn("prevent you from doing that", response)

    def test_look(self):
        self.send_command("look")
        response = self.receive_response()
        self.assertIn("magic box", response)
        self.assertIn("'north', 'west', 'east'", response)

    def test_movement(self):
        north = "move north"
        south = "move south"
        east = "move east"
        west = "move west"
        self.send_command(north)
        north_response = self.receive_response()
        self.send_command(south)
        south_response = self.receive_response()
        self.send_command(east)
        east_response = self.receive_response()
        self.send_command(west)
        west_response = self.receive_response()
        self.assertIn("south", north_response)
        self.assertIn("north", south_response)
        self.assertIn("west", east_response)
        self.assertIn("east", west_response)

    def test_stats(self):
        self.send_command("stats")
        response = self.receive_response()
        self.assertIn("strength: 3", response)
        self.assertIn("dexterity: 3", response)
        self.assertIn("wisdom: 1", response)

    def test_actions(self):
        self.send_command("actions")
        response = self.receive_response()
        self.assertIn(self.server.player.actions(), response)

    def test_say(self):
        self.send_command("say Hi")
        response = self.receive_response()
        self.assertIn("hi", response)

    def test_open(self):
        self.send_command("open magic box")
        response = self.receive_response()
        self.assertIn("You open the a magic box", response)
        self.assertIn("magical crystal", response)

    def test_grab(self):
        self.send_command("grab magic box")
        response = self.receive_response()
        self.assertIn("pick up", response)
        self.send_command("look")
        response = self.receive_response()
        self.assertNotIn("magic box", response)
