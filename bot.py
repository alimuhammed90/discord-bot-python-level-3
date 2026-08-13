import discord
from discord.ext import commands
import random


class UtilityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, left: int, right: int):
        """Adds two numbers together."""
        await ctx.send(left + right)

    @commands.command()
    async def roll(self, ctx, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return

        result = ', '.join(
            str(random.randint(1, limit))
            for r in range(rolls)
        )

        await ctx.send(result)

    @commands.command(
        description='For when you wanna settle the score some other way'
    )
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices."""

        if not choices:
            await ctx.send('En az iki seçenek vermelisin!')
            return

        await ctx.send(random.choice(choices))

    @commands.command()
    async def repeat(self, ctx, times: int, content='repeating...'):
        """Repeats a message multiple times."""

        if times < 1:
            await ctx.send('Tekrar sayısı 1 veya daha büyük olmalı!')
            return

        if times > 10:
            await ctx.send('En fazla 10 kere tekrar edebilirsin!')
            return

        for i in range(times):
            await ctx.send(content)

    @commands.command()
    async def joined(self, ctx, member: discord.Member):
        """Says when a member joined."""

        if member.joined_at is None:
            await ctx.send(f'{member} has no join date.')
        else:
            await ctx.send(
                f'{member} joined '
                f'{discord.utils.format_dt(member.joined_at)}'
            )

    @commands.group()
    async def cool(self, ctx):
        """Says if a user is cool."""

        if ctx.invoked_subcommand is None:
            await ctx.send(
                f'No, {ctx.subcommand_passed} is not cool'
            )

    @cool.command(name='bot')
    async def _bot(self, ctx):
        """Is the bot cool?"""

        await ctx.send('Yes, the bot is cool.')


async def setup(bot):
    await bot.add_cog(UtilityCommands(bot))
