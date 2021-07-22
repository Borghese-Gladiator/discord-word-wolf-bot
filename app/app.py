import discord
import os
from dotenv import load_dotenv
from random import choice
from utils import load_word_pairs
from game import WordWolfGame

load_dotenv()
TOKEN = os.getenv('TOKEN')
CLIENT = discord.Client()
WORD_PAIRS = load_word_pairs(r'../word_pairs.txt')
DAD_JOKES = [
    "\"Why do fathers take an extra pair of socks when they go golfing?\" \"In case they get a hole in one!\"')",
    "\"What do a tick and the Eiffel Tower have in common?\" \"They're both Paris sites.\"",
    "\"What do you call a factory that makes okay products?\" \"A satisfactory.\""
]
RULES_STR = "Who among you is the wolf with a different word?\n1. Every player receives a word\n2. One player has a different word from the rest\n3. Discuss to find the imposter\n4. Vote on the person you belive to be the imposter"
game = WordWolfGame(WORD_PAIRS)

@CLIENT.event
async def on_ready():
    print('We have logged in as {0}'.format(CLIENT.user))

@CLIENT.event
async def on_message(message):
    global game
    if message.author == CLIENT.user:
        return

    if message.content.startswith('$rules'):
        await message.channel.send('{}\n\nWORD WOLF RULES\n{}'.format(choice(DAD_JOKES), RULES_STR))
    
    if message.content.startswith('$list'):
        await message.channel.send('Below players are here!\n{}'.format(game.build_player_table_string()))

    if message.content.startswith('$join'):
        try:
            if message.author.id == 246485528348721152:
                await message.channel.send('THE SPELL MASTER#NA1 is the best Gangplank player NA. Watch his ARAM VOD')
            game.join(message.author)
            await message.channel.send('New player: <{}> joined'.format(message.author))
        except Exception as e:
            await message.channel.send(e)
    
    if message.content.startswith('$start'):
        try:
            majority_word, minority_word, minority_player, clueless_player, rest_of_players = game.start()
            await minority_player.send("Your word is <{}>!".format(minority_word))
            await clueless_player.send("You are the clueless! You do not know the word")
            for player in rest_of_players:
                player.send("Your word is <{}>!".format(majority_word))
            await message.channel.send('Word have been SENT to following players!\n{}'.format(game.build_player_table_string()))
        except Exception as e:
            await message.channel.send(e)

    if message.content.startswith('$vote'):
        try:
            voting_discord_id = message.author.id
            voted_discord_id = int(message.content.split(" ", 1)[1])
            game_status, most_voted_player = game.vote(voting_discord_id, voted_discord_id)
            if game_status == "NEED_MORE_VOTES":
                await message.channel.send('Waiting on following players: {}'.format(game.build_not_voted_players_string()))
            elif game_status == "CORRECT_MINORITY_GUESS":
                await message.channel.send('{} was the Minority! Guess the correct word to win! Message in the channel ```guess <word>```'.format(most_voted_player.name))
            elif game_status == "CORRECT_CLUELESS_GUESS":
                await message.channel.send('{} was the Clueless! Guess the correct word to win! Message in the channel ```guess <word>```'.format(most_voted_player.name))
            elif game_status == "INCORRECT_CONTINUE":
                await message.channel.send('{} has been voted out, but was not the minority nor clueless. The GAME continues!!!'.format(most_voted_player.name))
            elif game_status == "INCORRECT_END":
                await message.channel.send('{} was not the minority nor clueless. Minority and Clueless WIN!!!'.format(most_voted_player.name))
            else:
                raise Exception("Unexpected status <{}> or player <{}> returned".format(game_status, most_voted_player))
        except Exception as e:
            print(e)

    if message.content.startswith("$guess"):
        try:
            guesser_discord_id = message.author.id
            word_guess = message.content.split(" ", 1)[1]
            guess_status, correct_word = game.guess(guesser_discord_id, word_guess)
            if guess_status == "INCORRECT_GUESS_END":
                await message.channel.send("INCORRECT guess <{}> by {}! Majority WINS!!!!".format(correct_word, message.author.id))
            elif guess_status == "CORRECT_GUESS_END":
                await message.channel.send("CORRECT guess <{}> by {}! Minority and Clueless WIN!!!".format(correct_word, message.author.id))
        except Exception as e:
            await message.channel.send(e)
    
    if message.content.startswith("$add_word"):
        try:
            word_one, word_two = message.content.split(" ")[1].split(",")
            print(word_one, word_two)
        except Exception as e:
            await message.author.send(e)

    if message.content.startswith('$leave'):
        try:
            game.leave(message.author.id)
            await message.channel.send('{} just left'.format(message.author))
        except Exception as e:
            await message.channel.send(e)

CLIENT.run(TOKEN)
'''
print(message.author)
print(message.author.id)
print(message.content)
'''