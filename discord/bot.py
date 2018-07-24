import asyncio
import json
import platform
import sys

sys.path.insert(0, "/home/chris/Community_Manager")



try:
    from discord.ext import commands
    from discord.ext.commands import Bot
    import discord
except ImportError:
    print('Discord.py is not installed.')
    sys.exit(1)

#Load Settings
with open("/home/chris/Community_Manager/settings/discord_settings.json") as cfg:
    settings = json.load(cfg)

token        = settings["settings"]["token"]
prefix       = settings["settings"]["command_prefix"]


# Modify Bot Description, Prefix, and if it will direct message help.
bot = Bot(command_prefix=prefix, pm_help = False, description="Royal Bot with Cheese")

bot.load_extension(f'discord_modules.attendance')
bot.load_extension(f'discord_modules.grouping')


@bot.event
async def on_ready():
	print('Logged in as '+bot.user.name+' (ID:'+bot.user.id+') | Connected to '+str(len(bot.servers))+' servers | Connected to '+str(len(set(bot.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('--------')
	print('Use this link to invite {}:'.format(bot.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id))
	print('--------')
	print('Created by Mystykall')
	return await bot.change_presence(game=discord.Game(name='Bring a litte class'))

@bot.command()
async def ping():
    await bot.say("Pong!")


bot.run(token)
