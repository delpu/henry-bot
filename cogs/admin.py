import os
import sys
import discord
from discord.ext import commands
import sqlite3

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Connection to database
    def connect(self):
        connection = sqlite3.connect(os.path.join(sys.path[0],"henry.db"))
        return connection

    #SQL Query
    def insert(self, query):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()

    def retrive(self, query, check=1):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        return data[0] if check else data

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, prefix):
        self.insert(f"UPDATE GUILD_{ctx.guild.id} SET prefix = '{prefix}'")
        embed = discord.Embed(title="", description=f"🔹 Changed local guild prefix to {prefix}", color=0x89cff0 )
        await ctx.send(embed=embed, delete_after=5)
        await ctx.message.delete(delay=5)

def setup(bot):
    bot.add_cog(Admin(bot)) 