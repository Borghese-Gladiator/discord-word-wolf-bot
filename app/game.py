import random
from prettytable import PrettyTable

class Player:
    def __init__(self, discord_id, discord_object, game_id):
        self.discord_id = discord_id
        self.discord_object = discord_object
        self.game_id = game_id
        self.num_votes = 0
        self.has_voted = False
    ## setters
    def vote(self):
        self.has_voted = True
    def increment_num_votes(self):
        self.num_votes += 1
    def reset(self):
        self.num_votes = 0
        self.has_voted = False

class WordWolfGame:
    def __init__(self, WORD_PAIRS):
        self.WORD_PAIRS = WORD_PAIRS
        self.player_list = []
        self.majority_word = None
        self.minority_word = None
        self.minority_player_id = ""
        self.clueless_player_id = ""
        self.round_number = 0
        self.game_running = False

    def reset(self):
        self.player_list = []
        self.majority_word = None
        self.minority_word = None
        self.minority_player_id = ""
        self.clueless_player_id = ""
        self.round_number = 0
        self.game_running = False

    def join(self, discord_object):
        '''
        Join this game
        @param joining player
        '''
        if self.game_running:
            raise Exception("Game is already in progress")
        if any(player for player in self.player_list if player.discord_id == discord_object.id):
            raise Exception("Player <{}> already in the game".format(discord_object.id))
        self.player_list.append(Player(discord_object.id, discord_object, len(self.player_list)))
    
    def leave(self, discord_id):
        if None == any((player.discord_id == discord_id for player in self.player_list), None):
            raise Exception("Player <{}> has NOT joined the game".format(discord_id))
        self.player_list = filter(lambda id: id == discord_id, self.player_list)
        
    def start(self):
        '''
        Start this game
        @return selected word_pair, tuple of
        '''
        if 2 > len(self.player_list):
            raise Exception("Not enough players have joined the game. Current player count: {}".format(len(self.player_list)))
        self.game_running = True
        self.majority_word, self.minority_word = random.sample(random.choice(self.WORD_PAIRS), 2) # randomly picks a word pair and shuffles that pair
        list_discord_objects = [player.discord_object for player in self.player_list]
        shuffled_discord_objects = random.sample(list_discord_objects, len(list_discord_objects))
        self.minority_player_id, self.clueless_player_id = (shuffled_discord_objects[0], shuffled_discord_objects[1])
        return self.majority_word, self.minority_word, shuffled_discord_objects[0], shuffled_discord_objects[1], shuffled_discord_objects[2:]
    
    def vote(self, voting_discord_id, voted_discord_id):
        '''
        Vote for player in game
        @param voting player
        @param player who was voted
        @return tuple of (status, most_voted_player)
            status - ["NEED_MORE_VOTES", "CORRECT_MINORITY_GUESS", "CORRECT_CLUELESS_GUESS", "INCORRECT_CONTINUE", "INCORRECT_END"]
            most_voted_player is the player to be kicked

        Reference for any: https://stackoverflow.com/questions/598398/searching-a-list-of-objects-in-python
        '''
        if not self.game_running:
            raise Exception("Game is not currently running")
        if not any(player.discord_id == voted_discord_id for player in self.player_list):
            raise Exception("Discord ID not present in list of players <{}>.".format(voted_discord_id))
        
        ## increment num_votes for player who was voted
        for i in range(len(self.player_list)):
            if self.player_list[i].discord_id == voted_discord_id:
                self.player_list[i].increment_num_votes()
        ## change voting player has_voted status
        for i in range(len(self.player_list)):
            if self.player_list[i].discord_id == voting_discord_id:
                self.player_list[i].vote()
        
        ## check if anyone has not voted
        if any(player.has_voted == False for player in self.player_list):
            return ("NEED_MORE_VOTES", None)
        
        ## check if correct player has most votes
        most_voted_player = max(self.player_list, key=lambda player: player.num_votes)
        print(most_voted_player)
        if most_voted_player.discord_id == self.minority_player_id:
            return ("CORRECT_MINORITY_GUESS", most_voted_player.discord_object)
        elif most_voted_player.discord_id == self.clueless_player_id:
            return ("CORRECT_CLUELESS_GUESS", most_voted_player.discord_object)
        else:
            self.round_number += 1
            if self.round_number < 2:
                idx_most_voted_player = self.player_list.index(most_voted_player)
                del self.player_list[idx_most_voted_player]
                return ("INCORRECT_CONTINUE", most_voted_player.discord_object)
            else:
                self.player_list.clear()
                return ("INCORRECT_END", most_voted_player.discord_object)
    
    def guess(self, guesser_discord_id, word):
        if not self.game_running:
            raise Exception("Game is not currently running")
        if guesser_discord_id != self.minority_player_id and guesser_discord_id != self.clueless_player_id:
            raise Exception("Why are you guessing? Why~ are you guessing? https://youtu.be/W6oQUDFV2C0")
        if word == self.majority_word:
            return ("CORRECT_GUESS_END", self.majority_word)
        else:
            return ("INCORRECT_GUESS_END", self.majority_word)

    def build_not_voted_players_string(self):
        player_name_list = []
        for player in self.player_list:
            if player.has_voted == False:
                player_name_list.append(player.discord_object.name)
        return ",".join(player_name_list)

    def build_player_list_string(self):
        print(",".join([player.discord_object.name for player in self.player_list]))
        return ",".join([player.discord_object.name for player in self.player_list])
    
    def build_player_table_string(self):
        t = PrettyTable(['Discord ID', 'Name', '# of Votes'])
        for player in self.player_list:
            t.add_row([player.discord_id, player.discord_object.name, player.num_votes])
        return t
    
    def get_player_list(self):
        return self.player_list
    
    def get_round_running(self):
        return self.game_running
