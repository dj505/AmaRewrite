import discord
from discord.ext import commands
import json
import sys, traceback
import os
import datetime
from pathlib import Path

print("Starting Amadeus on discord.py version {}".format(discord.__version__))

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

if not Path("settings.json").exists():
    print("Settings does not exist! Please run setup script.")
if not Path("channels.json").exists():
    print("Channel config doesn't exist! Please run setup script.")
if not Path("roles.json").exists():
    print("Role config doesn't exist! Please run setup script.")
if not Path("wallets.json").exists():
    print("Wallet file doesn't exist! Please run setup script.")

with open('settings.json') as f:
    settings = json.load(f)
    token = settings['token']
    prefix = settings['prefix']
    description = settings['description']

with open('channels.json') as f:
    channels = json.load(f)
    log_id = channels['logs']
    welcome_id = channels['welcome']

with open('roles.json') as f:
    role_list = json.load(f)
    bot_role_id = role_list['bot']
    bit_role_id = role_list['default']
    mod_role_id = role_list['mod']
    admin_role_id = role_list['admin']

bot = commands.Bot(command_prefix=prefix, description=description)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        try:
            bot.guild = guild

            bot.log_channel = discord.utils.get(guild.channels, id=log_id)
            bot.welcome_channel = discord.utils.get(guild.channels, id=welcome_id)

            bot.bot_role = discord.utils.get(guild.roles, name="Bot")             # Temporary workaround
            bot.bit_role = discord.utils.get(guild.roles, name="Bit")             # because it won't accept
            bot.mod_role = discord.utils.get(guild.roles, name="Moderator")       # the role ID but it does
            bot.admin_role = discord.utils.get(guild.roles, name="Administrator") # accept the name, idk why

            bot.creator = discord.utils.get(guild.roles, id=165566685540122625)

            print('{0.user} is up and running on {1.name}!'.format(bot, guild))
        except Exception as e:
            print("Failed to start up properly on {} :(".format(guild.name))
            print("\t{}".format(e))

@bot.command(hidden=True, aliases=['gv'])
async def get_variable(ctx):
    await ctx.send('{}\n{}\n{}\n{}'.format(bot.welcome_channel, bot.log_channel, bot.bot_role, bot.bit_role))

modules = [
    'modules.logging',
    'modules.mod',
    'modules.utility',
    'modules.fun'
]

# The following code has been borrowed from https://githiub.com/nh-server/Kurisu
failed_modules = []

for extension in modules:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print('{} failed to load.\n{}: {}'.format(extension, type(e).__name__, e))
        failed_modules.append([extension, type(e).__name__, e])

bot.run(token)
