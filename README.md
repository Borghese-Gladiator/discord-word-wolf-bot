# word-wolf-bot
Discord bot to play Word Wolf with friends on a server

## Commands
Setup
- ```pip-compile dev-requirements.in -o requirements.txt```
- ```pip install -r requirements.txt```
Test
- ```python -m unittest```
- ```coverage run --source ../app -m unittest```
- ```coverage html``` and open /htmlcov/index.html

## Dependencies
- discord.py - library to interface with Discord
- python-dotenv - loads TOKEN environment variable from .env file

## Files
- app.py - interfaces with Discord using bot TOKEN and discord.py
- game.py - WordWolfGame logic and game state
- utils.py - utilities for app.py
- dev-requirements.in - use 

## Game Flow
Player types the below commands to play the game
- $join joins game
- $leave leaves game
- $start starts game with people who joined it
- $vote {discord_id} votes for a person
- $guess {word} guesses given word - you can only guess if you're Minority or Clueless
- $add_word {word1,word2} adds word pair to list of words (NOTE: words will go away when bot goes down)

## Possible Enhancements
- loop through voice channel and add those people to player list
- keep track of winners