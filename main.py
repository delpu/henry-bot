import os
import json
import discord
from discord.ext import commands

## Config
def config(filename: str = "config"):
    try:
        with open(f"{filename}.json", encoding='utf8') as data:
            return json.load(data)
    except FileNotFoundError:
        raise FileNotFoundError("Config not found!")

cfg = config()

## Bot Setup
intents = discord.Intents.all() 
bot = commands.Bot(command_prefix=cfg["bot_prefix"],
owner_ids=cfg["owners"],
case_insensitive=True,
help_command=None
)

def printl(text):
	print(f"[#] " + text)

## Loading Cogs
printl("Loading Cogs...")
for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")
        printl(f"Loaded {name}")


## Setting and starting Bot
@bot.event
async def on_ready():
	servers = [] 
	for server in bot.guilds:
		servers.append(server.name)
	print("Logged in as: " + bot.user.name)
	print("Bot ID: " + str(bot.user.id))
	print("Bot is online in: {} servers \n {}".format(len(servers), servers))
	activity = discord.Activity(type=discord.ActivityType.playing, name=cfg["activity"])
	await bot.change_presence(status=discord.Status(cfg["status"]), activity=activity)

try:
    bot.run(cfg["token"])
except Exception as x:
    printl(f"Bot Error: {x}") 