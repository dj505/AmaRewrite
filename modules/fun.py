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

    @commands.command(pass_context=True, brief="Get user information")
    async def userinfo(self, ctx, member=None):
        """
        Get information about a certain user, or yourself, if no user is specified
        """
        with open('wallets.json') as f:
            wallets = json.load(f)
        if member == None:
            member = ctx.message.author
        balance = wallets[str(member.id)]
        embed = discord.Embed(title="User information: {}".format(member.name), description=None, color=0x42F448)
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.add_field(name="ID", value=str(ctx.message.author.id))
        embed.add_field(name="Joined Server", value=str(ctx.message.author.joined_at))
        embed.add_field(name="Joined Discord", value=str(ctx.message.author.created_at))
        embed.add_field(name="Status", value=str(ctx.message.author.status).capitalize())
        embed.add_field(name="Highest Role", value=ctx.message.author.top_role)
        embed.add_field(name="Wallet Balance", value=balance)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, brief="Server information")
    async def serverinfo(self, ctx):
        humans = len([member for member in self.bot.guild.members if not member.bot])
        bots = len(([member for member in self.bot.guild.members if member.bot]))
        embed = discord.Embed(title="Server Information", color=0x42F450)
        text_channels = 0
        voice_channels = 0
        for channel in self.bot.guild.channels:
            if isinstance(channel, discord.TextChannel):
                text_channels += 1
            elif isinstance(channel, discord.VoiceChannel):
                voice_channels += 1
        embed.add_field(name="Name", value=self.bot.guild.name)
        embed.add_field(name="Owner", value=self.bot.guild.owner)
        embed.add_field(name="Member Count", value=str(humans))
        embed.add_field(name="Bot Count", value=str(bots))
        embed.add_field(name="Verification Level", value=str(self.bot.guild.verification_level).capitalize())
        embed.add_field(name="Region", value=self.bot.guild.region)
        embed.add_field(name="Highest Role", value=self.bot.guild.roles[-1])
        embed.add_field(name="Role Count", value=len(self.bot.guild.roles))
        embed.add_field(name="Text Channels", value=str(text_channels))
        embed.add_field(name="Emote Count", value=len(self.bot.guild.emojis))
        embed.add_field(name="Voice Channels", value=str(voice_channels))
        embed.add_field(name="Created At", value=self.bot.guild.created_at.__format__('%A, %B %d, %Y at %H:%M:%S'), inline=False)
        embed.set_thumbnail(url=self.bot.guild.icon_url)
        await ctx.send(embed=embed)

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
