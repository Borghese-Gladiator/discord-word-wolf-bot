import sys
import os

# Append path to import modules
sys.path.append(os.path.join('..', 'app'))

# Import modules
import game
from game import WordWolfGame
import unittest

word_pairs_list = [("word1","word2"),("word1","word2"),("word1","word2")]
class DiscordObject:
    def __init__(self, name, id):
        self.name = name
        self.id = id
discord_object_1 =  DiscordObject(name="OKFAMS",id="146485528348721152")
discord_object_2 =  DiscordObject(name="This is Developer Acct",id="246485528348721152")
discord_object_3 =  DiscordObject(name="Tunabutter",id="346485528348721152")
discord_object_4 =  DiscordObject(name="BoxedCube",id="446485528348721152")
discord_object_5 =  DiscordObject(name="MooncakeThief",id="546485528348721152")

class TestGame(unittest.TestCase):
    def test_join(self):
        game = WordWolfGame(word_pairs_list)
        self.assertEqual(len(game.player_list), 0, "Player list should be empty")
        game.join(discord_object_1)
        self.assertEqual(len(game.player_list), 1, "Player list should be 1")

    def test_reset(self):
        game = WordWolfGame(word_pairs_list)
        self.assertEqual(len(game.player_list), 0, "Player list should be empty")
        game.join(discord_object_1)
        game.reset()
        self.assertEqual(len(game.player_list), 0, "Player list should be 1")

    def test_start_no_players(self):
        game = WordWolfGame(word_pairs_list)
        self.assertFalse(game.game_running, "Assert game not running")
        try:
            game.start()
            self.fail("Should throw exception if 0 players try to start game")
        except Exception as e:
            self.assertFalse(game.game_running, "Assert 0 players game does not start")
    
    def test_start_five_players(self):
        game = WordWolfGame(word_pairs_list)
        self.assertFalse(game.game_running, "Assert game not running")
        try:
            game.join(discord_object_1)
            game.join(discord_object_2)
            game.join(discord_object_3)
            game.join(discord_object_4)
            game.join(discord_object_5)
            game.start()
            self.assertTrue(game.game_running, "Assert game starts w/ 5 players")
        except Exception as e:
            self.fail("Should start game correctly")
    
    def test_build_player_table(self):
        game = WordWolfGame(word_pairs_list)
        game.join(discord_object_1)
        game.join(discord_object_2)
        game.join(discord_object_3)
        game.join(discord_object_4)
        game.join(discord_object_5)
        print(game.build_player_table_string())

if __name__ == '__main__':
    unittest.main()