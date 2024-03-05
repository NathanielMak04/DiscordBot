import discord
import os
import response
import bot
from response import get_response
from discord.flags import Intents
from keepon import keep_alive
from replit import db

# dictionary to store hangman games for each user
hangman_games = {}

async def play_hangman(message):
  user = str(message.author)
  if user not in hangman_games:
    hangman_games[user] = {
      'guesses': [],
      'word': get_random_word(),
      'attempts': 6
    }
    initial_display = ['_' for _ in hangman_games[user]['word']]
    await message.channel.send('Welcome to Hangman! Guess the word by typing one letter at a time')
  else:
    hangman_game = hangman_games[user]
    user_guess = message.content.lower()
    if len(user_guess) == 1:
      if user_guess in hangman_game['guesses']:
        await message.channel.send('You already guessed that letter.')
      elif user_guess in hangman_game['word']:
        for idx, letter in enumerate(hangman_game['word']):
          if user_guess == letter:
            initial_display[idx] = user_guess
        await message.channel.send(' '.join(initial_display))
      else:
        hangman_game['attempts'] -= 1
        await message.channel.send(f'Incorrect guess! Attempts Remaining: {hangman_game["attempts"]}')
    else:
      await message.channel.send('Please guess a single letter')

async def send_message(message, user_message, is_private):
  try:
    response_text = response.get_response(user_message)
    await message.author.send(response_text) if is_private else await message.channel.send(response_text)

  except Exception as e:
    print(e)

def run_discord_bot():
  TOKEN = os.getenv('DISCORD_TOKEN')
  intents = discord.Intents.default()
  intents.message_content = True
  client = discord.Client(intents=intents)

  @client.event
  async def on_ready():
    print(f'{client.user} is now running!')

  @client.event
  async def on_message(message):
    if message.author == client.user:
      return

    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f'{username} said: "{user_message}" ({channel})')

    if user_message[0] == '!':
      if user_message[1:] == 'hangman':
        await bot.play_hangman(message)

    if user_message[0] == '?':
      user_message = user_message[1:]
      await send_message(message, user_message, is_private=True)
    else:
      await send_message(message, user_message, is_private=False)

  if __name__ == '__main__':
      keep_alive()
      client.run(TOKEN)