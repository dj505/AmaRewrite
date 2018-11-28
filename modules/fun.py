import discord
from discord.ext import commands
import json
from datetime import datetime
import random

def parser(message):
    return(message[message.find(' ')+1:])

class Fun:
    """
    Fun stuff
    """
    def __init__(self, bot):
        self.bot = bot
        print('Module "{}" loaded'.format(self.__class__.__name__))

    @commands.command(pass_context=True, brief="Gain daily 150 credits")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        """
        This command adds 150 credits to your wallet. Can only be used once per day.
        """
        user = ctx.message.author.id
        with open('wallets.json') as f:
            wallets = json.load(f)
        if user not in wallets:
            wallets[user] = 0
        balance = int(wallets[user]) + 150
        wallets[user] = balance
        with open('wallets.json', 'w') as f:
            json.dump(wallets, f, indent=2, sort_keys=True)
        await ctx.send(':moneybag: Wallet updated successfully! Your balance is now {}'.format(balance))

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True, hidden=True, aliases=['givecredit','gc'])
    async def givecredits(self, ctx, member: discord.Member, amount=0):
        member = str(member.id)
        with open('wallets.json') as f:
            wallets = json.load(f)
        if member not in wallets:
            wallets[member] = 0
        balance = int(wallets[member]) + amount
        wallets[member] = balance
        with open('wallets.json', 'w') as f:
            json.dump(wallets, f, indent=2, sort_keys=True)
        await ctx.send(':moneybag: Wallet updated successfully! Your balance is now {} after being given {} credits.'.format(balance, amount))

    @commands.command(aliases=["cf","coin","flip"])
    async def coinflip(self, ctx):
        await ctx.send(random.choice(["Heads!","Tails!"]))

    @commands.command(pass_context=True, brief='Says something')
    async def say(self, ctx, *, string=""):
        await ctx.message.delete()
        string = string.replace('@everyone', '`@everyone`').replace('@here', '`@here`')
        await ctx.send("{}".format(string))

def setup(bot):
    bot.add_cog(Fun(bot))
