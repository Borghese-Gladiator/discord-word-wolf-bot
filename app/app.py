import discord
import os
from dotenv import load_dotenv
from utils import get_rules, get_word_pairs
from game import WordWolfGame
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
load_dotenv()
TOKEN = os.getenv('TOKEN')
CLIENT = discord.Client()
game = WordWolfGame(get_word_pairs())

@CLIENT.event
async def on_ready():
    print('We have logged in as {0}'.format(CLIENT.user))

@CLIENT.event
async def on_message(message):
    global game
    if message.author == CLIENT.user:
        return

    if message.content.startswith('$rules'):
        logging.info('$rules - print rules to channel')
        await message.channel.send('{}\n\nWORD WOLF RULES\n{}'.format(get_rules()))
    
    if message.content.startswith('$list'):
        logging.info('$list - print player table to channel')
        table_embed = discord.Embed(title='Players Info', description=game.build_player_table_string())
        await message.channel.send(table_embed)

    if message.content.startswith('$join'):
        logging.info('$join - new player <{}> joined'.format(message.author))
        try:
            if message.author.id == 246485528348721152:
                await message.channel.send('THE SPELL MASTER#NA1 is the best Gangplank player NA. Watch his ARAM VOD')
            game.join(message.author)
            await message.channel.send('New player: <{}> joined'.format(message.author))
        except Exception as e:
            logging.info('Exception e: <{}>'.format(e))
            await message.channel.send(e)
    
    if message.content.startswith('$start'):
        logging.info('$start - player <{}> ran start'.format(message.author))
        try:
            majority_word, minority_word, minority_player, clueless_player, rest_of_players = game.start()
            logging.info('Minority Player <{}> with word <{}>'.format(minority_player, minority_word))
            logging.info('Clueless Player <{}>'.format(clueless_player))
            logging.info('Majority Player List <{}> with word <{}>'.format(', '.join(rest_of_players), majority_word))
            await minority_player.send("Your word is <{}>!".format(minority_word))
            await clueless_player.send("You are the clueless! You do not know the word")
            for player in rest_of_players:
                await player.send("Your word is <{}>!".format(majority_word))
            await message.channel.send('Word have been SENT!')
            table_embed = discord.Embed(title='Players Info', description=game.build_player_table_string())
            await message.channel.send(table_embed)
        except Exception as e:
            logging.info('Exception e: <{}>'.format(e))
            await message.channel.send(e)

    if message.content.startswith('$vote'):
        logging.info('$vote - player <{}> ran $vote with content <{}>'.format(message.author, message.content))
        try:
            voting_discord_id = message.author.id
            voted_discord_id = int(message.content.split(" ", 1)[1])
            game_status, most_voted_player = game.vote(voting_discord_id, voted_discord_id)
            logging.info('Game Status <{}> with most voted player <{}>'.format(game_status, most_voted_player))
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
            logging.info('Exception e: <{}>'.format(e))
            await message.channel.send(e)

    if message.content.startswith("$guess"):
        logging.info('$guess - player <{}> ran $guess with content <{}>'.format(message.author, message.content))
        try:
            guesser_discord_id = message.author.id
            word_guess = message.content.split(" ", 1)[1]
            guess_status, correct_word = game.guess(guesser_discord_id, word_guess)
            if guess_status == "INCORRECT_GUESS_END":
                await message.channel.send("INCORRECT guess <{}> by {}! Majority WINS!!!!\nYour guess was {}".format(correct_word, message.author.id, word_guess))
            elif guess_status == "CORRECT_GUESS_END":
                await message.channel.send("CORRECT guess <{}> by {}! Minority and Clueless WIN!!!\nYour guess was {}".format(correct_word, message.author.id, word_guess))
        except Exception as e:
            logging.info('Exception e: <{}>'.format(e))
            await message.channel.send(e)
    
    if message.content.startswith('$leave'):
        logging.info('$leave - player <{}> ran $leave'.format(message.author))
        try:
            game.leave(message.author)
            await message.channel.send('{} just left'.format(message.author))
        except Exception as e:
            logging.info('Exception e: <{}>'.format(e))
            await message.channel.send(e)

CLIENT.run(TOKEN)