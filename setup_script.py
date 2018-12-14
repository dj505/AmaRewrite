import json
from pathlib import Path
import time

settings = {}
channels = {}
roles = {}

if not Path("settings.json").exists():
    with open("settings.json","a+") as f:
        f.write("\{\}")

if not Path("channels.json").exists():
    with open("channels.json","a+") as f:
        f.write("\{\}")

if not Path("roles.json").exists():
    with open("roles.json","a+") as f:
        f.write("\{\}")

if not Path("wallets.json").exists():
    with open("wallets.json","a+") as f:
        f.write("\{\}")

print("Hello! Thanks for using Amadeus!~ Let's get you set up real quick before we're up and running. You'll need the following on hand to get started:")
print("- Token\n- Description (Can be anything, shows in help message)\n- Prefix\n- Bot Owner ID\n- Server Owner ID\n- Log Channel ID\n- Bot Commands Channel ID\n- Welcome channel ID\n- Admin Role ID\n- Mod Role ID\n- Bot Role ID\n- Default Role ID (Assigned when a member joins)")
print("Current step: settings.json setup")

token = input("Bot token: ")
settings["token"] = token
desc = input("Bot description: ")
settings["description"] = desc
prefix = input("Bot prefix: ")
settings["prefix"] = prefix
ownerid = input("Bot owner ID: ")
settings["bot_owner"] = ownerid
serverowner = input("Server owner ID: ")
settings["server_owner"] = serverowner
with open("settings.json","w") as f:
    json.dump(settings, f, indent=2, sort_keys=True)

print("\nsettings.json setup complete~ Next up, channels:")

logs = input("Log channel ID: ")
channels["logs"] = logs
botcmds = input("Bot commands channel ID: ")
channels["bot-commands"] = botcmds
welcome = input("Welcome channel ID: ")
channels["welcome"] = welcome
with open("channels.json","w") as f:
    json.dump(channels, f, indent=2, sort_keys=True)

print("\nChannel setup complete~ Final setup step, roles:")

admin = input("Admin role ID: ")
roles["admin"] = admin
mod = input("Moderator role ID: ")
roles["mod"] = mod
bot = input("Bot role ID: ")
roles["bot"] = bot
default = input("Default role ID: ")
roles["default"] = default
with open("roles.json","w") as f:
    json.dump(roles, f, indent=2, sort_keys=True)

print("\nSetup complete! Welcome to Amadeus!~")
print("This window will close in 10 seconds; feel free to close it yourself, all changes have been saved!")
time.sleep(10)
