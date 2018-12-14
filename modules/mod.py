import discord
from discord.ext import commands
import json
import time
import asyncio

class Mod:
    """
    Moderation commands.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Module "{}" loaded'.format(self.__class__.__name__))

    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context="True",brief="Kicks a member.")
    async def kick(self, ctx, member : discord.Member, reason="No reason given"):
        """
        Kicks a specified member.
        """
        if ctx.message.author == member:
            await ctx.send(':x: You can\'t kick yourself!')
        elif self.bot.admin_role in member.roles or self.bot.mod_role in member.roles:
            await ctx.send(':x: You can\'t kick a mod/admin!')
        else:
            await member.kick(reason=reason)
            embed = discord.Embed(title="Member kicked by {}".format(ctx.message.author.name), description="Name: {0.name}\nID: {0.id}".format(member), color=0xFFF110)
            embed.set_thumbnail(url=member.avatar_url)
            await self.bot.log_channel.send(embed=embed)
            await ctx.send(':white_check_mark: Kicked user successfully! This action has been logged.')

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True,brief="Bans a member.")
    async def ban(self, ctx, member : discord.Member, reason="No reason given"):
        """
        Bans a specified member.
        """
        if ctx.message.author == member:
            await ctx.send(':x: You can\'t ban yourself!')
        elif self.bot.admin_role in member.roles or self.bot.mod_role in member.roles:
            await ctx.send(':x: You can\'t ban a mod/admin!')
        else:
            await member.ban(reason=reason)
            embed = discord.Embed(title="Member banned by {}".format(ctx.message.author.name), description="Name: {0.name}\nID: {0.id}".format(member), color=0xFF9710)
            embed.set_thumbnail(url=member.avatar_url)
            await self.bot.log_channel.send(embed=embed)
            await ctx.send(':hammer: Banned user successfully! This action has been logged.')

def setup(bot):
    bot.add_cog(Mod(bot))
