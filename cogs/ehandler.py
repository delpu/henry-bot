import discord
from discord.ext import commands
from discord.ext.commands import errors

class EHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        embed_color = 0xff6961
        if isinstance(err, errors.MissingRequiredArgument) or isinstance(err, errors.BadArgument):
            embed = discord.Embed(title="", description=f"⭕ Something went wrong... Remember about: **{err.param}**", color=embed_color)
        elif isinstance(err, errors.MaxConcurrencyReached):
            embed = discord.Embed(title="", description="⭕ Something went wrong... Finish previous task first!", color=embed_color)
        elif isinstance(err, errors.CommandOnCooldown):
            embed = discord.Embed(title="", description=f"⭕ Slow down a little... Try again in {round(err.retry_after, 1)}s", color=embed_color)
        elif isinstance(err, errors.CommandNotFound):
            embed = discord.Embed(title="", description="⭕ Command not found", color=embed_color)
        elif isinstance(err, errors.MissingPermissions):
            embed = discord.Embed(title="", description="⭕ Something went wrong... You don't have permission to use that command.", color=embed_color)
        elif isinstance(err, errors.BotMissingPermissions):
            embed = discord.Embed(title="", description="🤖 Beep boop... I don't have permissions to perfom that action.", color=embed_color)
        elif isinstance(err, errors.BotMissingRole):
            embed = discord.Embed(title="", description="🤖 Beep boop... Role is missing.", color=embed_color)
        elif isinstance(err, errors.BotMissingAnyRole):
            embed = discord.Embed(title="", description="🤖 Beep boop... Role is missing.", color=embed_color)
        else:
            embed = discord.Embed(title="", description="⭕ Something went wrong...", color=embed_color)

        await ctx.send(embed=embed, delete_after=5)
        await ctx.message.delete(delay=5)
        
def setup(bot):
    bot.add_cog(EHandler(bot)) 