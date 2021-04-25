import socket
from character import Character
from room import rooms_dict
from items import item_dict, Equipment
from random import randint
#TODO: player inputs during combat

def roll_d20():
    '''generate random number between 1 and 20'''
    return randint(1, 20)
    
def roll_d10():
    '''generate random number between 1 and 10'''
    return randint(1, 10)

def to_hit_roll(player:Character, weapon:Equipment)->int:
    bonus = player.proficiency_skills.get(weapon.associated_skill, 0)
    return roll_d20() + bonus

#TODO: add server logging
class Server(object):
    """
    An adventure game socket server
    
    An instance's methods share the following variables:
    
    * self.socket: a "bound" server socket, as produced by socket.bind()
    * self.client_connection: a "connection" socket as produced by socket.accept()
    * self.input_buffer: a string that has been read from the connected client and
      has yet to be acted upon.
    * self.output_buffer: a string that should be sent to the connected client; for
      testing purposes this string should NOT end in a newline character. When
      writing to the output_buffer, DON'T concatenate: just overwrite.
    * self.done: A boolean, False until the client is ready to disconnect
    * self.room: one of 0, 1, 2, 3. This signifies which "room" the client is in,
      according to the following map:
      
                                     3                      N
                                     |                      ^
                                 1 - 0 - 2                  |
                                 
    When a client connects, they are greeted with a welcome message. And then they can
    move through the connected rooms. For example, on connection:
    
    OK! Welcome to Realms of Venture and dragons! This room has brown wall paper!  (S)
    move north                                                         (C)
    OK! This room has white wallpaper.                                 (S)
    say Hello? Is anyone here?                                         (C)
    OK! You say, "Hello? Is anyone here?"                              (S)
    move south                                                         (C)
    OK! This room has brown wall paper!                                (S)
    move west                                                          (C)
    OK! This room has a green floor!                                   (S)
    quit                                                               (C)
    OK! Goodbye!                                                       (S)
    
    Note that we've annotated server and client messages with *(S)* and *(C)*, but
    these won't actually appear in server/client communication. Also, you'll be
    free to develop any room descriptions you like: the only requirement is that
    each room have a unique description.
    """

    game_name = "Realms of Venture and dragons"
    player = Character('Ghenghiz Cohen', STR=5, DEX=5, INT=5, CON=5, CHA=5)
    training_dummy = Character('training dummy')
    training_dummy.inventory.append('magical crystal')
    training_dummy.room = 3
    character_dict = {'Ghengiz Cohen': player,
                       'training dummy': training_dummy}

    def __init__(self, port=50000):
        self.input_buffer = ""
        self.output_buffer = ""
        self.done = False
        self.socket = None
        self.client_connection = None
        self.port = port

    def connect(self):
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_TCP)

        address = ('127.0.0.1', self.port)
        self.socket.bind(address)
        self.socket.listen(1)

        self.client_connection, address = self.socket.accept()

    def greet(self):
        """
        Welcome a client to the game.
        
        Puts a welcome message and the description of the client's current room into
        the output buffer.
        
        :return: None 
        """
        self.output_buffer = "Hello {}! Welcome to {}! {}".format(
            self.player.name,
            self.game_name,
            rooms_dict[self.player.room].description()
        )

    def get_input(self):
        """
        Retrieve input from the client_connection. All messages from the client
        should end in a newline character: '\n'.
        
        This is a BLOCKING call. It should not return until there is some input from
        the client to receive.
         
        :return: None 
        """
        self.input_buffer = ''
        while True:
            chunk = self.client_connection.recv(10).decode('utf8')
            self.input_buffer = self.input_buffer + chunk
            if '\n' in chunk:
                break

    

    def quit(self, argument=None):
        """
        Quits the client from the server.
        
        Turns `self.done` to True and puts "Goodbye!" onto the output buffer.
        
        Ignore the argument.
        
        :param argument: str
        :return: None
        """
        self.output_buffer = 'Goodbye!'
        self.done = True

    def push_output(self):
        """
        Sends the contents of the output buffer to the client.
        
        This method should prepend "OK! " to the output and append "\n" before
        sending it.
        
        :return: None 
        """

        response = 'OK! '.encode('utf8')
        self.output_buffer += '\n'
        response = response + self.output_buffer.encode('utf8')
        self.client_connection.sendall(response)
    
    def kill_player(self, player:Character)->str:
        '''do all of the stuff that needs to happen on player death.
        mainly: equipment and inventory dump into the room they died.'''
        print(f'{player.name} died.')
        message = f"{player.name} falls to the ground, pooping his pants in death.\nHe drops {player.inventory}, {[item for item in player.equipment.values() if item is not None]}."
        for item in player.inventory:
            player.inventory.remove(item)
            rooms_dict[player.room].inventory.append(item)
        for slot, equipment in player.equipment.items():
            if equipment:
                rooms_dict[player.room].inventory.append(equipment)
                player[slot] = None
        player.room = 0
        return message
    
    def inflict_damage(self, attacker:Character, defender:Character)->str:
        damage = roll_d10() #damage roll
        defender.current_health -= damage
        message = f"{attacker.name} inflicts {damage} of damage onto {defender.name}."
        return message
    
    def combat_exchange(self, attacker:Character, defender:Character, to_hit_rolls:dict)->str:
        print('to hit stats for attacker: ', to_hit_rolls[attacker])
        if to_hit_rolls[attacker] >= defender.armor:
            message = self.inflict_damage(attacker, defender)
        else:
            message = f'{attacker.name} attack bounces off the armor of {defender.name}.'
        return message
    
    def run_combat(self, attacker: Character, defender: Character):
        while attacker.current_health > 0 and defender.current_health > 0:
            #rolls
            hit_bonus = {}
            init_rolls = {}
            to_hit_rolls = {}
            for character in [attacker, defender]:
                print('main weapon: ', character.equipment['main hand'])
                if character.equipment['main hand']:
                    weapon = item_dict[character.equipment['main hand']]
                    hit_bonus[character] = character.proficiency_skills.get(weapon.associated_skill, 0)
                else:
                    hit_bonus[character] = 0
            for character in [attacker, defender]:
                init_rolls[character] = roll_d20() + character._Character__get_stat('dexterity')
            for character in [attacker, defender]:
                to_hit_rolls[character] = roll_d20() + hit_bonus[character]
            # first player attacks
            print('Creating players_turn_order')
            players_turn_order = []
            if init_rolls[attacker] >= init_rolls[defender]:
                players_turn_order = [attacker, defender]
            else:
                players_turn_order = [defender, attacker]
            
            message = self.combat_exchange(players_turn_order[0], players_turn_order[1], to_hit_rolls)
            # if to_hit_rolls[players_turn_order[0]] >= players_turn_order[1].armor:
            #     message = self.inflict_damage(players_turn_order[0], players_turn_order[1])
            #     self.output_buffer = message.encode('utf8')
            #     self.push_output()
            # else:
            #     message = f'{players_turn_order[0].name} attack bounces off the armor of {players_turn_order[1].name}.'
            self.output_buffer = message
            self.push_output()

            if players_turn_order[1].current_health <= 0:
                self.output_buffer = self.kill_player(players_turn_order[1])
                self.push_output()
                break

            message = self.combat_exchange(players_turn_order[1], players_turn_order[0], to_hit_rolls)
            self.output_buffer = message
            self.push_output()
            print('attacker life: ', attacker.current_health)
            print('defender life: ', defender.current_health)

            if players_turn_order[0].current_health <= 0:
                #print that someone died
                self.output_buffer = self.kill_player(players_turn_order[0])
                self.push_output()
                break
            print('attacker health: ', attacker.current_health)
            print('defender health: ', defender.current_health)
    
    def route(self):
        """
        Examines `self.input_buffer` to perform the correct action (move, quit, or
        say) on behalf of the client.
        
        For example, if the input buffer contains "say Is anybody here?" then `route`
        should invoke `self.say("Is anybody here?")`. If the input buffer contains
        "move north", then `route` should invoke `self.move("north")`.
        
        :return: None
        """
        client_input = self.input_buffer.strip().lower()
        print('client_input:', client_input)
        if client_input == 'quit':
            self.quit()
        else:
            try:
                command, arg = client_input.lower().split(' ', 1)
                print('command, arg:', [command, arg])
                if command == 'attack':
                    if arg in rooms_dict[self.player.room].characters:
                        self.run_combat(self.player, self.character_dict[arg])
                    else:
                        self.output_buffer = 'Attack who?'
                else:
                    self.output_buffer = getattr(self.player, command)(arg)
            except ValueError:
                try:
                    self.output_buffer = getattr(self.player, client_input)()
                except AttributeError:
                    self.output_buffer = ("The ancient and powerful magic of AttributeErrors and text managment "
                                          "prevent you from doing that for an unknown reason.")
                except TypeError:
                    self.output_buffer = ("That command requires arguments. Try again.")
            except AttributeError:
                self.output_buffer = f"You desparately try to {command}, but the AttributeErrors are too powerful."

    def serve(self):
        self.connect()
        self.greet()
        self.push_output()

        while not self.done:
            self.get_input()
            self.route()
            self.push_output()

        self.client_connection.close()
        self.socket.close()
