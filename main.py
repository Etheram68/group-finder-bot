#!/home/frfrey/group-finder-bot/.venv/bin/python3.9 
import discord
from discord.ext import commands
import sys
import traceback
import os

bot = commands.Bot(command_prefix='!')
bot.remove_command("help")

initial_extensions = ['src.cogs.search']


if __name__ == '__main__':
	for extension in initial_extensions:
		try:
			bot.load_extension(extension)
		except Exception as e:
			print(f'Failed to load extension {extension}.', file=sys.stderr)
			traceback.print_exc()


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


bot.run(os.environ['DISCORD_TOKEN'])
