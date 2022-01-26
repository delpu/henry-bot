import os
import sys
import json
import discord
from discord.ext import commands
import sqlite3

## Config
def config(filename: str = "config"):
    try:
        with open(f"{filename}.json", encoding='utf8') as data:
            return json.load(data)
    except FileNotFoundError:
        raise FileNotFoundError("Config not found!")

cfg = config()

## Connection to database
def connect():
    connection = sqlite3.connect(os.path.join(sys.path[0],"henry.db"))
    return connection

## SQL Query
def insert(query):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

def retrive(query):
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchone()
        return data

## Get Prefix
def get_prefix(bot, message):
    prefix = retrive(f"SELECT prefix FROM GUILD_{message.guild.id}")
    if not prefix:
        prefix = cfg["bot_prefix"]
    return prefix


## Bot Setup
intents = discord.Intents.all() 
bot = commands.Bot(command_prefix=get_prefix,
owner_ids=cfg["owners"],
case_insensitive=True
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

## Help Command 
class HelpCmd(commands.MinimalHelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(color=0x89cff)
        embed.set_author(name="Henry's commands", icon_url=f'{bot.user.avatar_url}')
        for cog, commands in mapping.items():
           cmdsign = [self.get_command_signature(sig) for sig in commands]
           if cmdsign:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(cmdsign), inline=True)
        channel = self.get_destination()
        await channel.send(embed=embed)
            
bot.help_command = HelpCmd()

## Insert/Remove Guild specific vars
@bot.event
async def on_guild_join(guild):
    prefix = "!"
    try:
        insert(f'''CREATE TABLE IF NOT EXISTS GUILD_{guild.id} (prefix int DEFAULT '{prefix}')''')
        insert(f"INSERT INTO GUILD_{guild.id} DEFAULT VALUES;")
    except Exception as x:
      printl(f"On guild join error: {x}")

@bot.event
async def on_guild_remove(guild):
    try:
        insert(f'''DROP TABLE IF EXISTS GUILD_{guild.id}''')
    except Exception as x:
      printl(f"On guild remove error: {x}")

try:
    bot.run(cfg["token"])
except Exception as x:
    printl(f"Bot Error: {x}") 