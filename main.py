import discord
from discord.ext import commands
import confing

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix='/', intents=intents)


class Car:
    def __init__(self, renk, marka):
        self.renk = renk
        self.marka = marka

    def info(self):
        return f"Aracın markası: {self.marka}\nAracın rengi: {self.renk}"


@client.event
async def on_ready():
    print(f'Giriş yaptı: {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await client.process_commands(message)


@client.command()
async def about(ctx):
    await ctx.send('Bu discord.py kütüphanesi ile oluşturulmuş bot!')


@client.command()
async def car(ctx, renk: str, marka: str):
    araba = Car(renk, marka)

    await ctx.send(araba.info())


async def main():
    async with client:
        await client.load_extension("boy")
        await client.start(confing.token)


import asyncio

asyncio.run(main())
